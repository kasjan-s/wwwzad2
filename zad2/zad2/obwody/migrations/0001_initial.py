# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gmina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazwa', models.CharField(max_length=200)),
                ('aktualizacja', models.DateTimeField(verbose_name=b'Ostatnia aktualizacja')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Obwod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazwa', models.CharField(max_length=300)),
                ('karty', models.IntegerField(default=0)),
                ('wyborcy', models.IntegerField(default=0)),
                ('gmina', models.ForeignKey(to='obwody.Gmina')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
