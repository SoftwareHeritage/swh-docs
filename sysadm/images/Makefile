UML_DIAGS_SRC = $(wildcard *.uml)
UML_DIAGS = $(patsubst %.uml,%.svg,$(UML_DIAGS_SRC))

all: $(UML_DIAGS)

%.pdf: %.dot
	dot -T pdf $< > $@

%.svg: %.dot
	dot -T svg $< > $@

%.svg: %.uml
	DISPLAY="" plantuml -tsvg $<

clean:
	-rm -f $(UML_DIAGS)
