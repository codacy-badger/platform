import logging

from rest_framework import serializers

from helium.planner.models import Reminder

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.4'

logger = logging.getLogger(__name__)


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = (
            'id', 'title', 'message', 'start_of_range', 'offset', 'offset_type', 'type', 'sent', 'homework', 'event',
            'user',)
        read_only_fields = ('start_of_range', 'user',)

    def validate(self, attrs):
        if not self.instance and ('event' not in attrs and 'homework' not in attrs):
            raise serializers.ValidationError("One of `event` or `homework` must be given.")
        elif attrs.get('event', None) and attrs.get('homework', None):
            raise serializers.ValidationError("Only one of `event` or `homework` may be given.")

        # We're settings these to None here as the serialization save will persist the new parent
        if self.instance and ('event' in attrs or 'homework' in attrs):
            self.instance.event = None
            self.instance.homework = None

        return attrs


class ReminderExtendedSerializer(ReminderSerializer):
    class Meta(ReminderSerializer.Meta):
        depth = 2

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['user'] = representation['user']['id']

        return representation
