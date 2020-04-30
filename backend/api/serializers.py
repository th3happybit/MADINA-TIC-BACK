from .models import *
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.models import Group

# User Model serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid','first_name','last_name','email','phone','date_of_birth','address','role','is_approved','is_active','is_superuser','created_on']
        read_only_fields = ['is_superuser']
        lookup_field = 'uid'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid','first_name','last_name','email','phone','date_of_birth','address','role','is_approved','is_active','is_superuser','created_on']
        read_only_fields = ['is_approved','is_active','is_superuser','role','created_on']
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

# Declaration  type serializer 
class DeclarationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationType
        fields = ['dtid', 'name', 'created_on']
        lookup_field = 'dtid'

# Declaration serializer
class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = ['did', 'title', 'desc', 'address', 'geo_cord', 'citizen', 'status', 'dtype', 'created_on', 'modified_at', 'validated_at']
        lookup_field = ['did']

# Declaration rejection serializer 
class DeclarationRejectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationRejection
        fields = ['drid', 'maire', 'reason', 'declaration', 'created_on']
        lookup_field = ['drid']

# Declaration complement demand serializer 
class DeclarationComplementDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationComplementDemand
        fields = ['dcid', 'maire', 'reason', 'declaration', 'created_on']
        lookup_field = ['dcid']

# Document serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['dmid', 'filetype', 'src', 'declaration', 'created_on']
        lookup_field = ['dmid']

# Report serializer 
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['rid', 'declaration', 'title', 'desc', 'service', 'status', 'created_on', 'modified_at', 'validated_at']
        lookup_field = ['rid']

# Report rejection serializer 
class ReportRejectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRejection
        fields = ['rrid', 'maire', 'reason', 'report', 'created_on']
        lookup_field = ['rrid']

# Report complement demand 
class ReportComplementDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComplementDemand
        fields = ['rcid', 'maire', 'report', 'reason', 'created_on']
        lookup_field = ['rcid']


# Announce serializer
class AnnounceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announce
        fields = ['aid', 'title', 'desc', 'status', 'created_on', 'start_at', 'end_at']
        lookup_field = ['aid']