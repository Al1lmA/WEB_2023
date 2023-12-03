import random

from django.core.management.base import BaseCommand
from bank_services.models import *
from .utils import random_date, random_timedelta


def add_cities():
    BankServices(
        title="ДБО",
        text="Дистанционное банковское обслуживание (ДБО) — это предоставление клиентам банка с помощью инновационных технологий услуги удаленного доступа для совершения различных операций.",
        status=1,
        price=800,
    ).save()

    BankServices(
        title="Эквайринг",
        text="Возможность торгового предприятия принимать безналичную оплату товаров и услуг пластиковыми картами.",
        status=1,
        price=1500,
    ).save()

    BankServices(
        title="Зарплатный проект",
        text="Под зарплатным проектом понимается банковская услуга, целью предоставления которой становится автоматизация перечисления зарплаты персонала на пластиковые карточки сотрудников.",
        status=1,
        price=1000,
    ).save()


    print("Услуги добавлены")


def add_vacancies():
    users = CustomUser.objects.filter(is_moderator=False)
    if len(users) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    fines = BankServices.objects.all()

    for _ in range(30):
        breach = BankServices.objects.create()
        breach.name = "Request №" + str(breach.pk)
        breach.status = random.randint(2, 5)

        if breach.status in [3, 4]:
            breach.closed_date = random_date()
            breach.formated_date = breach.closed_date - random_timedelta()
            breach.created_date = breach.formated_date - random_timedelta()
        else:
            breach.formated_date = random_date()
            breach.created_date = breach.formated_date - random_timedelta()

        breach.user = random.choice(users)

        for i in range(random.randint(1, 3)):
            try:
                conf = RequestsServices.objects.create()
                conf.breach = breach
                conf.fine = random.choice(fines)
                conf.save()
            except:
                print("e")

        breach.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # management.call_command("clean_db")

        add_cities()
        add_vacancies()










