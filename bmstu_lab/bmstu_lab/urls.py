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



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/check/', check, name='check'),

    path(r'services/search/', search_services),
    path(r'services/<int:service_id>/', get_service),
    path(r'services/<int:service_id>/add_to_request/', add_service_to_request),

    path(r'requests/', search_requests),
    path(r'requests/draft/', get_draft_request),
    path(r'requests/<int:request_id>/delete/', delete_request),
    path(r'requests/<int:request_id>/delete_service/<int:service_id>/', delete_servce_from_request),
    path(r'requests/update_status_user/', update_request_status_user),

    path(r'requests/<int:request_id>/rating/', rating),
]


