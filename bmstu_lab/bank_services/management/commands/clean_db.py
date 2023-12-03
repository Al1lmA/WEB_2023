from django.core.management.base import BaseCommand
from bank_services.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        RequestsServices.objects.all().delete()
        BankServices.objects.all().delete()
        Requests.objects.all().delete()
        # CustomUser.objects.all().delete()