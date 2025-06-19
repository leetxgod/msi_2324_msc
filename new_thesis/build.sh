#!/bin/bash

# latexmk -xelatex cover-latex/main.tex
latexmk -pdf -interaction=nonstopmode -synctex=1 "$1"
build_result=$?

if [ $build_result -eq 0 ]; then
    echo "✅ Build succeeded. Cleaning aux files..."
    latexmk -C "$1"
    # latexmk -xelatex -c cover-latex/main.tex
else
    echo "❌ Build failed. Keeping aux files for debugging."
fi
