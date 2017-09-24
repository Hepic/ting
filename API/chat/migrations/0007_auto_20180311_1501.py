# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_tinguser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinguser',
            name='location',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
