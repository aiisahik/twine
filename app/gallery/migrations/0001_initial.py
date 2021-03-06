# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-05 04:22
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0007_auto_20170905_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(db_index=True, default=datetime.datetime(1900, 1, 1, 0, 0, tzinfo=utc))),
                ('end_date', models.DateTimeField(db_index=True, default=datetime.datetime(3000, 1, 1, 0, 0, tzinfo=utc))),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('data', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
                ('json_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_galleries', to='account.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('delete_date', models.DateTimeField(blank=True, null=True)),
                ('delete_reason', models.CharField(choices=[('user_remove', 'User Removed'), ('offensive', 'Offensive'), ('nudity', 'Nudity'), ('fake', 'Fake')], default='user_removed', max_length=20)),
                ('original_filename', models.CharField(blank=True, max_length=300, null=True)),
                ('path', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.PositiveSmallIntegerField(default=5)),
                ('caption', models.CharField(blank=True, max_length=1000, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('deleter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deleted_photos', to='account.Profile')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='gallery.Gallery')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_photos', to='account.Profile')),
            ],
            options={
                'ordering': ['order', '-create_date'],
            },
        ),
        migrations.AlterIndexTogether(
            name='gallery',
            index_together=set([('start_date', 'end_date')]),
        ),
    ]
