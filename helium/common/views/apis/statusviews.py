import copy
import time
from concurrent.futures import ThreadPoolExecutor

import psutil
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework.viewsets import ViewSet

from health_check.contrib.psutil.backends import MemoryUsage, DiskUsage
from health_check.plugins import plugin_dir

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.9'


def _run(plugin):
    plugin.run_check()
    try:
        return plugin.errors
    finally:
        from django.db import connection
        connection.close()


def _build_components_status(plugins):
    components = {}
    highest_severity = 999
    system_status = 'operational'
    for p in plugins:
        components[str(p.identifier())] = {
            "status": p.sensitive_status(),
            "description": p.description,
            "took": round(p.time_taken, 4)
        }
        plugin_severity = p.highest_severity()
        if plugin_severity < highest_severity:
            highest_severity = plugin_severity
            system_status = components[str(p.identifier())]["status"]

    return components, system_status


class StatusResourceView(ViewSet):
    """
    status:
    Check the status of the system and its dependencies.
    """

    @never_cache
    def status(self, request, *args, **kwargs):
        errors = []

        plugins = sorted((
            plugin_class(**copy.deepcopy(options))
            for plugin_class, options in plugin_dir._registry
        ), key=lambda plugin: plugin.identifier())

        with ThreadPoolExecutor(max_workers=len(plugins) or 1) as executor:
            for plugin, error in zip(plugins, executor.map(_run, plugins)):
                if plugin.critical:
                    errors.extend(error)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR if errors else status.HTTP_200_OK

        components, system_status = _build_components_status(plugins)

        return JsonResponse(
            {
                "components": components,
                "status": system_status
            },
            status=status_code
        )


class HealthResourceView(ViewSet):
    """
    health:
    Check the health of this node and its dependencies.
    """

    @never_cache
    def health(self, request, *args, **kwargs):
        errors = []

        plugins = sorted((
            plugin_class(**copy.deepcopy(options))
            for plugin_class, options in plugin_dir._registry
        ), key=lambda plugin: plugin.identifier())
        plugins.append(DiskUsage())
        plugins.append(MemoryUsage())

        with ThreadPoolExecutor(max_workers=len(plugins) or 1) as executor:
            for plugin, error in zip(plugins, executor.map(_run, plugins)):
                if plugin.critical:
                    errors.extend(error)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR if errors else status.HTTP_200_OK

        components, system_status = _build_components_status(plugins)

        return JsonResponse(
            {
                "components": components,
                "uptime": round(time.time() - psutil.boot_time(), 2),
                "disk_usage": '{}%'.format(psutil.disk_usage('/').percent),
                "memory_available": '{} MB'.format(int(psutil.virtual_memory().available / 1024 / 1024)),
                "status": system_status
            },
            status=status_code
        )
