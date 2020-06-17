from rest_framework import viewsets, generics, status, mixins
from .helpers import modify_input_for_multiple_files
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseRedirect
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .pagination import CustomPagination, NotificationCustomPagination, HomeDeclarationCustomPagination
from django_filters import rest_framework as filters
import django_filters
from django.http import Http404
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from .permissions import ReadOnly
from django.conf import settings
import pusher
from rest_framework.decorators import api_view
import json
# User Model View for admin access only
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'uid'
    filter_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id', 'is_french','role',
                     'is_approved', 'is_active', 'notif_seen', 'is_superuser', 'created_on']
    filterset_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id','is_french', 'role',
                        'is_approved', 'is_active', 'notif_seen', 'is_superuser', 'created_on']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id','is_french', 'role',
                     'is_approved', 'is_active', 'notif_seen', 'is_superuser', 'created_on']
    ordering_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'national_id','is_french', 'role',
                       'is_approved', 'is_active', 'notif_seen', 'is_superuser', 'created_on']
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
    has_parent = django_filters.BooleanFilter(field_name="parent_declaration", lookup_expr='isnull', exclude=True)
    class Meta:
        model = Declaration
        fields = ['title', 'address', 'geo_cord', 'parent_declaration', 'citizen', 'service', 'priority', 'status', 'dtype', 'created_on',
                  'modified_at', 'validated_at']


