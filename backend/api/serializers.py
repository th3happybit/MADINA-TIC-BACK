import binascii
import pytz
from django.conf import settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.models import Group
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .notification_push import *
from .models import *


# User Model serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id',
                  'image', 'is_french', 'role', 'is_approved', 'is_active', 'notif_seen', 'is_superuser', 'created_on']
        read_only_fields = ['is_superuser']
        lookup_field = 'uid'
        extra_kwargs = {
            'date_of_birth': {'error_messages': {'invalid': "invalid format"}},
        }

    def create(self, validated_data):
        instance = super().create(validated_data)
        clients = Group.objects.get(name='clients')
        admins = Group.objects.get(name='admins')
        maires = Group.objects.get(name='maires')
        services = Group.objects.get(name='services')
        if instance.role == 'Client':
            clients.user_set.add(instance)
        elif instance.role == 'Admin':
            admins.user_set.add(instance)
        elif instance.role == 'Maire':
            maires.user_set.add(instance)
        elif instance.role == 'Service':
            services.user_set.add(instance)
        password = binascii.hexlify(os.urandom(10)).decode()
        instance.set_password(password)
        instance.save()
        User.email_user(instance, "Madina-Tic Welcome",
                        "Welcome, your account has been created <br>your password: " + password)
        return instance

    def update(self, instance, validated_data):
        is_approved_key = None
        is_active_key = None
        if 'is_approved' in validated_data:
            is_approved_key = validated_data['is_approved']
        if 'is_active' in validated_data:
            is_active_key = validated_data['is_active']
        if is_approved_key:
            if is_approved_key == True and instance.is_approved == False:
                subject_validate = "Madina-Tic Validation mail"
                message_validate = "Welcome, Your Registration has been accepted, you can use your account now! <br>Madina-Tic Validation"
                User.email_user(instance, subject_validate, message_validate)
            elif is_approved_key == False and instance.is_approved == False:
                subject_reject = "Madina-Tic Rejection mail"
                message_reject = "Good bye, Your Registration has been rejected! <br>Madina-Tic Rejection"
                User.email_user(instance, subject_reject, message_reject)
        if is_active_key:
            if is_active_key == True and instance.is_active == False:
                subject_reject = "Madina-Tic Activation mail"
                message_reject = "Welcome back, Your account has been activated! <br>Madina-Tic Welcome"
                User.email_user(instance, subject_reject, message_reject)
            elif is_active_key == False and instance.is_active == True:
                subject_desactivate = "Madina-Tic Desactivation Mail "
                message_desactivation = "Your account has been disabled, Bye! <br>Madina-Tic Deactivation"
                User.email_user(instance, subject_desactivate, message_desactivation)
        return super().update(instance, validated_data)


# User Model serializer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'first_name', 'last_name', 'email', 'phone']
        read_only_fields = ['is_superuser']
        lookup_field = 'uid'
        extra_kwargs = {
            'date_of_birth': {'error_messages': {'invalid': "invalid format"}},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id',
                  'image', 'role', 'is_french', 'is_approved', 'notif_seen', 'is_active', 'is_superuser', 'created_on']
        read_only_fields = ['is_approved', 'is_active', 'is_superuser', 'role', 'created_on']
        lookup_field = 'uid'


# Custom Registration
class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(required=True)
    address = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'password1': self.validated_data.get('password1', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'address': self.validated_data.get('address', ''),
        }

    def save(self, request):
        clients = Group.objects.get(name='clients')
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.phone = self.cleaned_data.get('phone')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.address = self.cleaned_data.get('address')
        user.save()
        clients.user_set.add(user)
        return user


# Document serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['dmid', 'filetype', 'src', 'declaration', 'report', 'created_on']
        lookup_field = ['dmid']


# Declaration  type serializer
class DeclarationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationType
        fields = ['dtid', 'name', 'service', 'created_on']
        lookup_field = 'dtid'


