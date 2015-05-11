# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obwody', '0002_auto_20150423_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obwod',
            name='karty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='obwod',
            name='wyborcy',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
