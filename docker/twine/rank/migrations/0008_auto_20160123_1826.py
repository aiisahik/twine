# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20160119_0607'),
        ('matches', '0007_auto_20160123_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='playerLeft',
        ),
        migrations.RemoveField(
            model_name='match',
            name='playerRight',
        ),
        migrations.AddField(
            model_name='match',
            name='left',
            field=models.ForeignKey(related_query_name=b'leftProfile', related_name='leftProfiles', blank=True, to='account.Profile', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='right',
            field=models.ForeignKey(related_query_name=b'rightProfile', related_name='rightProfiles', blank=True, to='account.Profile', null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(related_query_name=b'loser', related_name='losers', blank=True, to='matches.Player', null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(related_query_name=b'winner', related_name='winners', blank=True, to='matches.Player', null=True),
        ),
    ]