# Declaration serializer
class DeclarationSerializer(serializers.ModelSerializer):
    attachments = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Declaration
        fields = ['did', 'title', 'desc', 'parent_declaration', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype',
                  'attachments', 'created_on', 'modified_at', 'validated_at']
        lookup_field = ['did']

    def create(self, validated_data):
        citoyen = validated_data['citizen']
        maire = User.objects.filter(role='Maire').first()
        if 'service' in validated_data:
            service = validated_data['service']
        declaration_title = validated_data['title']
        title = 'Déclaration crée'
        body = 'La déclaration ' +declaration_title+ ' crée par '+ citoyen.first_name

        instance = super().create(validated_data)
        # beams notification
        push_notify(citoyen.uid, maire.uid, title, body)
        # channels notification 
        data = {
            'title': title,
            'body' : body
        }
        channel = u'Declaration'
        event = u'Creation'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.maire = maire
        notification.save()
        return instance

    def update(self, instance, validated_data):
        declaration_state = validated_data["status"]
        declaration_title = instance.title
        citoyen = instance.citizen
        maire = User.objects.filter(role='Maire').first()
        title = 'Déclaration modifiée'
        body ='la déclaration '+ declaration_title + ' a été modifiée et le statut actuel: ' + declaration_state
        # beams notif
        push_notify(citoyen.uid, maire.uid, title, body)
        # channels notif
        data = {
            'title': title,
            'body' : body,
            'status': declaration_state
        }
        channel = u'Declaration'
        event = u'Update'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        if 'status' in validated_data:
            status = validated_data["status"]
            if status == 'validated':
                notification.title = title
                notification.body = body
                notification.citoyen = citoyen
                service = validated_data['service']
                notification.service = service
            else:
                notification.title = title
                notification.body = body
                notification.citoyen = citoyen
                notification.maire = maire
        notification.save()
        return super().update(instance, validated_data)

# Declaration serializer
class DeclarationNestedSerializer(serializers.ModelSerializer):
    attachments = DocumentSerializer(many=True, read_only=True)
    citizen = ServiceSerializer(read_only=True)

    class Meta:
        model = Declaration
        fields = ['did', 'title', 'desc', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype',
                  'attachments', 'created_on', 'modified_at', 'validated_at']
        lookup_field = ['did']


# Declaration rejection serializer
class DeclarationRejectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationRejection
        fields = ['drid', 'maire', 'reason', 'declaration', 'created_on']
        lookup_field = ['drid']

    def create(self, validated_data):
        declaration = validated_data['declaration']
        reason = validated_data['reason']
        citoyen = declaration.citizen
        maire = validated_data['maire']
        service = declaration.service
        title = 'Rejection'
        body = 'La déclaration : '+ declaration.title +' a été rejeté par ' + maire.first_name +''+ 'et la raison c`est: '+ reason

        instance = super().create(validated_data)
        instance.declaration.status = 'refused'
        instance.declaration.save()
        # beams notification
        push_notify(citoyen.uid, maire.uid, title, body)
        # channels notification
        data = {
            'title': title,
            'body': body
        }
        channel = u'Declaration'
        event = u'Rejection'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.citoyen = citoyen
        notification.save()
        return instance


# Declaration complement demand serializer
class DeclarationComplementDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationComplementDemand
        fields = ['dcid', 'maire', 'reason', 'declaration', 'created_on']
        lookup_field = ['dcid']

    def create(self, validated_data):
        declaration = validated_data['declaration']
        reason = validated_data['reason']
        maire = validated_data['maire']
        citoyen = declaration.citizen
        title = 'Demande de complément'
        body = 'La déclaration : '+ declaration.title +' besoin de complément d`aprés le maire ' + maire.first_name +''+ 'et la raison c`est: '+ reason

        instance = super().create(validated_data)
        instance.declaration.status = 'lack_of_info'
        instance.declaration.save()
        push_notify(citoyen.uid, maire.uid, title, body)
        data = {
            'title': title,
            'body': body
        }
        channel = u'Declaration'
        event = u'Complement'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.citoyen = citoyen
        notification.save()
        return instance


# Report serializer
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['rid', 'declaration', 'title', 'desc', 'service', 'status', 'created_on', 'modified_at',
                  'validated_at']
        lookup_field = ['rid']
    def create(self, validated_data):
        report_title = validated_data["title"]
        service = validated_data["service"]
        maire = User.objects.filter(role='Maire').first()
        title = 'Rapport crée'
        body = 'le rapport :' +''+ report_title+'a été crée par' +''+service.first_name

        instance = super().create(validated_data)
        # send notification 
        data = {
            'title': title,
            'body': body
        }
        channel = u'Report'
        event = u'Creation'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.maire = maire
        notification.save()
        return instance

# Report rejection serializer
class ReportRejectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRejection
        fields = ['rrid', 'maire', 'reason', 'report', 'created_on']
        lookup_field = ['rrid']

    def create(self, validated_data):
        report = validated_data["report"]
        service = report.service
        reason = validated_data["reason"]
        maire = validated_data['maire']
        title = 'le rapport Rejecté'
        body = 'le rapport :' +''+ report.title+'a été rejecté a cause de :'+''+reason+'' 'par' +''+maire.first_name

        instance = super().create(validated_data)
        instance.report.status = 'refused'
        instance.report.save()
        # send channels notif
        data = {
            'title': title,
            'body': body
        }
        channel = u'Report'
        event = u'Rejection'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.service = service
        notification.save()
        return instance


