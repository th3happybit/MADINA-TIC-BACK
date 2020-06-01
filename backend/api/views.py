from rest_framework import viewsets, generics, status, mixins
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseRedirect
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .pagination import CustomPagination
from django_filters import rest_framework as filters
import django_filters
from django.http import Http404


# User Model View for admin access only
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'uid'
    filter_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id', 'role',
                     'is_approved', 'is_active', 'is_superuser', 'created_on']
    filterset_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id', 'role',
                        'is_approved', 'is_active', 'is_superuser', 'created_on']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id', 'role',
                     'is_approved', 'is_active', 'is_superuser', 'created_on']
    ordering_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id', 'role',
                       'is_approved', 'is_active', 'is_superuser', 'created_on']
    pagination_class = CustomPagination


# DeclarationType Model View
class DeclarationTypeView(viewsets.ModelViewSet):
    pagination_class = None
    queryset = DeclarationType.objects.all()
    serializer_class = DeclarationTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'dtid'
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']


# choice filter for declaration
states = [
    ('draft', 'draft'),
    ('not_validated', 'not_validated'),
    ('lack_of_info', 'lack_of_info'),
    ('validated', 'validated'),
    ('refused', 'refused'),
    ('under_treatment', 'under_treatment'),
    ('treated', 'treated'),
    ('archived', 'archived'),
]


