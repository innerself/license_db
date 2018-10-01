# Generated by Django 2.1 on 2018-10-01 06:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='quantity')),
                ('expires', models.DateField(default=datetime.date(2019, 10, 1), verbose_name='expires')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='comment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
        ),
        migrations.CreateModel(
            name='LicenseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='LicenseLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='location')),
            ],
        ),
        migrations.CreateModel(
            name='LicenseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='type')),
            ],
        ),
        migrations.AddField(
            model_name='license',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='license_db.LicenseCategory'),
        ),
        migrations.AddField(
            model_name='license',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='license_db.LicenseLocation'),
        ),
        migrations.AddField(
            model_name='license',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='license_db.LicenseType'),
        ),
    ]