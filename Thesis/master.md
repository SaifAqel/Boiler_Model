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
  - \usepackage{indentfirst}
  - \setlength{\parindent}{1.5em}
  - \usepackage[acronym,nonumberlist]{glossaries}
  - \usepackage{longtable}
  - \usepackage{array}
  - \makenoidxglossaries
  - \loadglsentries{Thesis/abbreviations.tex}

  - |
    \newglossarystyle{acronyms-table}{
      \renewenvironment{theglossary}
        {\begin{longtable}{>{\bfseries}p{0.16\linewidth} p{0.64\linewidth} p{0.16\linewidth}}
         \textbf{Abbrev.} & \textbf{Meaning} & \textbf{Units} \\
         \hline\endhead}
        {\end{longtable}}

      % how each main entry prints
      \renewcommand*{\glossentry}[2]{%
        \glsentryshort{##1} & \glsentrylong{##1} & \glsentryuseri{##1}\\%
      }

      % how subentries print (indent the abbreviation slightly)
      \renewcommand*{\subglossentry}[3]{%
        \hspace*{1em}\glsentryshort{##2} & \glsentrylong{##2} & \glsentryuseri{##2}\\%
      }

      \renewcommand*{\glsgroupskip}{\addlinespace}
    }

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
\clearpage

\clearpage

```{=latex}
\chapter*{\centering DECLARATIONS}
\addcontentsline{toc}{chapter}{DECLARATIONS}
```

\begin{center}
Declaration about the acceptability of the thesis
\end{center}

This thesis fulfills every formal and content requirements of the regulation of the Budapest University of Technology and Economics, moreover it fulfills the assignment of the final project. This thesis is suitable for a review and an open defense.

Budapest, DATE

\vspace{2cm}

\begin{flushright}
Dr. Lezsovits Ferenc
\end{flushright}

\vspace{2cm}

\begin{center}
Declaration about the independent work
\end{center}

I, Saif-Aldain Ahmad Deeb Aqel (QTY3S6), hereby declare that the Thesis submitted for assessment and defense, exclusively contains the results of my own work assisted by my supervisor. Further to it, it is also stated that all other results taken from the technical literature or other sources are clearly identified and referred to according to copyright (footnotes/references are chapter and verse, and placed appropriately).

I accept that the scientific results presented in my Thesis can be utilized by the Department of the supervisor for further research or teaching purposes.

Budapest, DATE

\vspace{2cm}

\begin{flushright}
Saif-Aldain Aqel
\end{flushright}

\clearpage
\tableofcontents
\clearpage

\listoffigures
\addcontentsline{toc}{chapter}{List of Figures}
\clearpage

\listoftables
\addcontentsline{toc}{chapter}{List of Tables}
\clearpage

\newpage