class DeclarationFilter(filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(choices=states)

    class Meta:
        model = Declaration
        fields = ['title', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype', 'created_on',
                  'modified_at', 'validated_at']


# Declaration Model View
class DeclarationView(viewsets.ModelViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DeclarationFilter
    lookup_field = 'did'
    filter_fields = ['title', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype', 'created_on',
                     'modified_at', 'validated_at']
    filterset_fields = ['title', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype',
                        'created_on', 'modified_at', 'validated_at']
    search_fields = ['title', 'address', 'geo_cord', 'citizen__uid', 'citizen__first_name', 'citizen__last_name',
                     'service__uid', 'priority', 'status', 'dtype__name', 'created_on', 'modified_at', 'validated_at']
    ordering_fields = ['title', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype',
                       'created_on', 'modified_at', 'validated_at']


# DeclarationRejection Model View
class DeclarationRejectionView(viewsets.ModelViewSet):
    queryset = DeclarationRejection.objects.all()
    serializer_class = DeclarationRejectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'drid'
    filter_fields = ['maire', 'declaration', 'created_on']
    filterset_fields = ['maire', 'declaration', 'created_on']
    search_fields = ['maire__uid', 'declaration__did', 'created_on']
    ordering_fields = ['maire', 'declaration', 'created_on']


# DeclarationComplementDemand Model View
class DeclarationComplementDemandView(viewsets.ModelViewSet):
    queryset = DeclarationComplementDemand.objects.all()
    serializer_class = DeclarationComplementDemandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'dcid'
    filter_fields = ['maire', 'declaration', 'created_on']
    filterset_fields = ['maire', 'declaration', 'created_on']
    search_fields = ['maire__uid', 'declaration__did', 'created_on']
    ordering_fields = ['maire', 'declaration', 'created_on']


# Document Model View  Support GET and POST requests
class DocumentView(APIView):
    parser_class = [MultiPartParser, FileUploadParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'dmid'
    filter_fields = ['dmid', 'filetype', 'declaration', 'report__rid', 'created_on']
    filterset_fields = ['dmid', 'filetype', 'declaration', 'report__rid', 'created_on']
    search_fields = ['dmid', 'filetype', 'declaration', 'report__rid', 'created_on']
    ordering_fields = ['dmid', 'filetype', 'declaration', 'report__rid', 'created_on']

    """ filter the queryset with whichever filter backend is in use """

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    """get all instances"""

    def get_queryset(self):

        return Document.objects.all()

    def get(self, request):
        the_filtered_qs = self.filter_queryset(self.get_queryset())
        serializer = DocumentSerializer(the_filtered_qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        filetype = request.data['filetype']
        declaration = request.data['declaration']
        report = request.data['report']
        docs = dict((request.data).lists())['src']
        flag = 1
        arr = []
        for doc in docs:
            modified_data = modify_input_for_multiple_files(filetype, doc, declaration, report)
            file_serializer = DocumentSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr)
        else:
            return Response(arr)


# Document details for upadte/delete/retrieve document
class DocumentDetailView(APIView):
    parser_class = [MultiPartParser, FileUploadParser]
    filter_backends = []

    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    # get instance
    def get(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    # update instance
    def put(self, request, pk, format=None):
        filetype = request.data['filetype']
        declaration = request.data['declaration']
        report = request.data['report']
        docs = dict((request.data).lists())['src']
        flag = 1
        arr = []
        # document = self.get_object(pk)
        for doc in docs:
            modified_data = modify_input_for_multiple_files(filetype, doc, declaration, report)
            file_serializer = DocumentSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_200_OK)
        else:
            return Response(arr)

    # delete instance
    def delete(self, request, pk, format=None):
        message = {'success': 'document deleted successfully'}
        document = self.get_object(pk)
        document.delete()
        return Response(message, status=status.HTTP_200_OK)


# choice filter for declaration
states_report = [
    ('not_validated', 'not_validated'),
    ('lack_of_info', 'lack_of_info'),
    ('work_not_finished', 'work_not_finished'),
    ('validated', 'validated'),
    ('refused', 'refused'),
    ('archived', 'archived'),
]


class ReportFilter(filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(choices=states_report)

    class Meta:
        model = Report
        fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']


# Report Model View
class ReportView(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReportFilter
    lookup_field = 'rid'
    filter_fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']
    filterset_fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']
    search_fields = ['declaration__did', 'title', 'service__uid', 'status', 'created_on', 'modified_at', 'validated_at']
    ordering_fields = ['declaration', 'title', 'service', 'status', 'created_on', 'modified_at', 'validated_at']


# ReportRejection Model View
class ReportRejectionView(viewsets.ModelViewSet):
    queryset = ReportRejection.objects.all()
    serializer_class = ReportRejectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'rrid'
    filter_fields = ['maire', 'report', 'created_on']
    filterset_fields = ['maire', 'report', 'created_on']
    search_fields = ['maire__uid', 'report__rid', 'created_on']
    ordering_fields = ['maire', 'report', 'created_on']


# ReportComplementDemand Model View
class ReportComplementDemandView(viewsets.ModelViewSet):
    queryset = ReportComplementDemand.objects.all()
    serializer_class = ReportComplementDemandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'rcid'
    filter_fields = ['maire', 'report', 'created_on']
    filterset_fields = ['maire', 'report', 'created_on']
    search_fields = ['maire__uid', 'report__rid', 'created_on']
    ordering_fields = ['maire', 'report', 'created_on']


class AnnounceFilter(filters.FilterSet):
    start_at_greater = django_filters.DateTimeFilter(field_name='start_at', lookup_expr='gte')
    start_at_less = django_filters.DateTimeFilter(field_name='start_at', lookup_expr='lte')
    end_at_greater = django_filters.DateTimeFilter(field_name='end_at', lookup_expr="gte")
    end_at_less = django_filters.DateTimeFilter(field_name='end_at', lookup_expr="lte")

    class Meta:
        model = Announce
        fields = ['title', 'status', 'service', 'created_on', 'start_at_greater', 'start_at_less',
                  'end_at_greater', 'end_at_less']


# Announce Model View
class AnnounceView(viewsets.ModelViewSet):
    queryset = Announce.objects.all()
    serializer_class = AnnounceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AnnounceFilter
    search_fields = ['title', 'status', 'service__uid', 'created_on', 'start_at', 'end_at']
    ordering_fields = ['title', 'status', 'service', 'created_on', 'start_at', 'end_at']


# Announce Model View
class AnnounceNestedView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Announce.objects.all()
    serializer_class = AnnounceNestedSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AnnounceFilter
    filter_fields = ['title', 'status', 'service', 'created_on', 'start_at', 'end_at']
    search_fields = ['title', 'status', 'service__uid', 'created_on', 'start_at', 'end_at']
    ordering_fields = ['title', 'status', 'service', 'created_on', 'start_at', 'end_at']


# Confirmation email view
class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        query_email = EmailConfirmation.objects.all_valid()
        query_email = query_email.select_related("email_address__user")
        return

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
                try:
                    email_confirmation = queryset.get(key=key.lower())
                except EmailConfirmation.DoesNotExist:
                    return HttpResponseRedirect('http://13.92.195.8/login/')  # in case of failure
        return email_confirmation

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect('http://13.92.195.8/login')  # login page redirection


# Announce Complement Demand View
class AnnounceComplementDemandView(viewsets.ModelViewSet):
    queryset = AnnounceComplementDemand.objects.all()
    serializer_class = AnnounceComplementDemandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
    filterset_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
    search_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
    ordering_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
