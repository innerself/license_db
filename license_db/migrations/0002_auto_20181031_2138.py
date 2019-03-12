# Generated by Django 2.1.2 on 2018-10-31 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportLicense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('expires', models.DateField(default=datetime.date(2019, 10, 31))),
                ('comment', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='license',
            name='expires',
            field=models.DateField(default=datetime.date(2019, 10, 31), verbose_name='expires'),
        ),
    ]