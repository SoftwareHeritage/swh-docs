from swh.deposit.settings.development import *  # noqa
import swh.web.settings.development as web

# merge some config variables
ns = globals()
for var in dir(web):
    if var.isupper() and var in ns and isinstance(ns[var], list):
        for elt in getattr(web, var):
            if elt not in ns[var]:
                ns[var].append(elt)

# swh-web needs to find its static files when running autodoc
STATIC_DIR = web.STATIC_DIR
STATICFILES_DIRS = web.STATICFILES_DIRS

SECRET_KEY = "change me"
