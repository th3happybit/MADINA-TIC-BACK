from .models import *
from rest_framework import serializers,validators
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.models import Group
import os,binascii


# User Model serializer
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['uid','first_name','last_name','email','phone','date_of_birth','address','national_id','image','role','is_approved','is_active','is_superuser','created_on']
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
		User.email_user(instance, "Madina-Tic Welcome", "Welcome, your account has been created <br>your password: "+password)
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

class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['uid','first_name','last_name','email','phone','date_of_birth','address','national_id','image','role','is_approved','is_active','is_superuser','created_on']
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

# Document serializer
class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ['dmid', 'filetype', 'src', 'declaration', 'created_on']
		lookup_field = ['dmid']

# Declaration  type serializer 
class DeclarationTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeclarationType
		fields = ['dtid', 'name', 'created_on']
		lookup_field = 'dtid'

# Declaration serializer
class DeclarationSerializer(serializers.ModelSerializer):
	attachments = DocumentSerializer(many=True, read_only=True)
	class Meta:
		model = Declaration
		fields = ['did', 'title', 'desc', 'address', 'geo_cord', 'citizen', 'status', 'dtype', 'attachments','created_on', 'modified_at', 'validated_at']
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