# Report complement demand
class ReportComplementDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComplementDemand
        fields = ['rcid', 'maire', 'report', 'reason', 'created_on']
        lookup_field = ['rcid']

    def create(self, validated_data):
        report = validated_data["report"]
        service = report.service
        reason = validated_data["reason"]
        maire = validated_data['maire']
        title = 'Demande de complément'
        body = 'le rapport :' +''+ report.title+'a besoin de complément a cause de :'+''+reason+'' 'par' +''+maire.first_name

        instance = super().create(validated_data)
        instance.report.status = 'lack_of_info'
        instance.report.save()
        # send channels notif
        data = {
            'title': title,
            'body': body
        }
        channel = u'Report'
        event = u'Complement'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.service = service
        notification.save()
        return instance


utc = pytz.UTC

# Announce serializer
class AnnounceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
    class Meta:
        model = Announce
        fields = ['aid', 'title', 'desc', 'service', 'image', 'status', 'created_on', 'start_at', 'end_at']
        lookup_field = ['aid']
    
    def create(self, validated_data):
        announce_title = validated_data["title"]
        service = validated_data ["service"]
        maire = User.objects.filter(role='Maire').first()
        title = 'Announce crée'
        body = 'l`announce :' +''+ announce_title+'a été crée par' +''+service.first_name

        instance = super().create(validated_data)
        # send channels notif
        data = {
            'title': title,
            'body': body
        }
        channel = u'Announce'
        event = u'Creation'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.maire = maire
        notification.save()
        return instance

# Announce Nested serializer
class AnnounceNestedSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Announce
        fields = ['aid', 'title', 'desc', 'service', 'image', 'status', 'created_on', 'start_at', 'end_at']
        lookup_field = ['aid']

    def validate(self, validated_data):
        current_date = utc.localize(datetime.datetime.now())  # for comparaison we use same date format

        if validated_data['start_at'] > validated_data['end_at']:
            raise serializers.ValidationError("The end date (time) must occur after the start date (time)")
        elif current_date > validated_data['start_at']:
            raise serializers.ValidationError("The start date (time) must occur after the current date date (time)")
        elif current_date > validated_data['end_at']:
            raise serializers.ValidationError("The end date (time) must occur after the current date (time)")

        return validated_data


# Announce Complement Demand Serializer
class AnnounceComplementDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnounceComplementDemand
        fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
        lookup_field = ['acid']

    def create(self, validated_data):
        announce = validated_data["announce"]
        service = announce.service
        maire = validated_data["maire"]
        reason = validated_data["reason"]
        title = 'Demande de complément'
        body = 'l`announce :' +''+ announce.title+'a besoin de complément a cause de :'+''+reason+'' 'par' +''+maire.first_name
        
        instance = super().create(validated_data)
        instance.announce.status = 'lack_of_info'
        instance.announce.save()
        # send channels notif
        data = {
            'title': title,
            'body': body
        }
        channel = u'Announce'
        event = u'Complement'
        channels_notify(channel, event, data)
        # save the notification for users no logged in
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.service = service
        notification.save()
        return instance

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['nid', 'title', 'body', 'citoyen', 'maire', 'service', 'created_on']
        lookup_field = 'nid'

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['fid', 'sender_first_name', 'sender_last_name', 'sender_email', 'subject', 'message']
        lookup_field = 'fid'

    def create(self, validated_data):
        recipient_list = settings.ADMINS
        from_email = validated_data['sender_email']
        if 'message' and 'subject' in validated_data:
            message = validated_data['message']
            subject = validated_data['subject']
        instance = super().create(validated_data)
        instance.save()
        FeedBack.email_admins(subject, message, from_email, recipient_list) 
        return instance

class CityInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, allow_blank=True)
    name_ar = serializers.CharField(max_length=50, allow_blank=True)
    name_am = serializers.CharField(max_length=50, allow_blank=True)
    wilaya = serializers.CharField(max_length=20, allow_blank=True)
    daira = serializers.CharField(max_length=20, allow_blank=True)
    indicatif = serializers.CharField(max_length=3, allow_blank=True)
    population = serializers.CharField(max_length=20, allow_blank=True)
    surface = serializers.CharField(max_length=20, allow_blank=True)
    maire_fullname = serializers.CharField(max_length=30, allow_blank=True)
    description = serializers.CharField(max_length=300, allow_blank=True)
    cord = serializers.CharField(max_length=20, allow_blank=True)
    altitude = serializers.CharField(max_length=20, allow_blank=True)
    
    def create(self, validated_data):
        return CityInfo(**validated_data)
    
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance