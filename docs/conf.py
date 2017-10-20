# flake8: noqa

import swh.docs.sphinx.conf as sphinx_conf

# swh-web needs to add some extra sphinx settings
import swh.web.doc_config as swh_web_doc_config
swh_web_doc_config.customize_sphinx_conf(sphinx_conf)

from swh.docs.sphinx.conf import *
