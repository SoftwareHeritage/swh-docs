# Copyright (C) 2017-2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
from setuptools import setup, find_packages


def parse_requirements(name=None):
    if name:
        reqf = "requirements-%s.txt" % name
    else:
        reqf = "requirements.txt"

    requirements = []
    if not os.path.exists(reqf):
        return requirements

    with open(reqf) as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            requirements.append(line)
    return requirements


setup(
    name="swh.docs",
    description="Software Heritage development documentation",
    python_requires=">=3.7",
    author="Software Heritage developers",
    author_email="swh-devel@inria.fr",
    url="https://forge.softwareheritage.org/source/swh-docs/",
    packages=find_packages(),
    scripts=[],
    install_requires=parse_requirements(),
    setup_requires=["vcversioner"],
    extras_require={
        "testing": parse_requirements("test"),
        "building": parse_requirements("swh"),
    },
    vcversioner={},
    include_package_data=True,
)
