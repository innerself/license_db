# Generated by Django 2.1.2 on 2019-03-12 13:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_db', '0002_auto_20181031_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importlicense',
            name='expires',
            field=models.DateField(default=datetime.date(2020, 3, 11)),
        ),
        migrations.AlterField(
            model_name='license',
            name='expires',
            field=models.DateField(default=datetime.date(2020, 3, 11), verbose_name='expires'),
        ),
    ]
