SPHINXOPTS =
SPHINXBUILD = sphinx-build
SOURCEDIR = .
BUILDDIR = _build
HTMLDIR = $(BUILDDIR)/html

INSTALL_HOST = pergamon.internal.softwareheritage.org
INSTALL_DIR = /srv/softwareheritage/docs/webroot/devel
INSTALL_GROUP = swhdev
INSTALL_PERMS = g+rwX

html: sphinx/html
sphinx/html: links-stamp apidoc-stamp

links-stamp:
	bin/ln-sphinx-subprojects
	touch $@

apidoc-stamp:
	make -C ../../ docs-apidoc
	touch $@

clean: sphinx/clean
	bin/ln-sphinx-subprojects --remove
	rm -f *-stamp

distclean: clean
	make -C ../../ docs-clean

help: sphinx/help
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

sphinx/%:
	@$(SPHINXBUILD) -M $* "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

install: html
	test -d $(HTMLDIR)
	rsync -avuz $(BUILDDIR)/html/ $(INSTALL_HOST):$(INSTALL_DIR)/
	ssh $(INSTALL_HOST) \
		"chgrp -R $(INSTALL_GROUP) $(INSTALL_DIR) ; \
		 chmod -R $(INSTALL_PERMS) $(INSTALL_DIR) ; \
		 find $(INSTALL_DIR) -type d -exec chmod g+s {} +"

.PHONY: help html clean distclean install
