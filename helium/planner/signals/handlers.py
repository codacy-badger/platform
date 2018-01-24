import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from helium.planner.models import Category, Course, Homework
from helium.planner.tasks import gradingtasks

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Course)
def delete_course(sender, instance, **kwargs):
    gradingtasks.recalculate_course_group_grade.delay(instance.course_group)


@receiver(post_save, sender=Category)
def save_category(sender, instance, **kwargs):
    gradingtasks.recalculate_category_grade.delay(instance)


@receiver(post_delete, sender=Category)
def delete_category(sender, instance, **kwargs):
    gradingtasks.recalculate_course_grade.delay(instance.course)


@receiver(post_delete, sender=Homework)
def delete_homework(sender, instance, **kwargs):
    if instance.category:
        gradingtasks.recalculate_category_grade.delay(instance.category)


@receiver(post_save, sender=Homework)
def save_homework(sender, instance, **kwargs):
    if instance.category:
        gradingtasks.recalculate_category_grade.delay(instance.category)