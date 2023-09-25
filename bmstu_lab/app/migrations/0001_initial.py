# Generated by Django 4.2.4 on 2023-09-24 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankServices',
            fields=[
                ('bank_service_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, null=True)),
                ('button_text', models.CharField(blank=True, null=True)),
                ('short_description', models.CharField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('img', models.CharField(blank=True, null=True)),
                ('order_img', models.CharField(blank=True, null=True)),
                ('service_status', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'bank_services',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_status', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateField(blank=True, null=True)),
                ('formation_date', models.DateField(blank=True, null=True)),
                ('completion_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'requests',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, null=True)),
                ('surname', models.CharField(blank=True, null=True)),
                ('password', models.CharField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RequestsServices',
            fields=[
                ('request_service', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.requests')),
                ('request_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'requests_services',
                'managed': False,
            },
        ),
    ]
