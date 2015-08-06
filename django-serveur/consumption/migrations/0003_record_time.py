# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('consumption', '0002_auto_20150801_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='time',
            field=models.DateTimeField(default=datetime.now),
            preserve_default=False,
        ),
    ]