# Declaration Model View
class DeclarationView(viewsets.ModelViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
    permission_classes = [IsAuthenticated|ReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DeclarationFilter
    lookup_field = 'did'
    filter_fields = ['title',  'address', 'geo_cord', 'parent_declaration', 'citizen', 'service', 'priority', 'status', 'dtype', 'created_on',
                     'modified_at', 'validated_at']
    filterset_fields = ['title', 'address', 'geo_cord', 'parent_declaration', 'citizen', 'service', 'priority', 'status', 'dtype',
                        'created_on', 'modified_at', 'validated_at']
    search_fields = ['title', 'address', 'geo_cord', 'parent_declaration__did', 'parent_declaration__title', 'citizen__uid', 'citizen__first_name', 'citizen__last_name',
                     'service__uid', 'priority', 'status', 'dtype__name', 'created_on', 'modified_at', 'validated_at']
    ordering_fields = ['title', 'address', 'geo_cord', 'parent_declaration', 'citizen', 'service', 'priority', 'status', 'dtype',
                       'created_on', 'modified_at', 'validated_at']


# Declaration Nested Model View
class DeclarationNestedView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationNestedSerializer
    permission_classes = [IsAuthenticated|ReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DeclarationFilter
    lookup_field = 'did'
    filter_fields = ['title', 'address', 'geo_cord', 'citizen', 'parent_declaration', 'service', 'priority', 'status', 'dtype', 'created_on',
                     'modified_at', 'validated_at']
    filterset_fields = ['title', 'address', 'geo_cord', 'citizen',  'parent_declaration', 'service', 'priority', 'status', 'dtype',
                        'created_on', 'modified_at', 'validated_at']
    search_fields = ['title', 'address', 'geo_cord', 'citizen__uid', 'citizen__first_name', 'citizen__last_name', 'parent_declaration',
                     'service__uid', 'priority', 'status', 'dtype__name', 'created_on', 'modified_at', 'validated_at']
    ordering_fields = ['title', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype', 'parent_declaration',
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
        report = request.data.get('report')
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
    permission_classes = [IsAuthenticated|ReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AnnounceFilter
    search_fields = ['title', 'status', 'service__uid', 'created_on', 'start_at', 'end_at']
    ordering_fields = ['title', 'status', 'service', 'created_on', 'start_at', 'end_at']

# Announce Model View
class AnnounceNestedView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Announce.objects.all()
    serializer_class = AnnounceNestedSerializer
    permission_classes = [IsAuthenticated|ReadOnly]
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
                    return HttpResponseRedirect('https://madina-tic.ml/login')  # in case of failure
        return email_confirmation

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect('https://madina-tic.ml/login')  # login page redirection


# Announce Complement Demand View
class AnnounceComplementDemandView(viewsets.ModelViewSet):
    queryset = AnnounceComplementDemand.objects.all()
    serializer_class = AnnounceComplementDemandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
    filterset_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
    search_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']
    ordering_fields = ['acid', 'maire', 'announce', 'reason', 'created_on']


class UserStatisticsView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated|ReadOnly]

    def get(self, request, format=None):
        ''' Users Statistics '''
        all_users_count = User.objects.all().count() # all current users
        active_users_count = User.objects.filter(is_active=True).exclude(role='Admin').count() #  active users exclude Admins
        all_citoyens_count = User.objects.filter(role='Client').count() # citoyens 
        citoyens_approved_count = User.objects.filter(role='Client').filter(is_approved=True).count() # citoyen approved
        citoyens_non_approved_count = User.objects.filter(role='Client').filter(is_approved=False).count() # citoyen non approved
        current_services_count = User.objects.filter(role='Service').count() # services

        data = {
            'all_users': all_users_count,
            'active_users': active_users_count,
            'citoyens': all_citoyens_count, 
            'citoyens_approved': citoyens_approved_count,
            'citoyens_non_approved': citoyens_non_approved_count,
            'current_services':  current_services_count,
            }

        return Response(data)

class DeclarationStatisticsView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated|ReadOnly]

    def get(self, request, format=None):
        ''' Users Statistics '''
        critical = dict()
        important = dict()
        normal = dict()
        low = dict()
        status = ["validated", "refused", "under_treatment", "treated"]
        for statu in status:
            critical[statu] = Declaration.objects.filter(priority=1).filter(status=statu).count()
            important[statu] = Declaration.objects.filter(priority=2).filter(status=statu).count()
            normal[statu] = Declaration.objects.filter(priority=3).filter(status=statu).count()
            low[statu] = Declaration.objects.filter(priority=4).filter(status=statu).count()
            
        data = {
            'critical': critical,
            'important': important,
            'normal': normal,
            'low': low
        }
        return Response(data)

utc = pytz.UTC
class AnnounceStatisticsView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated|ReadOnly]
    
    def get(self, request, format=None):
        ''' Announce Statistics '''
        current_date = utc.localize(datetime.datetime.now())
        print(current_date)
        all_announces_count = Announce.objects.all().count()
        published_announces_count = Announce.objects.filter(status='published').count()
        removed_announces_count = Announce.objects.filter(status='removed').count()
        expired_announces_count = Announce.objects.filter(end_at__lt=current_date).count()
        active_announces_count = Announce.objects.filter(end_at__gte=current_date).count()

        data = {
            'all_announces_count': all_announces_count,
            'published': published_announces_count,
            'removed': removed_announces_count,
            'expired': expired_announces_count,
            'active': active_announces_count
        }

        return Response(data)


# Pusher Beams AUTH
class BeamsAuthView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        from pusher_push_notifications import PushNotifications
        push_client = PushNotifications(
            instance_id='65b0754a-0713-4b71-bc41-4d2abae63fc6',
            secret_key='E1067A08CDB1C1F6DD92AF5CAFF4CA9C8F5B50740B6865B3CFACFC282A202A10',
            )
        user_id = str(request.user.uid)
        beams_token = push_client.generate_token(user_id)      
        # content = {
        #     'user': request.user.first_name,
        #     'user_id': request.user.uid,
        #     'beams_token': beams_token,
        #     'auth': request.auth,
        # }
        return Response(beams_token)

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['nid', 'title', 'body', 'citoyen', 'maire', 'service', 'created_on']
    filterset_fields = ['nid', 'title', 'body', 'citoyen', 'maire', 'service', 'created_on']
    search_fields = ['nid', 'title', 'body', 'citoyen', 'maire', 'service', 'created_on']
    ordering_fields = ['nid', 'title', 'body', 'citoyen', 'maire', 'service', 'created_on']
    authentication_classes = []
    permission_classes = []
    pagination_class = NotificationCustomPagination


class PusherAuthView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    pusher_client = pusher.Pusher(
        app_id= settings.PUSHER_APP_ID,
        key= settings.PUSHER_KEY,
        secret= settings.PUSHER_SECRET,
        cluster= settings.PUSHER_CLUSTER
            )

    def get(self, request, format=None):
        channel_name = self.request.query_params.get('channel_name')
        socket_id = self.request.query_params.get('socket_id')

        auth = self.pusher_client.authenticate(
            channel = channel_name,
            socket_id = socket_id
            )
        
        return Response(auth)
    
    def post(self, request):
        channel_name = self.request.data['channel_name']
        socket_id = self.request.data['socket_id']

        auth = self.pusher_client.authenticate(
            channel = channel_name,
            socket_id = socket_id
            )
        
        return Response(auth)


class DeclarationHomeView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    serializer_class = DeclarationSerializer
    permission_classes = [IsAuthenticated|ReadOnly]
    pagination_class = HomeDeclarationCustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'did'
    filter_fields = ['title', 'address', 'geo_cord', 'citizen', 'parent_declaration', 'service', 'priority', 'status', 'dtype', 'created_on',
                     'modified_at', 'validated_at']
    filterset_fields = ['title', 'address', 'geo_cord', 'citizen',  'parent_declaration', 'service', 'priority', 'status', 'dtype',
                        'created_on', 'modified_at', 'validated_at']
    search_fields = ['title', 'address', 'geo_cord', 'citizen__uid', 'citizen__first_name', 'citizen__last_name', 'parent_declaration',
                     'service__uid', 'priority', 'status', 'dtype__name', 'created_on', 'modified_at', 'validated_at']
    ordering_fields = ['title', 'address', 'geo_cord', 'citizen', 'service', 'priority', 'status', 'dtype', 'parent_declaration',
                       'created_on', 'modified_at', 'validated_at']
    
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator
        
    def paginate_queryset(self, queryset):
         """
         Return a single page of results, or `None` if pagination is disabled.
         """
         if self.paginator is None:
             return None
         return self.paginator.paginate_queryset(queryset, self.request, view=self)
         
    def get_paginated_response(self, data):
         """
         Return a paginated style `Response` object for the given output data.
         """
         assert self.paginator is not None
         return self.paginator.get_paginated_response(data) 

    """ filter the queryset with whichever filter backend is in use """
    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    """exclude the declarations for the current user"""
    def get_queryset(self):
        if self.request.user.is_authenticated:   # check if user logged
            user = self.request.user
            instance = Declaration.objects.exclude(citizen=user)
        else:
            instance = Declaration.objects.all() # for anonyme user
        
        return instance
    
    def get(self, request):
        the_filtered_qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset( the_filtered_qs)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = DeclarationSerializer(the_filtered_qs, many=True)
        return Response(serializer.data)

# TO DO iplement recaptcha for feedback form
# crete feedback for all
class FeedbackCreateView(generics.CreateAPIView):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'fid'

# List feedbacks for admin only 
class FeedbackListView(generics.ListAPIView):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'fid'

# TO DO
class NotificationCleanView(APIView):
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset
    
    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(citoyen=user)

    def get(self, request):
        qs = self.filter_queryset(self.get_queryset())
        print(qs)
        serializer = NotificationSerializer(qs, many=True)
        return Response(serializer.data)
