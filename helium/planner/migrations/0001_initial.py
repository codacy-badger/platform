# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-07 01:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, default=b'', max_length=255)),
                ('room', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('credits', models.DecimalField(decimal_places=2, max_digits=4)),
                ('color', models.CharField(choices=[(b'#ac725e', b'#ac725e'), (b'#d06b64', b'#d06b64'), (b'#f83a22', b'#f83a22'), (b'#fa573c', b'#fa573c'), (b'#ff7537', b'#ff7537'), (b'#ffad46', b'#ffad46'), (b'#42d692', b'#42d692'), (b'#16a765', b'#16a765'), (b'#7bd148', b'#7bd148'), (b'#b3dc6c', b'#b3dc6c'), (b'#fad165', b'#fad165'), (b'#92e1c0', b'#92e1c0'), (b'#9fe1e7', b'#9fe1e7'), (b'#9fc6e7', b'#9fc6e7'), (b'#4986e7', b'#4986e7'), (b'#9a9cff', b'#9a9cff'), (b'#b99aff', b'#b99aff'), (b'#c2c2c2', b'#c2c2c2'), (b'#cabdbf', b'#cabdbf'), (b'#cca6ac', b'#cca6ac'), (b'#f691b2', b'#f691b2'), (b'#cd74e6', b'#cd74e6'), (b'#a47ae2', b'#a47ae2'), (b'#555', b'#555')], default=b'#4986e7', max_length=7)),
                ('website', models.URLField(blank=True, max_length=3000, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('current_grade', models.DecimalField(decimal_places=4, default=-1, max_digits=7)),
                ('trend', models.FloatField(blank=True, default=None, null=True)),
                ('private_slug', models.SlugField(blank=True, null=True, unique=True)),
                ('teacher_name', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('teacher_email', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('days_of_week', models.CharField(default=b'0000000', max_length=7)),
                ('sun_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('sun_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('mon_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('mon_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('tue_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('tue_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('wed_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('wed_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('thu_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('thu_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('fri_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('fri_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('sat_start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('sat_end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('days_of_week_alt', models.CharField(default=b'0000000', max_length=7)),
                ('sun_start_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('sun_end_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('mon_start_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('mon_end_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('tue_start_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('tue_end_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('wed_start_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('wed_end_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('thu_start_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('thu_end_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('fri_start_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('fri_end_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('sat_start_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
                ('sat_end_time_alt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, default=b'', max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('shown_on_calendar', models.BooleanField(default=True)),
                ('average_grade', models.DecimalField(decimal_places=4, default=-1, max_digits=7)),
                ('trend', models.FloatField(blank=True, default=None, null=True)),
                ('private_slug', models.SlugField(blank=True, null=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='course',
            name='course_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='planner.CourseGroup'),
        ),
    ]
