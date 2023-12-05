# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Reads docs/devel/forge-support.yml and generates ReST documents with tables
summarizing the status of loaders ands listers."""

from pathlib import Path
import sys
import textwrap

import tabulate
from typing_extensions import Literal

from .software_origins import parse

LISTERS_PRELUDE = """
.. This file was generated by swh/docs/generate_forge_list.py using {source_yml}

.. rst-class:: swh-logos-table

.. table::
  :align: center

"""


LOADERS_PRELUDE = """
.. This file was generated by swh/docs/generate_forge_list.py using {source_yml}

.. rst-class:: swh-logos-table

.. table::
  :align: center

"""


def write_table(data, lister_or_loader: Literal["lister", "loader"], file) -> None:
    links = []
    headers = (
        f"{lister_or_loader.capitalize()} name",
        "Related links",
        "Current status",
        "Related `grants <https://www.softwareheritage.org/grants/>`_",
    )
    table = []
    for forge_id, forge in sorted(data["forges"].items()):
        package_name = forge[lister_or_loader].package_name
        links.append(
            (
                f"{forge_id}-source",
                forge[lister_or_loader].source,
            )
        )

        logo_cell = f"|{forge_id}_logo|\n\n:ref:`user-software-origins-{forge_id}`"

        if forge_id in ("cran", "gnu"):
            # FIXME: swh-web coverage should have them lowercased, like everything else
            id_in_swh_web_coverage = forge_id.upper()
        else:
            id_in_swh_web_coverage = forge_id

        status = forge[lister_or_loader].status
        if status == "N/A":
            # No lister or loader for this forge, skipping
            continue
        elif status == "dev":
            status_cell = "In development"
            links_cell = (
                f"* `Source Code <{forge_id}-source_>`__\n"
                f"* :mod:`Developer documentation <{package_name}>`"
            )
        elif status == "staging":
            status_cell = "In staging"
            if lister_or_loader == "loader":
                links.append(
                    (
                        f"{forge_id}-origins",
                        "https://webapp.staging.swh.network/browse/search/"
                        f"?with_visit=true&with_content=true&visit_type={forge_id}",
                    )
                )

                links_cell = (
                    f"* `Source Code <{forge_id}-source_>`__\n"
                    f"* :mod:`Developer documentation <{package_name}>`\n"
                    f"* `Browse origins <{forge_id}-origins_>`__"
                )
            else:
                links.append(
                    (
                        f"{forge_id}-coverage",
                        "https://webapp.staging.swh.network/coverage/"
                        f"?focus={id_in_swh_web_coverage}#{id_in_swh_web_coverage}",
                    )
                )
                links_cell = (
                    f"* `Source Code <{forge_id}-source_>`__\n"
                    f"* :mod:`Developer documentation <{package_name}>`\n"
                    f"* `See coverage <{forge_id}-coverage_>`__"
                )
        elif status == "prod":
            status_cell = "In production"
            if lister_or_loader == "loader":
                links.append(
                    (
                        f"{forge_id}-origins",
                        f"https://archive.softwareheritage.org/browse/search/"
                        f"?with_visit=true&with_content=true&visit_type={forge_id}",
                    )
                )
                links_cell = (
                    f"* `Source Code <{forge_id}-source_>`__\n"
                    f"* :mod:`Developer documentation <{package_name}>`\n"
                    f"* `Browse origins <{forge_id}-origins_>`__"
                )
            else:
                links.append(
                    (
                        f"{forge_id}-coverage",
                        f"https://archive.softwareheritage.org/coverage/"
                        f"?focus={id_in_swh_web_coverage}#{id_in_swh_web_coverage}",
                    )
                )
                links_cell = (
                    f"* `Source Code <{forge_id}-source_>`__\n"
                    f"* :mod:`Developer documentation <{package_name}>`\n"
                    f"* `See coverage <{forge_id}-coverage_>`__"
                )
        else:
            assert False, f"Unexpected status {status!r} for {forge_id}"
        issue = forge[lister_or_loader].get("issue")
        if issue:
            links_cell += f"\n* `Tracking issue <{forge[lister_or_loader].issue}>`__"

        notes = forge.get("notes")
        if notes:
            status_cell = f"{status_cell}\n\n{notes}"

        grant_id = forge.get("grant")
        grant = data["grants"][grant_id] if grant_id else None
        developer_id = forge.get("developer")
        if grant:
            assert developer_id, f"{forge_id} has grant but no developer"
            developer = data["developers"][developer_id]
            grant_cell = (
                f"|{grant_id}|_\n\n"
                f"(awarded to `{developer.name} <{developer.url}>`__)"
            )
        else:
            assert not developer_id, f"{forge_id} has developer but no grant"
            grant_cell = ""

        table.append((logo_cell, links_cell, status_cell, grant_cell))

    file.write(
        textwrap.indent(
            tabulate.tabulate(table, headers=headers, tablefmt="grid"),
            prefix="  ",
        )
        + "\n\n"
    )

    for link_name, link_url in links:
        file.write(f".. _{link_name}: {link_url}\n")

    file.write("\n")


def write_logos(data, lister_or_loader: Literal["lister", "loader"], file) -> None:
    for forge_id, forge in sorted(data["forges"].items()):
        if forge[lister_or_loader]["status"] != "N/A":
            file.write(
                f".. |{forge_id}_logo| image:: logos/{forge_id}.png\n"
                f"  :width: 50%\n"
                f"  :target: software-origins/{forge_id}.html\n"
                f"  :alt: {forge.name} {lister_or_loader}\n"
                f"\n"
            )


def write_grants(data, file) -> None:
    for grant_id, grant in data["grants"].items():
        file.write(
            f".. |{grant_id}| replace:: {grant.funder}\n"
            f".. _{grant_id}: {grant.announcement}\n"
            f"\n"
        )


def main(input_path: Path, lister_output_path: Path, loader_output_path: Path) -> None:
    data = parse(input_path)

    with lister_output_path.open("wt") as listers_file, loader_output_path.open(
        "wt"
    ) as loaders_file:
        listers_file.write(LISTERS_PRELUDE.format(source_yml=input_path))
        loaders_file.write(LOADERS_PRELUDE.format(source_yml=input_path))

        write_table(data, "lister", listers_file)
        write_table(data, "loader", loaders_file)

        write_logos(data, "lister", listers_file)
        write_logos(data, "loader", loaders_file)

        write_grants(data, listers_file)
        write_grants(data, loaders_file)


if __name__ == "__main__":
    try:
        (_, input_path, lister_output_path, loader_output_path) = sys.argv
    except ValueError:
        print(
            f"Syntax: {sys.argv[0]} docs/devel/forge-support.yml "
            f"docs/user/software-origins/dynamic/lister_table.inc "
            f"docs/user/software-origins/dynamic/loader_table.inc",
            sys.stderr,
        )
        exit(1)
    main(Path(input_path), Path(lister_output_path), Path(loader_output_path))
