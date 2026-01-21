# Copyright (C) 2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Reads :file:`docs/software-origins-support.yml` and generates ReST documents
which are included each in a forge's page to summarize its status and link
to other documentation page"""

from pathlib import Path
import sys

from .software_origins import parse


def write_status(data, forge_id, file) -> None:
    forge = data.forges[forge_id]

    has_loader = forge["loader"]["status"] != "N/A"
    has_lister = forge["lister"]["status"] != "N/A"

    links_cell = ""

    if forge.status == "dev":
        status_cell = f"Archival for {forge.name} is currently in development:\n\n"
    elif forge.status in ("staging", "prod"):
        if forge.status == "staging":
            status_cell = (
                f"{forge.name} is currently archived only on "
                f"the staging infrastructure:\n\n"
            )
        else:
            status_cell = (
                f"{forge.name} is currently archived by Software Heritage:\n\n"
            )

        if has_loader:
            links_cell += f"* `Browse\N{NBSP}origins <{forge.origins}>`__\n"
        if has_lister:
            links_cell += f"* `See\N{NBSP}coverage <{forge.coverage}>`__\n"
    else:
        assert False, f"Unexpected status {forge.status!r} for {forge_id}"

    if has_loader:
        links_cell += (
            f"* `Loader Source Code <{forge.loader.source}>`__\n"
            f"* :mod:`Loader Developer documentation <{forge.loader.package_name}>`"
            f"\n"
        )
    if has_lister:
        links_cell += (
            f"* `Lister Source Code <{forge.lister.source}>`__\n"
            f"* :mod:`Lister Developer documentation <{forge.lister.package_name}>`"
            f"\n"
        )

    loader_issue = forge["loader"].get("issue")
    lister_issue = forge["lister"].get("issue")
    if loader_issue and lister_issue:
        if loader_issue == lister_issue:
            links_cell += f"* `Tracking issue <{loader_issue}>`__\n\n"
        else:
            links_cell += (
                f"* `Tracking loader issue <{loader_issue}>`__\n\n"
                f"* `Tracking lister issue <{lister_issue}>`__\n\n"
            )
    elif not loader_issue and not lister_issue:
        pass
    elif lister_issue:
        if has_loader:
            status_cell += f"* `Lister Tracking issue <{lister_issue}>`__\n\n"
        else:
            status_cell += f"* `Tracking issue <{lister_issue}>`__\n\n"
    elif loader_issue:
        if has_loader:
            status_cell += f"* `Loader Tracking issue <{loader_issue}>`__\n\n"
        else:
            status_cell += f"* `Tracking issue <{loader_issue}>`__\n\n"
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

        # TODO: grammar is hard; we may want to write 'grant from the XXX Foundation'
        # but also 'grant from XXX' sometimes.
        # For now, only foundations provide grants.
        assert grant.funder.endswith(" Foundation")

        grant_cell = (
            f"Developed by `{developer['name']} <{developer['url']}>`__ "
            f"thanks to a `grant from the {grant.funder} <{grant.announcement}>`__ "
        )
    else:
        assert not developer_id, f"{forge_id} has developer but no grant"
        grant_cell = ""

    file.write(status_cell)
    file.write(links_cell)
    file.write("\n")
    file.write(grant_cell)

    file.write("\n")


def write_logo(data, forge_id, file) -> None:
    forge = data.forges[forge_id]
    file.write(
        f".. image:: ../logos/{forge_id}.png\n"
        f"  :alt: {forge['name']} logo\n"
        f"  :align: right"
        f"\n\n"
    )


def main(input_path: Path, output_dir: Path) -> None:
    data = parse(input_path)

    for forge_id in data.forges:
        with (output_dir / f"{forge_id}_status.inc").open("wt") as output_file:
            write_logo(data, forge_id, output_file)
            write_status(data, forge_id, output_file)


if __name__ == "__main__":
    try:
        (_, input_path, output_path) = sys.argv
    except ValueError:
        print(
            f"Syntax: {sys.argv[0]} docs/devel/forge-support.yml "
            f"docs/user/software-origins/",
            sys.stderr,
        )
        exit(1)
    main(Path(input_path), Path(output_path))
