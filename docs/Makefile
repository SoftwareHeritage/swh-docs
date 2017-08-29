SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

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

.PHONY: html help clean
