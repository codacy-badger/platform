import logging

from rest_framework import serializers

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.3.1'

logger = logging.getLogger(__name__)


class PrivateFeedSerializer(serializers.Serializer):
    events_private_url = serializers.URLField()

    homework_private_url = serializers.URLField()

    courseschedules_private_url = serializers.URLField()
