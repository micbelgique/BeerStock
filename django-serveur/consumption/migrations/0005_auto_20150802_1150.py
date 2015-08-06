# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('consumption', '0004_auto_20150802_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='record',
            name='valve',
            field=models.ForeignKey(null=True, to='consumption.Valve'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rfid_uid_0',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='rfid_uid_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='rfid_uid_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='rfid_uid_3',
            field=models.IntegerField(default=0),
        ),
    ]
