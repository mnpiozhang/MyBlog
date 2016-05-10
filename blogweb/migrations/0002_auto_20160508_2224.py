# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagname', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='tag',
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='blogweb.TagInfo', blank=True),
        ),
    ]
