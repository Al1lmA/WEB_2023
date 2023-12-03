from django.contrib import admin

from . import models

admin.site.register(models.BankServices)
admin.site.register(models.Requests)
admin.site.register(models.RequestsServices)
admin.site.register(models.CustomUser)