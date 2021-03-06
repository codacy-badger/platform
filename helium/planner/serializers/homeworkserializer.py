import logging

from rest_framework import serializers

from helium.planner.models import Homework
from helium.planner.serializers.attachmentserializer import AttachmentSerializer
from helium.planner.serializers.reminderserializer import ReminderSerializer
from helium.planner.tasks import recalculate_category_grade

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.4'

logger = logging.getLogger(__name__)


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = (
            'id', 'title', 'all_day', 'show_end_time', 'start', 'end', 'priority', 'url', 'comments', 'current_grade',
            'completed', 'category', 'materials', 'attachments', 'reminders', 'course',
            # Property fields (which should also be declared as read-only)
            'calendar_item_type',)
        read_only_fields = ('attachments', 'reminders', 'calendar_item_type',)

    def validate(self, attrs):
        start = attrs.get('start', None)
        if not start and self.instance:
            start = self.instance.start
        end = attrs.get('end', None)
        if not end and self.instance:
            end = self.instance.end

        if start and end and start > end:
            raise serializers.ValidationError("The 'start' must be before the 'end'")

        return attrs

    def update(self, instance, validated_data):
        old_category = self.instance.category if 'category' in validated_data and self.instance.category_id != \
                                                                                  validated_data['category'] else None

        instance = super().update(instance, validated_data)

        if old_category:
            recalculate_category_grade(old_category.pk)

        return instance


class HomeworkExtendedSerializer(HomeworkSerializer):
    attachments = AttachmentSerializer(many=True)

    reminders = ReminderSerializer(many=True)
