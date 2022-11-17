SPHINXOPTS ?= -t devel_doc
SPHINXOPTCOLOR ?= --color
SPHINXBUILD = sphinx-build
SOURCEDIR = .
BUILDDIR = _build
SWHPKGDIR ?= sources/swh/

SPHINXAPIDOC = sphinx-apidoc
APIDOC_DIR = apidoc
APIDOC_OPTS = --ext-viewcode --separate --no-toc
APIDOC_EXCLUDES = */tests */migrations */wsgi.py */conftest.py */setup.py
APIDOC_EXCLUDES += deposit/settings/* web/settings/* dataset/*
APIDOC_SWH_EXCLUDES = $(patsubst %,"$(SWHPKGDIR)/%",$(APIDOC_EXCLUDES))

all: html

html: sphinx/html

sphinx/html: links-stamp apidoc-stamp images-stamp rec-build-stamp

links-stamp:
	mkdir -p sources/swh
	bin/ln-sphinx-subprojects
	touch $@

apidoc: apidoc-stamp
apidoc-stamp: links-stamp
	$(SPHINXAPIDOC) \
		--implicit-namespaces \
		--templatedir=../../swh/docs/templates/ \
		--maxdepth=3 \
		$(APIDOC_OPTS) \
		-o $(APIDOC_DIR) \
		$(SWHPKGDIR) \
		$(APIDOC_SWH_EXCLUDES)
	touch $@
	# remove warning about swh.rst not being included in any toctree
	sed -i '1s/^/:orphan:\n\n/' $(APIDOC_DIR)/swh.rst

images-stamp:
	$(MAKE) -C images
	touch $@

# Build documentation recursively in all packages, to make sure that auxiliary,
# non-sphinx managed documentation artifacts (e.g., schema diagrams) are also
# built.
rec-build-stamp: $(wildcard ../../swh-*/docs/*.rst)
	$(MAKE) -C ../../../ docs-assets
	touch $@

clean: sphinx/clean
	bin/ln-sphinx-subprojects --remove
	$(MAKE) -C images clean
	rm -f *-stamp
	rm -f $(APIDOC_DIR)/*

distclean: clean
	make -C ../../../ docs-clean

sphinx/clean:
	$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(SPHINXOPTCOLOR)

sphinx/%:
	$(SPHINXBUILD) -b $* "$(SOURCEDIR)" "$(BUILDDIR)/$*" $(SPHINXOPTS) $(SPHINXOPTCOLOR)

.PHONY: html clean distclean install
