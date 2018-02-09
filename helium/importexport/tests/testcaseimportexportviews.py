import datetime
import json
import logging
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from helium.auth.tests.helpers import userhelper
from helium.feed.models import ExternalCalendar
from helium.feed.tests.helpers import externalcalendarhelper
from helium.planner.models import CourseGroup, Course, Category, MaterialGroup, Material, Event, Homework, Reminder
from helium.planner.tests.helpers import coursegrouphelper, coursehelper, categoryhelper, materialgrouphelper, \
    materialhelper, eventhelper, homeworkhelper, attachmenthelper, reminderhelper

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Helium Edu"
__version__ = '1.2.0'

logger = logging.getLogger(__name__)


class TestCaseImportExportViews(TestCase):
    def test_importexport_login_required(self):
        # GIVEN
        userhelper.given_a_user_exists()

        # WHEN
        responses = [
            self.client.get(reverse('importexport_import')),
            self.client.post(reverse('importexport_export'))
        ]

        # THEN
        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_import_success(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        with open(os.path.join(os.path.dirname(__file__), os.path.join('resources', 'sample.json'))) as fp:
            data = {
                'file[]': [fp]
            }
            self.client.post(
                reverse('importexport_import'),
                data)
        # We are intentionally uploading this file twice so that, in the case of unit tests, the key IDs do not line
        # up and the remapping is properly tested
        with open(os.path.join(os.path.dirname(__file__), os.path.join('resources', 'sample.json'))) as fp:
            data = {
                'file[]': [fp]
            }
            response = self.client.post(
                reverse('importexport_import'),
                data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_groups = CourseGroup.objects.all()
        courses = Course.objects.all()
        categories = Category.objects.all()
        material_groups = MaterialGroup.objects.all()
        materials = Material.objects.all()
        events = Event.objects.all()
        homework = Homework.objects.all()
        self.assertEqual(len(course_groups), 4)
        self.assertEqual(len(courses), 4)
        self.assertEqual(len(categories), 4)
        self.assertEqual(len(material_groups), 2)
        self.assertEqual(len(materials), 2)
        self.assertEqual(len(events), 4)
        self.assertEqual(len(homework), 4)
        coursegrouphelper.verify_course_group_matches_data(self, course_groups[2], {'average_grade': 66.6667,
                                                                                    'start_date': '2017-01-06',
                                                                                    'end_date': '2017-05-08',
                                                                                    'private_slug': None,
                                                                                    'shown_on_calendar': True,
                                                                                    'title': 'Test Course Group',
                                                                                    'trend': None,
                                                                                    'user': 1})
        coursegrouphelper.verify_course_group_matches_data(self, course_groups[3], {'average_grade': -1.0,
                                                                                    'start_date': '2017-01-06',
                                                                                    'end_date': '2017-05-08',
                                                                                    'private_slug': None,
                                                                                    'shown_on_calendar': True,
                                                                                    'title': 'Test Course Group',
                                                                                    'trend': None,
                                                                                    'user': 1})
        coursehelper.verify_course_matches_data(self, courses[2], {'title': 'Test Course', 'room': '',
                                                                   'credits': 5.0, 'color': '#4986e7',
                                                                   'website': 'http://mycourse.com', 'is_online': False,
                                                                   'current_grade': 66.6667, 'trend': None,
                                                                   'private_slug': None, 'teacher_name': 'My Teacher',
                                                                   'teacher_email': 'teacher@email.com',
                                                                   'start_date': '2017-01-06',
                                                                   'end_date': '2017-05-08',
                                                                   'days_of_week': '0000000',
                                                                   'sun_start_time': '12:00:00',
                                                                   'sun_end_time': '12:00:00',
                                                                   'mon_start_time': '12:00:00',
                                                                   'mon_end_time': '12:00:00',
                                                                   'tue_start_time': '12:00:00',
                                                                   'tue_end_time': '12:00:00',
                                                                   'wed_start_time': '12:00:00',
                                                                   'wed_end_time': '12:00:00',
                                                                   'thu_start_time': '12:00:00',
                                                                   'thu_end_time': '12:00:00',
                                                                   'fri_start_time': '12:00:00',
                                                                   'fri_end_time': '12:00:00',
                                                                   'sat_start_time': '12:00:00',
                                                                   'sat_end_time': '12:00:00',
                                                                   'days_of_week_alt': '0000000',
                                                                   'sun_start_time_alt': '12:00:00',
                                                                   'sun_end_time_alt': '12:00:00',
                                                                   'mon_start_time_alt': '12:00:00',
                                                                   'mon_end_time_alt': '12:00:00',
                                                                   'tue_start_time_alt': '12:00:00',
                                                                   'tue_end_time_alt': '12:00:00',
                                                                   'wed_start_time_alt': '12:00:00',
                                                                   'wed_end_time_alt': '12:00:00',
                                                                   'thu_start_time_alt': '12:00:00',
                                                                   'thu_end_time_alt': '12:00:00',
                                                                   'fri_start_time_alt': '12:00:00',
                                                                   'fri_end_time_alt': '12:00:00',
                                                                   'sat_start_time_alt': '12:00:00',
                                                                   'sat_end_time_alt': '12:00:00',
                                                                   'course_group': course_groups[2].pk})
        coursehelper.verify_course_matches_data(self, courses[3],
                                                {'title': 'Test Course', 'room': 'DNC 201', 'credits': 5.0,
                                                 'color': '#4986e7', 'website': 'http://mycourse.com',
                                                 'is_online': False, 'current_grade': -1.0, 'trend': None,
                                                 'private_slug': None, 'teacher_name': 'My Teacher',
                                                 'teacher_email': 'teacher@email.com',
                                                 'start_date': '2017-01-06',
                                                 'end_date': '2017-05-08', 'days_of_week': '0000000',
                                                 'sun_start_time': '12:00:00',
                                                 'sun_end_time': '12:00:00',
                                                 'mon_start_time': '12:00:00',
                                                 'mon_end_time': '12:00:00',
                                                 'tue_start_time': '12:00:00',
                                                 'tue_end_time': '12:00:00',
                                                 'wed_start_time': '12:00:00',
                                                 'wed_end_time': '12:00:00',
                                                 'thu_start_time': '12:00:00',
                                                 'thu_end_time': '12:00:00',
                                                 'fri_start_time': '12:00:00',
                                                 'fri_end_time': '12:00:00',
                                                 'sat_start_time': '12:00:00',
                                                 'sat_end_time': '12:00:00', 'days_of_week_alt': '0000000',
                                                 'sun_start_time_alt': '12:00:00',
                                                 'sun_end_time_alt': '12:00:00',
                                                 'mon_start_time_alt': '12:00:00',
                                                 'mon_end_time_alt': '12:00:00',
                                                 'tue_start_time_alt': '12:00:00',
                                                 'tue_end_time_alt': '12:00:00',
                                                 'wed_start_time_alt': '12:00:00',
                                                 'wed_end_time_alt': '12:00:00',
                                                 'thu_start_time_alt': '12:00:00',
                                                 'thu_end_time_alt': '12:00:00',
                                                 'fri_start_time_alt': '12:00:00',
                                                 'fri_end_time_alt': '12:00:00',
                                                 'sat_start_time_alt': '12:00:00',
                                                 'sat_end_time_alt': '12:00:00',
                                                 'course_group': course_groups[3].pk})
        categoryhelper.verify_category_matches_data(self, categories[2],
                                                    {'title': 'Uncategorized', 'weight': 0.0, 'color': '#4986e7',
                                                     'average_grade': 66.6667, 'grade_by_weight': 0.0, 'trend': None,
                                                     'course': courses[0].pk})
        categoryhelper.verify_category_matches_data(self, categories[3],
                                                    {'title': 'Uncategorized', 'weight': 0.0, 'color': '#4986e7',
                                                     'average_grade': 66.6667, 'grade_by_weight': 0.0, 'trend': None,
                                                     'course': courses[2].pk})
        materialgrouphelper.verify_material_group_matches_data(self, material_groups[1],
                                                               {'title': 'Test Material Group',
                                                                'shown_on_calendar': True, 'user': 1})
        materialhelper.verify_material_matches_data(self, materials[1],
                                                    {'title': 'Test Material', 'status': 3, 'condition': 7,
                                                     'website': 'http://www.material.com', 'price': '9.99',
                                                     'details': 'Return by 7/1', 'material_group': 2, 'courses': []})
        eventhelper.verify_event_matches_data(self, events[2],
                                              {'title': 'Test Event', 'all_day': False, 'show_end_time': True,
                                               'start': '2017-05-08T12:00:00Z', 'end': '2017-05-08T14:00:00Z',
                                               'priority': 75, 'url': None, 'comments': 'A comment on an event.',
                                               'user': 1})
        eventhelper.verify_event_matches_data(self, events[3],
                                              {'title': 'Test Event', 'all_day': False, 'show_end_time': True,
                                               'start': '2017-05-08T12:00:00Z', 'end': '2017-05-08T14:00:00Z',
                                               'priority': 75, 'url': None, 'comments': 'A comment on an event.',
                                               'user': 1})
        homeworkhelper.verify_homework_matches_data(self, homework[2],
                                                    {'title': 'Test Homework', 'all_day': False, 'show_end_time': True,
                                                     'start': '2017-05-08T16:00:00Z', 'end': '2017-05-08T18:00:00Z',
                                                     'priority': 65, 'url': None,
                                                     'comments': 'A comment on a homework.', 'current_grade': '20/30',
                                                     'completed': True, 'category': categories[3].pk,
                                                     'course': courses[2].pk, 'materials': [materials[1].pk]})
        homeworkhelper.verify_homework_matches_data(self, homework[3],
                                                    {'title': 'Test Homework', 'all_day': False, 'show_end_time': True,
                                                     'start': '2017-05-08T16:00:00Z', 'end': '2017-05-08T18:00:00Z',
                                                     'priority': 65, 'url': None,
                                                     'comments': 'A comment on a homework.', 'current_grade': '-1/100',
                                                     'completed': False, 'category': categories[1].pk,
                                                     'course': courses[3].pk, 'materials': []})

    def test_import_invalid_json(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)
        tmp_file = attachmenthelper.given_file_exists(ext='.json')

        # WHEN
        with open(tmp_file.name) as fp:
            data = {
                'file[]': [fp]
            }
            response = self.client.post(
                reverse('importexport_import'),
                data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(ExternalCalendar.objects.count(), 0)
        self.assertEqual(CourseGroup.objects.count(), 0)
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(MaterialGroup.objects.count(), 0)
        self.assertEqual(Material.objects.count(), 0)
        self.assertEqual(Event.objects.count(), 0)
        self.assertEqual(Homework.objects.count(), 0)
        self.assertEqual(Reminder.objects.count(), 0)

    def test_import_invalid_relationships(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        with open(os.path.join(os.path.dirname(__file__), os.path.join('resources', 'invalidsample.json'))) as fp:
            data = {
                'file[]': [fp]
            }
            response = self.client.post(
                reverse('importexport_import'),
                data)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('course', response.data['homework'][1])
        self.assertIn('may not be null', response.data['homework'][1]['course'][0])
        self.assertIn('materials', response.data['homework'][1])
        self.assertIn('object does not exist', response.data['homework'][1]['materials'][0])
        self.assertEqual(ExternalCalendar.objects.count(), 0)
        self.assertEqual(CourseGroup.objects.count(), 0)
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(MaterialGroup.objects.count(), 0)
        self.assertEqual(Material.objects.count(), 0)
        self.assertEqual(Event.objects.count(), 0)
        self.assertEqual(Homework.objects.count(), 0)
        self.assertEqual(Reminder.objects.count(), 0)

    def test_export_success(self):
        # GIVEN
        user1 = userhelper.given_a_user_exists_and_is_logged_in(self.client)
        user2 = userhelper.given_a_user_exists(username='user2', email='test2@email.com')
        external_calendar = externalcalendarhelper.given_external_calendar_exists(user1)
        event1 = eventhelper.given_event_exists(user1)
        event2 = eventhelper.given_event_exists(user1)
        eventhelper.given_event_exists(user2)
        course_group1 = coursegrouphelper.given_course_group_exists(user1)
        course_group2 = coursegrouphelper.given_course_group_exists(user1)
        course_group3 = coursegrouphelper.given_course_group_exists(user2)
        course1 = coursehelper.given_course_exists(course_group1, room='')
        course2 = coursehelper.given_course_exists(course_group2)
        course3 = coursehelper.given_course_exists(course_group3)
        category1 = categoryhelper.given_category_exists(course1, title='Uncategorized')
        category2 = categoryhelper.given_category_exists(course2)
        category3 = categoryhelper.given_category_exists(course3)
        material_group1 = materialgrouphelper.given_material_group_exists(user1)
        material_group2 = materialgrouphelper.given_material_group_exists(user2)
        material1 = materialhelper.given_material_exists(material_group1)
        materialhelper.given_material_exists(material_group2)
        homework1 = homeworkhelper.given_homework_exists(course1, category=category1, completed=True,
                                                         current_grade="20/30", materials=[material1])
        homework2 = homeworkhelper.given_homework_exists(course2, category=category2, current_grade="-1/100")
        homeworkhelper.given_homework_exists(course3, category=category3, completed=True, current_grade="-1/100")
        reminder = reminderhelper.given_reminder_exists(user1, homework=homework1)

        # WHEN
        response = self.client.get(reverse('importexport_export'))
        data = json.loads(response.content)

        # THEN
        course_group1 = CourseGroup.objects.get(pk=course_group1.pk)
        course_group2 = CourseGroup.objects.get(pk=course_group2.pk)
        course1 = Course.objects.get(pk=course1.pk)
        course2 = Course.objects.get(pk=course2.pk)
        category1 = Category.objects.get(pk=category1.pk)
        category2 = Category.objects.get(pk=category2.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        externalcalendarhelper.verify_externalcalendar_matches_data(self, external_calendar,
                                                                    data['external_calendars'][0])
        eventhelper.verify_event_matches_data(self, event1, data['events'][0])
        eventhelper.verify_event_matches_data(self, event2, data['events'][1])
        coursegrouphelper.verify_course_group_matches_data(self, course_group1, data['course_groups'][0])
        coursegrouphelper.verify_course_group_matches_data(self, course_group2, data['course_groups'][1])
        coursehelper.verify_course_matches_data(self, course1, data['courses'][0])
        coursehelper.verify_course_matches_data(self, course2, data['courses'][1])
        categoryhelper.verify_category_matches_data(self, category1, data['categories'][1])
        categoryhelper.verify_category_matches_data(self, category2, data['categories'][0])
        homeworkhelper.verify_homework_matches_data(self, homework1, data['homework'][0])
        homeworkhelper.verify_homework_matches_data(self, homework2, data['homework'][1])
        reminderhelper.verify_reminder_matches_data(self, reminder, data['reminders'][0])

    def test_user_registration_imports_example_schedule(self):
        # GIVEN
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        self.client.post(reverse('register'),
                         {'email': 'test@test.com', 'username': 'my_test_user',
                          'password1': 'test_pass_1!',
                          'password2': 'test_pass_1!', 'time_zone': 'America/Chicago'})

        # THEN
        start_of_current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(CourseGroup.objects.count(), 1)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(MaterialGroup.objects.count(), 2)
        self.assertEqual(Material.objects.count(), 4)
        self.assertEqual(Homework.objects.count(), 22)
        self.assertEqual(CourseGroup.objects.all()[0].start_date, start_of_current_month.date())
        self.assertEqual(Course.objects.all()[0].start_date, start_of_current_month.date())
        homework = Homework.objects.all()[0]
        self.assertEqual(homework.start.date(), homework.course.start_date + datetime.timedelta(days=11))