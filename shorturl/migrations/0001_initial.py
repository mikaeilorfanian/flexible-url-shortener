# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 08:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortURLCombination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('combination', models.CharField(max_length=8)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('long_url', models.URLField(primary_key=True, serialize=False)),
                ('visit_count', models.IntegerField(default=0)),
                ('converted_url', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shorturl.ShortURLCombination')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]