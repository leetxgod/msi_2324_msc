@echo off
setlocal

latexmk -xelatex cover-latex/main.tex
latexmk -pdf -interaction=nonstopmode -synctex=1 "%~1"
set build_result=%errorlevel%

if %build_result% equ 0 (
    echo ✅ Build succeeded. Cleaning aux files...
    latexmk -c "%~1"
    latexmk -c cover-latex/main.tex
) else (
    echo ❌ Build failed. Keeping aux files for debugging.
)

endlocal