# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-27 20:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170827_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(db_index=True, default=datetime.datetime(1900, 1, 1, 0, 0, tzinfo=utc))),
                ('end_date', models.DateTimeField(db_index=True, default=datetime.datetime(3000, 1, 1, 0, 0, tzinfo=utc))),
                ('membership_type', models.CharField(choices=[(b'admin', b'Administrator'), (b'founder', b'Founder'), (b'member', b'Member')], default=b'member', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterIndexTogether(
            name='adminmembership',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='adminmembership',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='adminmembership',
            name='admin_group',
        ),
        migrations.RemoveField(
            model_name='adminmembership',
            name='inviter',
        ),
        migrations.AlterIndexTogether(
            name='regularmembership',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='regularmembership',
            name='group',
        ),
        migrations.RemoveField(
            model_name='regularmembership',
            name='inviter',
        ),
        migrations.RemoveField(
            model_name='regularmembership',
            name='member',
        ),
        migrations.RemoveField(
            model_name='group',
            name='admins',
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', through='account.GroupMembership', to='account.Profile'),
        ),
        migrations.DeleteModel(
            name='AdminMembership',
        ),
        migrations.DeleteModel(
            name='RegularMembership',
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_memberships', to='account.Group'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='inviter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inviter_memberships', to='account.Profile'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='account.Profile'),
        ),
        migrations.AlterIndexTogether(
            name='groupmembership',
            index_together=set([('start_date', 'end_date')]),
        ),
    ]
