# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Done',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('done_id', models.IntegerField(default=None)),
                ('owner', models.CharField(max_length=64)),
                ('team_short_name', models.CharField(max_length=64)),
                ('done_date', models.DateField(default=None)),
                ('last_updated', models.DateTimeField(default=None)),
                ('is_goal', models.BooleanField(default=None)),
                ('is_completed', models.BooleanField(default=None)),
                ('raw_text', models.TextField(default=None)),
                ('markedup_text', models.TextField(default=None)),
            ],
        ),
    ]
