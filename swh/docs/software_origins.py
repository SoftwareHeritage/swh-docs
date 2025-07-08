# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Parser for :file:`docs/devel/software-origins-support.yml`"""

import collections
from pathlib import Path

import yaml


class DotDict(collections.UserDict):
    """Like a dictionary, but can be accessed with ``.key`` in addition to
    ``[key]``, to simplify f-string."""

    def __init__(self, d):
        d = {
            key: DotDict(value) if isinstance(value, dict) else value
            for (key, value) in d.items()
        }
        super().__setattr__("data", d)

    def __getattr__(self, key):
        try:
            return self.data[key]
        except KeyError as e:
            raise AttributeError(*e.args) from None

    def __setattr__(self, key, value):
        self.data[key] = value


def parse(input_path: Path):
    data = DotDict(yaml.safe_load(input_path.read_text()))

    for forge_id, forge in sorted(data["forges"].items()):
        forge.loader.setdefault(
            "source",
            f"https://gitlab.softwareheritage.org/swh/devel/swh-loader-core/-/"
            f"tree/master/swh/loader/package/{forge_id}",
        )
        forge.lister.setdefault(
            "source",
            f"https://gitlab.softwareheritage.org/swh/devel/swh-lister/-/"
            f"tree/master/swh/lister/{forge_id}",
        )

        forge.loader.setdefault("package_name", f"swh.loader.package.{forge_id}")
        forge.lister.setdefault("package_name", f"swh.lister.{forge_id}")

        forge.loader.setdefault("id_in_swh_web", forge_id)
        forge.lister.setdefault("id_in_swh_web", forge_id)

        has_loader = forge["loader"]["status"] != "N/A"
        has_lister = forge["lister"]["status"] != "N/A"

        assert has_loader or has_lister, f"{forge_id} has neither loader nor lister"

        if has_loader and has_lister:
            # We may want to do this eventually, but it never happened so far.
            assert (
                forge["loader"]["status"] == forge["lister"]["status"]
            ), f"Loader and lister statuses for {forge_id} are not the same."

        forge.status = (
            forge["loader"]["status"] if has_loader else forge["lister"]["status"]
        )

        if forge.status == "dev":
            forge.origins = None
            forge.coverage = None
        elif forge.status in ("staging", "prod"):
            if forge.status == "staging":
                archive_base_url = "https://webapp.staging.swh.network"
            else:
                archive_base_url = "https://archive.softwareheritage.org"
            forge.origins = (
                f"{archive_base_url}/browse/search/?with_visit=true&with_content=true"
                f"&visit_type={forge.loader.id_in_swh_web}"
            )
            forge.coverage = (
                f"{archive_base_url}/coverage"
                f"?focus={forge.lister.id_in_swh_web}#{forge.lister.id_in_swh_web}"
            )

    return data
