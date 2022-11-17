# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS  ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR    = .
BUILDDIR     = _build
HTMLDIR      = $(BUILDDIR)/html

INSTALL_HOST  = pergamon.internal.softwareheritage.org
INSTALL_DIR   = /srv/softwareheritage/docs/webroot
INSTALL_GROUP = swhdev
INSTALL_PERMS = g+rwX

.PHONY: help images apidoc html clean install

all: html

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
sphinx/%: Makefile images apidoc
	@$(SPHINXBUILD) -M $* "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

sphinx/clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

images:
	$(MAKE) -C devel images-stamp
	$(MAKE) -C sysadm images-stamp

apidoc:
	$(MAKE) -C devel apidoc

html: sphinx/html

clean: sphinx/clean
	$(MAKE) -C devel clean
	$(MAKE) -C sysadm clean
	$(MAKE) -C user clean

install: html
	test -d $(HTMLDIR)
	rsync -rlvuz --delete $(BUILDDIR)/html/ $(INSTALL_HOST):$(INSTALL_DIR)/
	ssh $(INSTALL_HOST) \
		"find $(INSTALL_DIR) -not -group $(INSTALL_GROUP) -exec chgrp -v $(INSTALL_GROUP) {} + ; \
		 find $(INSTALL_DIR) -not -perm -ug=rw,o=r -exec chmod -v ug+rw,o+r {} + ; \
		 find $(INSTALL_DIR) -type d -not -perm -g=xs,ou=x -exec chmod -v g+xs,ou+x {} +"
