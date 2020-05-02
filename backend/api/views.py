from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
#from .models import Declaration as DeclarationModel
#from .serializers import DeclarationSerializer as DeclarationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# User Model View for admin access only
class UserView(viewsets.ModelViewSet):
	permission_classes = [IsAdminUser]
	queryset = User.objects.all()
	serializer_class = UserSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'uid'
	filter_fields = ['first_name','last_name','email','phone','date_of_birth','address','role','is_approved','is_active','is_superuser','created_on']
	filterset_fields = ['first_name','last_name','email','phone','date_of_birth','address','role','is_approved','is_active','is_superuser','created_on']
	search_fields = ['first_name','last_name','email','phone','date_of_birth','address','role','is_approved','is_active','is_superuser','created_on']
	ordering_fields = ['first_name','last_name','email','phone','date_of_birth','address','role','is_approved','is_active','is_superuser','created_on']
	
# DeclarationType Model View
class DeclarationTypeView(viewsets.ModelViewSet):
	queryset = DeclarationType.objects.all()
	serializer_class = DeclarationTypeSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'dtid'
	filter_fields = ['name']
	filterset_fields = ['name']
	search_fields = ['name']
	ordering_fields = ['name']

# Declaration Model View 
class DeclarationView(viewsets.ModelViewSet):
	queryset = Declaration.objects.all()
	serializer_class = DeclarationSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'did'
	filter_fields = ['title', 'address', 'geo_cord', 'citizen', 'status', 'dtype', 'created_on', 'modified_at', 'validated_at']
	filterset_fields = ['title', 'address', 'geo_cord', 'citizen', 'status', 'dtype', 'created_on', 'modified_at', 'validated_at']
	search_fields = ['title', 'address', 'geo_cord', 'citizen', 'status', 'dtype', 'created_on', 'modified_at', 'validated_at']
	ordering_fields = ['title', 'address', 'geo_cord', 'citizen', 'status', 'dtype', 'created_on', 'modified_at', 'validated_at']

# DeclarationRejection Model View
class DeclarationRejectionView(viewsets.ModelViewSet):
	queryset = DeclarationRejection.objects.all()
	serializer_class = DeclarationRejectionSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'drid'
	filter_fields = ['maire', 'declaration', 'created_on']
	filterset_fields = ['maire', 'declaration', 'created_on']
	search_fields = ['maire', 'declaration', 'created_on']
	ordering_fields = ['maire', 'declaration', 'created_on']

# DeclarationComplementDemand Model View 
class DeclarationComplementDemandView(viewsets.ModelViewSet):
	queryset = DeclarationComplementDemand.objects.all()
	serializer_class = DeclarationComplementDemandSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'dcid'
	filter_fields = ['maire', 'declaration', 'created_on']
	filterset_fields = ['maire', 'declaration', 'created_on']
	search_fields = ['maire', 'declaration', 'created_on']
	ordering_fields = ['maire', 'declaration', 'created_on']

# Document Model View 
class DocumentView(viewsets.ModelViewSet):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'dmid'
	filter_fields = ['filetype', 'declaration', 'created_on']
	filterset_fields = ['filetype', 'declaration', 'created_on']
	search_fields = ['filetype', 'declaration', 'created_on']
	ordering_fields = ['filetype', 'declaration', 'created_on']

# Report Model View 
class ReportView(viewsets.ModelViewSet):
	queryset = Report.objects.all()
	serializer_class = ReportSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'rid'
	filter_fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']
	filterset_fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']
	search_fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']
	ordering_fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']

# ReportRejection Model View 
class ReportRejectionView(viewsets.ModelViewSet):
	queryset = ReportRejection.objects.all()
	serializer_class = ReportRejectionSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'rrid'
	filter_fields = ['maire', 'report', 'created_on']
	filterset_fields = ['maire', 'report', 'created_on']
	search_fields = ['maire', 'report', 'created_on']
	ordering_fields = ['maire', 'report', 'created_on']

# ReportComplementDemand Model View 
class ReportComplementDemandView(viewsets.ModelViewSet):
	queryset = ReportComplementDemand.objects.all()
	serializer_class = ReportComplementDemandSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	lookup_field = 'rcid'
	filter_fields = ['maire', 'report', 'created_on']
	filterset_fields = ['maire', 'report', 'created_on']
	search_fields = ['maire', 'report', 'created_on']
	ordering_fields = ['maire', 'report', 'created_on']

# Announce Model View 
class AnnounceView(viewsets.ModelViewSet):
	queryset = Announce.objects.all()
	serializer_class = AnnounceSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filter_fields = ['title', 'status', 'created_on', 'start_at', 'end_at']
	filterset_fields = ['title', 'status', 'created_on', 'start_at', 'end_at']
	search_fields = ['title', 'status', 'created_on', 'start_at', 'end_at']
	ordering_fields = ['title', 'status', 'created_on', 'start_at', 'end_at']