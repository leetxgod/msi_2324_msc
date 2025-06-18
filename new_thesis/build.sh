#!/bin/bash

latexmk -pdf -interaction=nonstopmode -synctex=1 "$1"
build_result=$?

if [ $build_result -eq 0 ]; then
    echo "✅ Build succeeded. Cleaning aux files..."
    latexmk -c "$1"
else
    echo "❌ Build failed. Keeping aux files for debugging."
fi
