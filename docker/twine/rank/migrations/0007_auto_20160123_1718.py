# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20160119_0607'),
        ('matches', '0006_auto_20160119_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='playerLeft',
            field=models.ForeignKey(related_query_name=b'playerLeft', related_name='playersLeft', blank=True, to='account.Profile', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='playerRight',
            field=models.ForeignKey(related_query_name=b'playerRight', related_name='playersRight', blank=True, to='account.Profile', null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(related_query_name=b'loser', related_name='losers', blank=True, to='account.Profile', null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(related_query_name=b'winner', related_name='winners', blank=True, to='account.Profile', null=True),
        ),
    ]
