"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from api import views
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse
from api.views import ConfirmEmailView, DocumentView, DocumentDetailView, UserStatisticsView, DeclarationStatisticsView, AnnounceStatisticsView, BeamsAuthView, PusherAuthView, DeclarationHomeView, NotificationCleanView, FeedbackCreateView, FeedbackListView, ToCSVView


def empty_view(request):
    return HttpResponse('')


# admin rest api routes
router = routers.DefaultRouter()
router.register(r'users', views.UserView)
router.register(r'declarations_types', views.DeclarationTypeView)
router.register(r'declarations', views.DeclarationView)
router.register(r'declarations_rejection', views.DeclarationRejectionView)
router.register(r'declarations_complement_demand', views.DeclarationComplementDemandView)
router.register(r'reports', views.ReportView)
router.register(r'reports_rejection', views.ReportRejectionView)
router.register(r'reports_complement_demand', views.ReportComplementDemandView)
router.register(r'announces', views.AnnounceView)
router.register(r'announces_complement_demand', views.AnnounceComplementDemandView)
router.register(r'announce_nested', views.AnnounceNestedView)
router.register(r'declaration_nested', views.DeclarationNestedView)
router.register(r'notifications', views.NotificationView)
router.register(r'city', views.CityInfoView, basename='city_infos')


schema_view = get_schema_view(
    openapi.Info(
        title="Madina-tic API",
        default_version='v1',
        description="""
      Madina-tic Project api docs.
      """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@madina-tic.dz"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/home-declarations/', DeclarationHomeView.as_view(), name='home view'),
    path('api/documents/', DocumentView.as_view(), name='documents'),
    re_path(r'api/documents/(?P<pk>[0-9a-f-]+)', DocumentDetailView.as_view(), name='document'),
    path('api/users-statistics/', UserStatisticsView.as_view(), name='Users_Statistics'),
    path('api/declarations-statistics/', DeclarationStatisticsView.as_view(), name='Declarations_Statistics'),
    path('api/announces-statistics/', AnnounceStatisticsView.as_view(), name='Announces_Statistics'),
    path('api/notification-clean/', NotificationCleanView.as_view(), name='Notification_Clean'),
    path('api/create-feedbacks/', FeedbackCreateView.as_view(), name="feedback_create"),
    path('api/list-feedbacks/', FeedbackListView.as_view(), name="feedback_list"),
    # Beams
    path('api/beams_auth/', BeamsAuthView.as_view(), name='beams_auth'),
    # Pusher
    path('api/pusher/auth', PusherAuthView.as_view() , name='pusher_auth'),
    # rest auth using token routes
    url(r'api/', include('rest_auth.urls')),
    url(r'api/registration/', include('rest_auth.registration.urls')),
    re_path(r'auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_,:&]+)/$', ConfirmEmailView.as_view(),
            name='account_confirm_email'),
    # docs routes
    url(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('account/reset-password/confirm/<uidb64>/<token>/', empty_view, name='password_reset_confirm'),
    # pandas routes
    path('api/download-csv-file/', ToCSVView.as_view(), name='download-csv-file'),
]
