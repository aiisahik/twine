# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 21:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'F', max_length=10)),
                ('gender_preference', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'M', max_length=10)),
            ],
        ),
    ]