
PY_REQUIREMENTS = $(wildcard ../../../*/requirements*.txt)
DEP_GRAPHS_base = py-deps-all py-deps-swh py-deps-ext
DEP_GRAPHS += $(patsubst %,%.dot,$(DEP_GRAPHS_base))
DEP_GRAPHS += $(patsubst %,%.pdf,$(DEP_GRAPHS_base))
DEP_GRAPHS += $(patsubst %,%.svg,$(DEP_GRAPHS_base))
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

%.svg: %.dot
	dot -T svg $< > $@

clean:
	-rm -f $(DEP_GRAPHS)
