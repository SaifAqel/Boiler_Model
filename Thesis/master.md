---
title: "Heat Transfer and Fluid Flow Calculations of Industrial Shell Boilers and Evaluation of Operation Conditions – Draft"
author: "Saif-Aldain Aqel"
date: 2025
bibliography: "Thesis/refs/library.bib"
csl: "Thesis/refs/ieee.csl"
reference-section-title: "References"
citeproc: true
toc: false
numbersections: true
mainfont: "Arial"
sansfont: "Arial"
monofont: "Consolas"
monofontoptions:
  - Scale=0.85
  - Ligatures=TeX
fontsize: 12pt
geometry:
  - a4paper
  - margin=1in
documentclass: report
pdf-engine: xelatex
highlight-style: tango
tables: true
caption-position: below
header-includes:
  - \usepackage{float}
  - \usepackage{graphicx}
  - \usepackage{amsmath}
  - \numberwithin{equation}{chapter}
  - \usepackage{caption}
  - \captionsetup[table]{font=small}
  - \usepackage{pdfpages}
autoEqnLabels: true
filters:
  - pandoc-crossref
---

\includepdf[
pages=1,
fitpaper=true,
pagecommand={}
]{Thesis/figures/task_page.pdf}
\clearpage
\tableofcontents
\clearpage
\newpage
