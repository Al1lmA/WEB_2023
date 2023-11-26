"""
URL configuration for bmstu_lab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework import routers
from bank_services.Views.BankServicesView import *
from bank_services.Views.RequestServicesView import *
from bank_services.Views.RequestsView import *
from bank_services.Views.UsersView import *

from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),

    path(r'services/', Services_View.as_view(), name='services_list_form'),
    path(r'services/<int:pk>/', Service_View.as_view(), name='services_detail'),

    path(r'requests/', Requests_View.as_view(), name='request_list_form'),
    path(r'requests/<int:pk>/', Request_View.as_view(), name='request_detail'),

    path(r'r_s/<int:pk>/', Requests_Services_View.as_view(), name='r_s_details'),
]


