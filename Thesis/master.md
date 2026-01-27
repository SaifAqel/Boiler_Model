---
title: "Heat Transfer and Fluid Flow Calculations of Industrial Shell Boilers and Evaluation of Operation Conditions"
author: "Saif-Aldain Aqel"
date: 2025
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
  - \usepackage{indentfirst}
  - \setlength{\parindent}{1.5em}
  - \addbibresource{Thesis/refs/library.bib}
  - '\DefineBibliographyStrings{english}{bibliography={References}}'
  - '\defbibheading{bibliography}{\chapter*{\bibname}\addcontentsline{toc}{chapter}{\bibname}}'

autoEqnLabels: true
filters:
  - pandoc-crossref
---

\pagenumbering{roman}
\setcounter{page}{2}
\pagestyle{plain}

\includepdf[
pages={1, 2},
pagecommand={\thispagestyle{empty}}
]{Thesis/figures/Title_page.pdf}
\clearpage

\includepdf[
pages={1, 2},
fitpaper=true,
pagecommand={\thispagestyle{empty}}
]{Thesis/signed.PDF}
\clearpage

\clearpage
\tableofcontents
\addcontentsline{toc}{chapter}{Table of Contents}
\clearpage

\listoffigures
\addcontentsline{toc}{chapter}{List of Figures}
\clearpage

\listoftables
\addcontentsline{toc}{chapter}{List of Tables}
\clearpage

\newpage
