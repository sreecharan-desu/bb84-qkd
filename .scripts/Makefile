# Build system for BB84 Research Manuscript
# This file is located in .scripts/, all paths are relative to the root.

LATEX_SOURCE  = docs/main.tex
BIB_SOURCE    = docs/refs.bib
PDF_OUTPUT    = bb84_fingerprint_paper.pdf
LATEX_COMPILER = pdflatex
BIB_COMPILER   = bibtex

# Rebuild the publication ready PDF
all: $(PDF_OUTPUT)

$(PDF_OUTPUT): $(LATEX_SOURCE) $(BIB_SOURCE)
	@echo "Updating Manuscript: $(PDF_OUTPUT)..."
	@mkdir -p .build
	# Triple-pass to resolve LaTeX cross-references and BibTeX citations
	$(LATEX_COMPILER) -output-directory=.build $(LATEX_SOURCE)
	-cd .build && $(BIB_COMPILER) main
	$(LATEX_COMPILER) -output-directory=.build $(LATEX_SOURCE)
	$(LATEX_COMPILER) -output-directory=.build $(LATEX_SOURCE)
	@mv -f .build/main.pdf ../$(PDF_OUTPUT)
	@echo "Research Paper updated: $(PDF_OUTPUT)"

# Cleanup transient build files
clean:
	rm -rf .build

.PHONY: all clean
