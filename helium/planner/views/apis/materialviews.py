import json
import logging

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from helium.common.permissions import IsOwner
from helium.common.utils import metricutils
from helium.planner.models import MaterialGroup, Material, Course
from helium.planner.serializers.materialserializer import MaterialSerializer
from helium.planner.views.apis.schemas.materialschemas import MaterialIDSchema, MaterialListSchema

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'

logger = logging.getLogger(__name__)


class UserMaterialsApiListView(GenericAPIView, ListModelMixin):
    """
    get:
    Return a list of all material instances for the authenticated user.
    """
    serializer_class = MaterialSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Material.objects.filter(material_group__user_id=user.pk)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MaterialGroupMaterialsApiListView(GenericAPIView, ListModelMixin):
    """
    get:
    Return a list of all material instances for the given material group.

    post:
    Create a new material instance for the given material group.
    """
    serializer_class = MaterialSerializer
    permission_classes = (IsAuthenticated,)
    schema = MaterialListSchema()

    def get_queryset(self):
        user = self.request.user
        return Material.objects.filter(material_group_id=self.kwargs['material_group'],
                                       material_group__user_id=user.pk)

    def check_material_group_permission(self, request, material_group_id):
        if not MaterialGroup.objects.filter(pk=material_group_id, user_id=request.user.pk).exists():
            raise NotFound('MaterialGroup not found.')

    def check_course_permission(self, request, course_id):
        if not Course.objects.filter(pk=course_id, course_group__user_id=request.user.pk).exists():
            raise NotFound('Course not found.')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, material_group, format=None):
        data = request.data.copy()

        self.check_material_group_permission(request, material_group)
        # If Django Rest Framework adds better support for properly getting the `help_text` of related fields,
        # this can be removed
        if 'courses' in data:
            courses = json.loads(data['courses'])
            for course_id in courses:
                self.check_course_permission(request, course_id)
            data.pop('courses')
        else:
            courses = []

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save(material_group_id=material_group, courses=courses)

            logger.info(
                'Material {} created in MaterialGroup {} for user {}'.format(serializer.instance.pk, material_group,
                                                                             request.user.get_username()))

            metricutils.increment(request, 'action.material.created')

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialGroupMaterialsApiDetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    """
    get:
    Return the given material instance.

    put:
    Update the given material instance.

    delete:
    Delete the given material instance.
    """
    serializer_class = MaterialSerializer
    permission_classes = (IsAuthenticated, IsOwner,)
    schema = MaterialIDSchema()

    def get_queryset(self):
        user = self.request.user
        return Material.objects.filter(material_group_id=self.kwargs['material_group'],
                                       material_group__user_id=user.pk)

    def check_material_group_permission(self, request, material_group_id):
        if not MaterialGroup.objects.filter(pk=material_group_id, user_id=request.user.pk).exists():
            raise NotFound('MaterialGroup not found.')

    def check_course_permission(self, request, course_id):
        if not Course.objects.filter(pk=course_id, course_group__user_id=request.user.pk).exists():
            raise NotFound('Course not found.')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, material_group, pk, format=None):
        data = request.data.copy()

        material = self.get_object()
        if 'material_group' in data:
            self.check_material_group_permission(request, data['material_group'])
        # If Django Rest Framework adds better support for properly getting the `help_text` of related fields,
        # this can be removed
        if 'courses' in data:
            courses = json.loads(data['courses'])
            for course_id in courses:
                self.check_course_permission(request, course_id)
            data.pop('courses')
        else:
            courses = []

        serializer = self.get_serializer(material, data=data)

        if serializer.is_valid():
            serializer.save(courses=courses)

            logger.info('Material {} updated for user {}'.format(pk, request.user.get_username()))

            metricutils.increment(request, 'action.material.updated')

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)

        logger.info(
            'Material {} deleted from MaterialGroup {} for user {}'.format(kwargs['pk'], kwargs['material_group'],
                                                                           request.user.get_username()))

        metricutils.increment(request, 'action.material.deleted')

        return response