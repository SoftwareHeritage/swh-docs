SPHINXOPTS =
SPHINXBUILD = python3 -c 'import sphinx, sys; sys.exit(sphinx.main(sys.argv))'
SOURCEDIR = .
BUILDDIR = _build
HTMLDIR = $(BUILDDIR)/html

INSTALL_HOST = pergamon.internal.softwareheritage.org
INSTALL_DIR = /srv/softwareheritage/docs/webroot/devel
INSTALL_GROUP = swhdev
INSTALL_PERMS = g+rwX


html: sphinx/html
sphinx/html: links-stamp apidoc-stamp images-stamp

links-stamp:
	bin/ln-sphinx-subprojects
	touch $@

apidoc-stamp:
	$(MAKE) -C ../../ docs-apidoc
	touch $@

images-stamp:
	$(MAKE) -C images
	touch $@

clean: sphinx/clean
	bin/ln-sphinx-subprojects --remove
	$(MAKE) -C images clean
	rm -f *-stamp

distclean: clean
	make -C ../../ docs-clean

help: sphinx/help

sphinx/%:
	@$(SPHINXBUILD) -M $* "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

install: html
	test -d $(HTMLDIR)
	rsync -rlvuz --delete $(BUILDDIR)/html/ $(INSTALL_HOST):$(INSTALL_DIR)/
	ssh $(INSTALL_HOST) \
		"find $(INSTALL_DIR) -not -group $(INSTALL_GROUP) -exec chgrp -v $(INSTALL_GROUP) {} + ; \
		 find $(INSTALL_DIR) -not -perm -ug=rw,o=r -exec chmod -v ug+rw,o+r {} + ; \
		 find $(INSTALL_DIR) -type d -not -perm -g=xs,ou=x -exec chmod -v g+xs,ou+x {} +"

.PHONY: help html clean distclean install
