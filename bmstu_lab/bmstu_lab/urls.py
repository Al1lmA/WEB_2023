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
from django.urls import include, path
from rest_framework import routers
from bank_services.Views.BankServicesView import *
from bank_services.Views.RequestServicesView import *
from bank_services.Views.RequestsView import *
from bank_services.Views.UsersView import *

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path(r'services/', services_list_form, name='services_list_form'),
    path(r'services/<int:pk>/', services_detail, name='services_detail'),

    path(r'requests/', request_list_form, name='request_list_form'),
    path(r'requests/<int:pk>/', request_detail, name='request_detail'),
    path(r'requests/<int:pk>/end/', request_final, name='request_final'),

    path(r'r_s/<int:pk>/', r_s_details, name='r_s_details'),
]


