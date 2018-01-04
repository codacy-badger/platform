# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-04 07:01
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import helium.common.utils.commonutils
import helium.planner.utils.attachmentutils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('attachment', models.FileField(blank=True, help_text=b'The file to be uploaded.', null=True, upload_to=helium.planner.utils.attachmentutils.get_path_for_attachment)),
                ('size', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('weight', models.DecimalField(decimal_places=2, help_text=b"A decimal weight for this category's homework (note that all weights associated with a single course cannot exceed a value of 100).", max_digits=5)),
                ('color', models.CharField(choices=[(b'#ac725e', b'#ac725e'), (b'#d06b64', b'#d06b64'), (b'#f83a22', b'#f83a22'), (b'#fa573c', b'#fa573c'), (b'#ff7537', b'#ff7537'), (b'#ffad46', b'#ffad46'), (b'#42d692', b'#42d692'), (b'#16a765', b'#16a765'), (b'#7bd148', b'#7bd148'), (b'#b3dc6c', b'#b3dc6c'), (b'#fad165', b'#fad165'), (b'#92e1c0', b'#92e1c0'), (b'#9fe1e7', b'#9fe1e7'), (b'#9fc6e7', b'#9fc6e7'), (b'#4986e7', b'#4986e7'), (b'#9a9cff', b'#9a9cff'), (b'#b99aff', b'#b99aff'), (b'#c2c2c2', b'#c2c2c2'), (b'#cabdbf', b'#cabdbf'), (b'#cca6ac', b'#cca6ac'), (b'#f691b2', b'#f691b2'), (b'#cd74e6', b'#cd74e6'), (b'#a47ae2', b'#a47ae2'), (b'#555', b'#555')], default=b'#4986e7', help_text=b'A valid hex color code choice to determine the color items will be shown on the calendar', max_length=7)),
                ('average_grade', models.DecimalField(decimal_places=4, default=-1, max_digits=7)),
                ('grade_by_weight', models.DecimalField(decimal_places=4, default=0, max_digits=7)),
                ('trend', models.FloatField(blank=True, default=None, null=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('room', models.CharField(blank=True, help_text=b'An arbitrary string.', max_length=255)),
                ('credits', models.DecimalField(decimal_places=2, help_text=b'A decimal corresponding to credit hours.', max_digits=4)),
                ('color', models.CharField(choices=[(b'#ac725e', b'#ac725e'), (b'#d06b64', b'#d06b64'), (b'#f83a22', b'#f83a22'), (b'#fa573c', b'#fa573c'), (b'#ff7537', b'#ff7537'), (b'#ffad46', b'#ffad46'), (b'#42d692', b'#42d692'), (b'#16a765', b'#16a765'), (b'#7bd148', b'#7bd148'), (b'#b3dc6c', b'#b3dc6c'), (b'#fad165', b'#fad165'), (b'#92e1c0', b'#92e1c0'), (b'#9fe1e7', b'#9fe1e7'), (b'#9fc6e7', b'#9fc6e7'), (b'#4986e7', b'#4986e7'), (b'#9a9cff', b'#9a9cff'), (b'#b99aff', b'#b99aff'), (b'#c2c2c2', b'#c2c2c2'), (b'#cabdbf', b'#cabdbf'), (b'#cca6ac', b'#cca6ac'), (b'#f691b2', b'#f691b2'), (b'#cd74e6', b'#cd74e6'), (b'#a47ae2', b'#a47ae2'), (b'#555', b'#555')], default=b'#4986e7', help_text=b'A valid hex color code choice to determine the color events will be shown on the calendar', max_length=7)),
                ('website', models.URLField(blank=True, help_text=b'A valid URL.', max_length=3000, null=True)),
                ('is_online', models.BooleanField(default=False, help_text=b'Whether or not the course is online (and thus may have times associated with it)')),
                ('current_grade', models.DecimalField(decimal_places=4, default=-1, max_digits=7)),
                ('trend', models.FloatField(blank=True, default=None, null=True)),
                ('private_slug', models.SlugField(blank=True, null=True, unique=True)),
                ('teacher_name', models.CharField(blank=True, help_text=b'A display name for the teacher.', max_length=255)),
                ('teacher_email', models.EmailField(blank=True, default=None, help_text=b'A valid email address.', max_length=254, null=True)),
                ('start_date', models.DateField(help_text=b'An ISO-8601 date.')),
                ('end_date', models.DateField(help_text=b'An ISO-8601 date.')),
                ('days_of_week', models.CharField(default=b'0000000', help_text=b'Seven booleans (0 or 1) indicating which days of the week the course is on (week starts on Sunday).', max_length=7, validators=[django.core.validators.RegexValidator(b'^[0-1]+$', b'Seven booleans (0 or 1) indicating which days of the week the course is on (week starts on Sunday).', b'invalid'), django.core.validators.MinLengthValidator(7, b'Seven booleans (0 or 1) indicating which days of the week the course is on (week starts on Sunday).')])),
                ('sun_start_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('sun_end_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('mon_start_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('mon_end_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('tue_start_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('tue_end_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('wed_start_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('wed_end_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('thu_start_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('thu_end_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('fri_start_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('fri_end_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('sat_start_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('sat_end_time', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('days_of_week_alt', models.CharField(default=b'0000000', help_text=b'Seven booleans (0 or 1) indicating which days of the week the course is on (week starts on Sunday).', max_length=7, validators=[django.core.validators.RegexValidator(b'^[0-1]+$', b'Seven booleans (0 or 1) indicating which days of the week the course is on (week starts on Sunday).', b'invalid'), django.core.validators.MinLengthValidator(7, b'Seven booleans (0 or 1) indicating which days of the week the course is on (week starts on Sunday).')])),
                ('sun_start_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('sun_end_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('mon_start_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('mon_end_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('tue_start_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('tue_end_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('wed_start_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('wed_end_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('thu_start_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('thu_end_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('fri_start_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('fri_end_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('sat_start_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
                ('sat_end_time_alt', models.TimeField(default=datetime.time(12, 0), help_text=b'An ISO-8601 time.')),
            ],
            options={
                'ordering': ('start_date',),
            },
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('start_date', models.DateField(help_text=b'An ISO-8601 date.')),
                ('end_date', models.DateField(help_text=b'An ISO-8601 date.')),
                ('shown_on_calendar', models.BooleanField(default=True, help_text=b'Whether or not items should be shown on the calendar.')),
                ('average_grade', models.DecimalField(decimal_places=4, default=-1, max_digits=7)),
                ('trend', models.FloatField(blank=True, default=None, null=True)),
                ('private_slug', models.SlugField(blank=True, null=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('start_date',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('all_day', models.BooleanField(default=False, help_text=b'Whether or not it is an all day event.')),
                ('show_end_time', models.BooleanField(default=False, help_text=b'Whether or not the end time should be shown on the calendar.')),
                ('start', models.DateTimeField(help_text=b'An ISO-8601 date.')),
                ('end', models.DateTimeField(help_text=b'An ISO-8601 date.')),
                ('priority', models.PositiveIntegerField(default=50, help_text=b'A priority integer between 0 and 100.')),
                ('comments', models.TextField(blank=True, help_text=b'An arbitrary string (which may contain HTML formatting).')),
                ('calendar_item_type', models.PositiveIntegerField(choices=[(0, b'Event'), (1, b'Homework'), (2, b'Class')], default=0, help_text=b'A valid calendar item choice.')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('start',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('all_day', models.BooleanField(default=False, help_text=b'Whether or not it is an all day event.')),
                ('show_end_time', models.BooleanField(default=False, help_text=b'Whether or not the end time should be shown on the calendar.')),
                ('start', models.DateTimeField(help_text=b'An ISO-8601 date.')),
                ('end', models.DateTimeField(help_text=b'An ISO-8601 date.')),
                ('priority', models.PositiveIntegerField(default=50, help_text=b'A priority integer between 0 and 100.')),
                ('comments', models.TextField(blank=True, help_text=b'An arbitrary string (which may contain HTML formatting).')),
                ('current_grade', models.CharField(help_text=b'The current grade in fraction form (ex. 25/30).', max_length=255, validators=[helium.common.utils.commonutils.fraction_validator])),
                ('completed', models.BooleanField(default=False, help_text=b'Whether or not the homework has been completed.')),
                ('calendar_item_type', models.PositiveIntegerField(choices=[(0, b'Event'), (1, b'Homework'), (2, b'Class')], default=1)),
                ('category', models.ForeignKey(blank=True, default=None, help_text=b'The category with which to associate.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homework', to='planner.Category')),
                ('course', models.ForeignKey(blank=True, help_text=b'The course with which to associate.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='homework', to='planner.Course')),
            ],
            options={
                'ordering': ('start',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('status', models.PositiveIntegerField(choices=[(0, b'Owned'), (1, b'Rented'), (2, b'Ordered'), (3, b'Shipped'), (4, b'Need'), (5, b'Received'), (6, b'To Sell')], default=0, help_text=b'A valid material status choice.')),
                ('condition', models.PositiveIntegerField(choices=[(0, b'Brand New'), (1, b'Refurbished'), (2, b'Used - Like New'), (3, b'Used - Very Good'), (4, b'Used - Good'), (5, b'Used - Acceptable'), (6, b'Used - Poor'), (7, b'Broken')], default=0, help_text=b'A valid material condition choice.')),
                ('website', models.URLField(blank=True, help_text=b'A valid URL.', max_length=3000, null=True)),
                ('price', models.CharField(blank=True, help_text=b'A price string.', max_length=255)),
                ('details', models.TextField(blank=True, help_text=b'An arbitrary string (which may contain HTML formatting).')),
                ('courses', models.ManyToManyField(blank=True, default=None, help_text=b'A list of courses with which to associate.', related_name='materials', to='planner.Course')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='MaterialGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('shown_on_calendar', models.BooleanField(default=True, help_text=b'Whether or not items should be shown on the calendar.')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, help_text=b'A display name.', max_length=255)),
                ('message', models.TextField(help_text=b'A string that will be used as the reminder message (may contain HTML formatting).')),
                ('start_of_range', models.DateTimeField(help_text=b'An ISO-8601 date.')),
                ('offset', models.PositiveIntegerField(default=30, help_text=b'The number of units (in `offset_type`) from the offset.')),
                ('offset_type', models.PositiveIntegerField(choices=[(0, b'minutes'), (1, b'hours'), (2, b'days'), (3, b'weeks')], default=0, help_text=b'A valid reminder offset type choice.')),
                ('type', models.PositiveIntegerField(choices=[(0, b'Popup'), (1, b'Email'), (2, b'Text')], default=0, help_text=b'A valid reminder type choice.')),
                ('sent', models.BooleanField(default=False)),
                ('from_admin', models.BooleanField(default=False)),
                ('event', models.ForeignKey(blank=True, help_text=b'The event with which to associate.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to='planner.Event')),
                ('homework', models.ForeignKey(blank=True, help_text=b'The homework with which to associate.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to='planner.Homework')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='material',
            name='material_group',
            field=models.ForeignKey(help_text=b'The material group with which to associate.', on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='planner.MaterialGroup'),
        ),
        migrations.AddField(
            model_name='homework',
            name='materials',
            field=models.ManyToManyField(blank=True, default=None, help_text=b'A list of materials with which to associate.', related_name='homework', to='planner.Material'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_group',
            field=models.ForeignKey(help_text=b'The course group with which to associate.', on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='planner.CourseGroup'),
        ),
        migrations.AddField(
            model_name='category',
            name='course',
            field=models.ForeignKey(help_text=b'The course with which to associate.', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='planner.Course'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='course',
            field=models.ForeignKey(blank=True, help_text=b'The course with which to associate.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='planner.Course'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='event',
            field=models.ForeignKey(blank=True, help_text=b'The event with which to associate.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='planner.Event'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='homework',
            field=models.ForeignKey(blank=True, help_text=b'The homework with which to associate.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='planner.Homework'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to=settings.AUTH_USER_MODEL),
        ),
    ]
