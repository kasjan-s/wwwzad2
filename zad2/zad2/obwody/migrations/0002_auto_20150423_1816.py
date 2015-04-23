# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('obwody', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gmina',
            name='aktualizacja',
        ),
        migrations.AddField(
            model_name='obwod',
            name='aktualizacja',
            field=models.DateTimeField(default=datetime.date(2015, 4, 23), verbose_name=b'Ostatnia aktualizacja'),
            preserve_default=False,
        ),
    ]
