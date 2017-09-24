# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0005_auto_20160511_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='TingUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(default=b'Male', max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'Other', b'Other')])),
                ('birthday', models.DateTimeField(default=None, null=True, blank=True)),
                ('location', models.CharField(max_length=50, blank=True)),
                ('last_used', models.DateTimeField(default=None, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
