# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Reads :file:`docs/devel/software-origins-support.yml` and generates ReST documents
with tables summarizing the status of loaders ands listers."""

from pathlib import Path
import sys
import textwrap

import tabulate

from .software_origins import parse

PRELUDE = """
.. This file was generated by swh/docs/generate_software_origins_list.py
.. using {source_yml}

.. rst-class:: swh-logos-table

.. table::
  :align: center

"""


def write_table(data, file) -> None:
    links = []
    headers = (
        "Software origins",
        "Related links",
        "Current status",
        "Related `grants <https://www.softwareheritage.org/grants/>`_",
    )
    table = []
    for (forge_id, forge) in sorted(data["forges"].items()):
        logo_cell = (
            f"|{forge_id}_logo|\n\n:ref:`{forge['name']} "
            f"<user-software-origins-{forge_id}>`"
        )

        links.append((f"{forge_id}-loader-source", forge.loader.source))
        links.append((f"{forge_id}-lister-source", forge.lister.source))

        has_loader = forge["loader"]["status"] != "N/A"
        has_lister = forge["lister"]["status"] != "N/A"

        if forge.status == "dev":
            status_cell = "In\N{NBSP}development\n\n"
        elif forge.status in ("staging", "prod"):
            links.append((f"{forge_id}-origins", forge.origins))
            links.append((f"{forge_id}-coverage", forge.coverage))
            if forge.status == "staging":
                status_cell = "In\N{NBSP}staging\n\n"
            else:
                status_cell = "In\N{NBSP}production\n\n"

            if has_loader:
                status_cell += f"`Browse\N{NBSP}origins <{forge_id}-origins_>`__\n\n"
            if has_lister:
                status_cell += f"`See\N{NBSP}coverage <{forge_id}-coverage_>`__\n\n"
        else:
            assert False, f"Unexpected status {forge.status!r} for {forge_id}"

        links_cell = ""
        if has_loader:
            links_cell += (
                f"* `Loader Source Code <{forge_id}-loader-source_>`__\n"
                f"* :mod:`Loader Developer documentation <{forge.loader.package_name}>`"
                f"\n"
            )
        if has_lister:
            links_cell += (
                f"* `Lister Source Code <{forge_id}-lister-source_>`__\n"
                f"* :mod:`Lister Developer documentation <{forge.lister.package_name}>`"
                f"\n"
            )

        loader_issue = forge["loader"].get("issue")
        lister_issue = forge["lister"].get("issue")
        if loader_issue and lister_issue:
            if loader_issue == lister_issue:
                status_cell += f"`Tracking issue <{loader_issue}>`__\n\n"
            else:
                status_cell += (
                    f"`Tracking loader issue <{loader_issue}>`__\n\n"
                    f"`Tracking lister issue <{lister_issue}>`__\n\n"
                )
        elif not loader_issue and not lister_issue:
            pass
        elif lister_issue:
            if has_loader:
                status_cell += f"`Lister Tracking issue <{lister_issue}>`__\n\n"
            else:
                status_cell += f"`Tracking issue <{lister_issue}>`__\n\n"
        elif loader_issue:
            if has_loader:
                status_cell += f"`Loader Tracking issue <{loader_issue}>`__\n\n"
            else:
                status_cell += f"`Tracking issue <{loader_issue}>`__\n\n"
        else:
            assert False, f"The impossible happened for {forge_id}"

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
                f"(awarded to `{developer['name']} <{developer['url']}>`__)"
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

    for (link_name, link_url) in links:
        file.write(f".. _{link_name}: {link_url}\n")

    file.write("\n")


def write_toctree(data, file) -> None:
    file.write(".. toctree::\n" "  :maxdepth: 2\n" "  :hidden:\n" "\n")
    for (forge_id, forge) in sorted(data["forges"].items()):
        file.write(f"  {forge_id}\n")

    file.write("\n")


def write_logos(data, file) -> None:
    for (forge_id, forge) in sorted(data["forges"].items()):
        file.write(
            f".. |{forge_id}_logo| image:: ../logos/{forge_id}.png\n"
            f"  :target: {forge_id}.html\n"
            f"  :alt: {forge['name']}\n"
            f"\n"
        )


def write_grants(data, file) -> None:
    for (grant_id, grant) in data["grants"].items():
        file.write(
            f".. |{grant_id}| replace:: {grant['funder']}\n"
            f".. _{grant_id}: {grant['announcement']}\n"
            f"\n"
        )


def main(input_path: Path, output_path: Path) -> None:
    data = parse(input_path)

    with output_path.open("wt") as output_file:
        output_file.write(PRELUDE.format(source_yml=input_path))
        write_table(data, output_file)
        write_toctree(data, output_file)
        write_logos(data, output_file)
        write_grants(data, output_file)


if __name__ == "__main__":
    try:
        (_, input_path, output_path) = sys.argv
    except ValueError:
        print(
            f"Syntax: {sys.argv[0]} docs/devel/forge-support.yml "
            f"docs/user/software-origins/dynamic/table.inc",
            sys.stderr,
        )
        exit(1)
    main(Path(input_path), Path(output_path))
