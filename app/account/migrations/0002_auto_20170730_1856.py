# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-30 18:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('label', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TraitIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength', models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='TraitPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength', models.PositiveSmallIntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='TraitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('label', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='max_age_preference',
            field=models.PositiveSmallIntegerField(default=99),
        ),
        migrations.AddField(
            model_name='profile',
            name='max_height_preference',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='min_age_preference',
            field=models.PositiveSmallIntegerField(default=18),
        ),
        migrations.AddField(
            model_name='profile',
            name='min_height_preference',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='traitpreference',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_profiles', to='account.Profile'),
        ),
        migrations.AddField(
            model_name='traitpreference',
            name='trait',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_traits', to='account.Trait'),
        ),
        migrations.AddField(
            model_name='traitidentity',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identity_profiles', to='account.Profile'),
        ),
        migrations.AddField(
            model_name='traitidentity',
            name='trait',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identity_traits', to='account.Trait'),
        ),
        migrations.AddField(
            model_name='trait',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trait_type', to='account.TraitType'),
        ),
    ]
