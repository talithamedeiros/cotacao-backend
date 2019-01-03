# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2019-01-03 00:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nome', models.CharField(blank=True, max_length=45, null=True)),
                ('sobrenome', models.CharField(blank=True, max_length=45, null=True)),
                ('nomecompleto', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(default='', max_length=75, unique=True, verbose_name='email')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(blank=True, max_length=45, null=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
