# Generated by Django 4.2.6 on 2023-12-02 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 2, 12, 53, 2, 960874, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
