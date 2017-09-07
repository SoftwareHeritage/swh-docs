from swh.docs.sphinx.conf import *  # NoQA

# For swh-web, needed to allow import of django modules (sigh). Note: this is
# here and not in swh.docs.sphinx.docs to avoid forcing a django dependency on
# every module that uses the common Sphinx configuration.
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swh.web.settings")
django.setup()
