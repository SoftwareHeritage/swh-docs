import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'swh.deposit.settings.development')
django.setup()

from swh.docs.sphinx.conf import *  # NoQA
