import logging

from rest_framework import serializers

from helium.planner.models import CourseGroup

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.0.1'

logger = logging.getLogger(__name__)


class CourseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGroup
        fields = (
            'id', 'title', 'start_date', 'end_date', 'shown_on_calendar', 'average_grade', 'trend', 'private_slug',
            'user',
            # Property fields (which should also be declared as read-only)
            'num_days', 'num_days_completed', 'num_homework', 'num_homework_completed', 'num_homework_graded',)
        read_only_fields = (
            'average_grade', 'trend', 'private_slug', 'user', 'num_days', 'num_days_completed', 'num_homework',
            'num_homework_completed', 'num_homework_graded',)

    def validate(self, attrs):
        start_date = self.instance.start_date if self.instance else attrs.get('start_date', None)
        end_date = self.instance.end_date if self.instance else attrs.get('end_date', None)

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("The 'start_date' must be before the 'end_date'")

        return attrs
