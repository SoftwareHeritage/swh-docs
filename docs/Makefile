SPHINXOPTS ?=
SPHINXBUILD = python3 -c 'import sphinx, sys; sys.exit(sphinx.main(sys.argv))'
SOURCEDIR = .
BUILDDIR = _build
HTMLDIR = $(BUILDDIR)/html
SWHPKGDIR = `python3 -c 'import swh; print(swh.__path__[0])'`

INSTALL_HOST = pergamon.internal.softwareheritage.org
INSTALL_DIR = /srv/softwareheritage/docs/webroot/devel
INSTALL_GROUP = swhdev
INSTALL_PERMS = g+rwX

SPHINXAPIDOC = sphinx-apidoc
APIDOC_DIR = apidoc
APIDOC_OPTS = --ext-viewcode
APIDOC_EXCLUDES = */tests */tests/* */*/tests/* */*/*/tests/*
APIDOC_EXCLUDES += */migrations */migrations/* */*/migrations/* */*/*/migrations/*
APIDOC_EXCLUDES += */wsgi.py */*/wsgi.py */*/*/wsgi.py */*/*/wsgi.py
APIDOC_SWH_EXCLUDES = $(patsubst %,$(SWHPKGDIR)/%,$(APIDOC_EXCLUDES))

html: sphinx/html

sphinx/html: links-stamp apidoc-stamp images-stamp rec-build-stamp

links-stamp:
	bin/ln-sphinx-subprojects
	touch $@

apidoc: apidoc-stamp
apidoc-stamp: images-stamp
	$(SPHINXAPIDOC) $(APIDOC_OPTS) -o $(APIDOC_DIR) $(SWHPKGDIR) $(APIDOC_SWH_EXCLUDES)
	touch $@

images-stamp:
	$(MAKE) -C images
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
	$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

sphinx/%:
	$(SPHINXBUILD) -b $* "$(SOURCEDIR)" "$(BUILDDIR)/$*" $(SPHINXOPTS)

install: html
	test -d $(HTMLDIR)
	rsync -rlvuz --delete $(BUILDDIR)/html/ $(INSTALL_HOST):$(INSTALL_DIR)/
	ssh $(INSTALL_HOST) \
		"find $(INSTALL_DIR) -not -group $(INSTALL_GROUP) -exec chgrp -v $(INSTALL_GROUP) {} + ; \
		 find $(INSTALL_DIR) -not -perm -ug=rw,o=r -exec chmod -v ug+rw,o+r {} + ; \
		 find $(INSTALL_DIR) -type d -not -perm -g=xs,ou=x -exec chmod -v g+xs,ou+x {} +"

.PHONY: help html clean distclean install
