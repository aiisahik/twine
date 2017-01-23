# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='winner_mu',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_sigma',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
