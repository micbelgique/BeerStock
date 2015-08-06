# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumption', '0003_record_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rfid_uid_0',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='rfid_uid_1',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='rfid_uid_2',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='rfid_uid_3',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
