# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class BankServices(models.Model):
    bank_service_id = models.AutoField(primary_key=True)
    title = models.CharField(blank=True, null=True)
    button_text = models.CharField(blank=True, null=True)
    short_description = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    img = models.CharField(blank=True, null=True)
    order_img = models.CharField(blank=True, null=True)
    service_status = models.CharField(max_length=20, default='действует')  # This field type is a guess.


class Requests(models.Model):
    request_id = models.AutoField(primary_key=True)
    request_status = models.CharField(max_length=20, default='черновик')  # This field type is a guess.
    creation_date = models.DateTimeField(blank=True, null=True)
    formation_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    admin = models.ForeignKey('Users', models.DO_NOTHING, related_name='requests_admin_set', blank=True, null=True)


class RequestsServices(models.Model):
    bank_service_id = models.ForeignKey('BankServices', models.DO_NOTHING)  # The composite primary key (bank_service_id, request_id) found, that is not supported. The first column is selected.
    request_id = models.ForeignKey('Requests', models.DO_NOTHING)
    bill = models.CharField(blank=True, null=True, max_length=100)
    rs_id = models.AutoField(primary_key=True)


    class Meta:
        unique_together = (('bank_service_id', 'request_id'),)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    surname = models.CharField(blank=True, null=True)
    password = models.CharField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True)
    admin_flag = models.BooleanField(blank=True, null=True)

