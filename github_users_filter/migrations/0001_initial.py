# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-09 07:04
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('name', models.TextField()),
                ('avatar_url', models.URLField(blank=True, null=True)),
                ('company', models.TextField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('followers', models.IntegerField()),
                ('public_repos', models.IntegerField()),
                ('location', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SearchApiCallLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('for_date', models.DateField()),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
