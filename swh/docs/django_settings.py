# Copyright (C) 2021-2025  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from importlib import reload
import os


def force_django_settings(settings_module):
    """
    Enable to modify django settings module dynamically while
    building sphinx documentation and force settings full reloading.
    """
    if os.environ.get("DJANGO_SETTINGS_MODULE") != settings_module:
        os.environ["DJANGO_SETTINGS_MODULE"] = settings_module

        import django
        from django import conf as django_conf

        # reset django settings to force their reloading
        reload(django_conf)
        django.setup()

        # ensure django apps are registered
        from django.apps import apps
        from django.conf import settings

        apps.set_installed_apps(settings.INSTALLED_APPS)
