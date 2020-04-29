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
from django.urls import path, include
from django.conf.urls import url
from api import views
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse

def empty_view(request):
    return HttpResponse('')

# admin rest api routes
router = routers.DefaultRouter()
router.register(r'users', views.UserView)

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
    # rest auth using token routes
    url(r'api/', include('rest_auth.urls')),
    url(r'api/registration/', include('rest_auth.registration.urls')),
    url(r'api/userinstance/', views.userInstance, name='user'),
    # docs routes
   	url(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   	url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('account/reset-password/confirm/<uidb64>/<token>/', empty_view, name='password_reset_confirm'),
]
