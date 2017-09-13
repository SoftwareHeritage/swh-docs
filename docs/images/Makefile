
PY_REQUIREMENTS = $(wildcard ../../../*/requirements*.txt)
DEP_GRAPHS = py-deps-all.pdf py-deps-swh.pdf py-deps-ext.pdf
PY_DEPGRAPH = ../bin/py-depgraph

all: $(DEP_GRAPHS)

py-deps-all.dot: $(PY_DEPGRAPH) $(PY_REQUIREMENTS)
	cd ../../.. ; $(CURDIR)/$(PY_DEPGRAPH) > $(CURDIR)/$@

py-deps-swh.dot: $(PY_DEPGRAPH) $(PY_REQUIREMENTS)
	cd ../../.. ; $(CURDIR)/$(PY_DEPGRAPH) --no-external > $(CURDIR)/$@

py-deps-ext.dot: $(PY_DEPGRAPH) $(PY_REQUIREMENTS)
	cd ../../.. ; $(CURDIR)/$(PY_DEPGRAPH) --no-internal > $(CURDIR)/$@

%.pdf: %.dot
	dot -T pdf $< > $@

clean:
	-rm -f $(DEP_GRAPHS) $(patsubst %.pdf,%.dot,$(DEP_GRAPHS))
