# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -t user_doc
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

all: html

software-origins/dynamic/table.inc: ../software-origins-support.yml ../../swh/docs/generate_software_origins_list.py ../../swh/docs/generate_software_origin_status.py ../../swh/docs/software_origins.py
	python3 -m swh.docs.generate_software_origin_status ../software-origins-support.yml software-origins/dynamic/
	# technically the above should be in their own targets, but it would be
	# overly complicated.
	python3 -m swh.docs.generate_software_origins_list ../software-origins-support.yml software-origins/dynamic/table.inc

software-origins/dynamic/lister_table.inc software-origins/dynamic/loader_table.inc: ../software-origins-support.yml ../../swh/docs/generate_lister_loader_lists.py ../../swh/docs/software_origins.py
	python3 -m swh.docs.generate_lister_loader_lists ../software-origins-support.yml software-origins/dynamic/lister_table.inc software-origins/dynamic/loader_table.inc

dynamic-rst: software-origins/dynamic/table.inc software-origins/dynamic/lister_table.inc software-origins/dynamic/loader_table.inc

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
sphinx/%: Makefile dynamic-rst
	@$(SPHINXBUILD) -M $* "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: sphinx/html

clean: sphinx/clean
	rm -f software-origins/dynamic/*.inc

.PHONY: html clean dynamic-rst
