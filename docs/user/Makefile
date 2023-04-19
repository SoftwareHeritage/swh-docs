# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -t sysadm_doc
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

all: html

listers/table.inc loaders/table.inc: ../forge-support.yml
	python3 -m swh.docs.generate_forge_list ../forge-support.yml listers/table.inc loaders/table.inc

dynamic-rst: listers/table.inc loaders/table.inc

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
sphinx/%: Makefile dynamic-rst
	@$(SPHINXBUILD) -M $* "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: sphinx/html

clean: sphinx/clean
	rm -f listers/table.inc loaders/table.inc

.PHONY: html clean dynamic-rst
