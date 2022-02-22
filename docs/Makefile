SPHINXOPTS ?=
SPHINXOPTCOLOR ?= --color
SPHINXBUILD = sphinx-build
SOURCEDIR = .
BUILDDIR = _build
HTMLDIR = $(BUILDDIR)/html
SWHPKGDIR ?= sources/swh/

INSTALL_HOST = pergamon.internal.softwareheritage.org
INSTALL_DIR = /srv/softwareheritage/docs/webroot/devel
INSTALL_GROUP = swhdev
INSTALL_PERMS = g+rwX

SPHINXAPIDOC = sphinx-apidoc
APIDOC_DIR = apidoc
APIDOC_OPTS = --ext-viewcode --separate --no-toc
APIDOC_EXCLUDES = */tests */tests/* */*/tests/* */*/*/tests/*
APIDOC_EXCLUDES += */migrations */migrations/* */*/migrations/* */*/*/migrations/*
APIDOC_EXCLUDES += */wsgi.py */*/wsgi.py */*/*/wsgi.py */*/*/wsgi.py
APIDOC_EXCLUDES += deposit/settings/* web/settings/* dataset/*
APIDOC_SWH_EXCLUDES = $(patsubst %,$(SWHPKGDIR)/%,$(APIDOC_EXCLUDES))

html: sphinx/html

sphinx/html: links-stamp apidoc-stamp images-stamp rec-build-stamp

links-stamp:
	bin/ln-sphinx-subprojects
	touch $@

apidoc: apidoc-stamp
apidoc-stamp: links-stamp
	$(SPHINXAPIDOC) \
		--implicit-namespaces \
		--templatedir=../swh/docs/templates/ \
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
	$(MAKE) -C swh-deposit/images
	touch $@

# Build documentation recursively in all packages, to make sure that auxiliary,
# non-sphinx managed documentation artifacts (e.g., schema diagrams) are also
# built.
rec-build-stamp: $(wildcard ../../swh-*/docs/*.rst)
	$(MAKE) -C ../../ docs-assets
	touch $@

clean: sphinx/clean
	bin/ln-sphinx-subprojects --remove
	$(MAKE) -C images clean
	rm -f *-stamp
	rm -f $(APIDOC_DIR)/*

distclean: clean
	make -C ../../ docs-clean

help: sphinx/help

sphinx/clean:
	$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(SPHINXOPTCOLOR)

sphinx/%:
	$(SPHINXBUILD) -b $* "$(SOURCEDIR)" "$(BUILDDIR)/$*" $(SPHINXOPTS) $(SPHINXOPTCOLOR)

install: html
	test -d $(HTMLDIR)
	rsync -rlvuz --delete $(BUILDDIR)/html/ $(INSTALL_HOST):$(INSTALL_DIR)/
	ssh $(INSTALL_HOST) \
		"find $(INSTALL_DIR) -not -group $(INSTALL_GROUP) -exec chgrp -v $(INSTALL_GROUP) {} + ; \
		 find $(INSTALL_DIR) -not -perm -ug=rw,o=r -exec chmod -v ug+rw,o+r {} + ; \
		 find $(INSTALL_DIR) -type d -not -perm -g=xs,ou=x -exec chmod -v g+xs,ou+x {} +"

.PHONY: help html clean distclean install images-stamp
