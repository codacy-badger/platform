import logging

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from helium.common.permissions import IsOwner
from helium.common.utils import metricutils
from helium.planner.models import MaterialGroup
from helium.planner.schemas import MaterialGroupDetailSchema
from helium.planner.serializers.materialgroupserializer import MaterialGroupSerializer

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.3.7'

logger = logging.getLogger(__name__)


class MaterialGroupsApiListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    """
    get:
    Return a list of all material group instances for the authenticated user.

    post:
    Create a new material group instance for the authenticated user.

    For more details pertaining to choice field values, [see here](https://github.com/HeliumEdu/platform/wiki#choices).
    """
    serializer_class = MaterialGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if hasattr(self.request, 'user'):
            user = self.request.user
            return user.material_groups.all()
        else:
            MaterialGroup.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)

        logger.info('MaterialGroup {} created for user {}'.format(response.data['id'], request.user.get_username()))

        metricutils.increment('action.materialgroup.created', request)

        return response


class MaterialGroupsApiDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """
    get:
    Return the given material group instance.

    put:
    Update the given material group instance.

    delete:
    Delete the given material group instance.
    """
    serializer_class = MaterialGroupSerializer
    permission_classes = (IsAuthenticated, IsOwner,)
    schema = MaterialGroupDetailSchema()

    def get_queryset(self):
        if hasattr(self.request, 'user'):
            user = self.request.user
            return user.material_groups.all()
        else:
            return MaterialGroup.objects.none()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)

        logger.info('MaterialGroup {} updated for user {}'.format(kwargs['pk'], request.user.get_username()))

        metricutils.increment('action.materialgroup.updated', request)

        return response

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)

        logger.info('MaterialGroup {} deleted for user {}'.format(kwargs['pk'], request.user.get_username()))

        metricutils.increment('action.materialgroup.deleted', request)

        return response
