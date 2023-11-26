# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

class NewUserManager(UserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('У пользователя должен быть логин!')
        
        user: Users = self.model(login=login, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user

class BankServices(models.Model):
    bank_service_id = models.AutoField(primary_key=True)
    title = models.CharField(blank=True, null=True)
    button_text = models.CharField(blank=True, null=True)
    short_description = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    img = models.CharField(blank=True, null=True)
    order_img = models.CharField(blank=True, null=True)
    service_status = models.CharField(max_length=20, default='действует')  


class Requests(models.Model):
    request_id = models.AutoField(primary_key=True)
    request_status = models.CharField(max_length=20, default='черновик')
    creation_date = models.DateTimeField(blank=True, null=True)
    formation_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    admin = models.ForeignKey('Users', models.DO_NOTHING, related_name='requests_admin_set', blank=True, null=True)


class RequestsServices(models.Model):
    bank_service_id = models.ForeignKey('BankServices', models.DO_NOTHING) 
    request_id = models.ForeignKey('Requests', models.DO_NOTHING)
    bill = models.CharField(blank=True, null=True, max_length=100)
    rs_id = models.AutoField(primary_key=True)


    class Meta:
        unique_together = (('bank_service_id', 'request_id'),)


class Users(AbstractBaseUser):
    objects = NewUserManager()

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    surname = models.CharField(blank=True, null=True)
    login = models.CharField(max_length=255, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    phone_number = models.CharField(blank=True, null=True)
    admin_flag = models.BooleanField(blank=True, null=True)
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    USERNAME_FIELD = 'login'

# class Users(AbstractBaseUser):
#     objects = NewUserManager()

#     user_id = models.AutoField(primary_key=True)
#     Userlogin = models.CharField(max_length=255, unique=True, verbose_name="Логин")
#     password = models.CharField(max_length=255, verbose_name="Пароль")
#     admin_pass = models.BooleanField(blank=True, null=True, default=False)
#     is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
#     is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    
#     USERNAME_FIELD = 'Userlogin'