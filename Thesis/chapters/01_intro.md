# Introduction

Industrial shell boilers remain one of the most widely deployed technologies for producing saturated steam and hot water in small to medium industrial plants. Their popularity arises from their compact construction, robust heat transfer surfaces, straightforward operation, and comparatively low installation and maintenance requirements. Typical applications span food and beverage processing, chemicals and pharmaceuticals, textiles, healthcare, and general manufacturing sectors where steady, reliable steam generation is essential for heating, processing, and auxiliary services.

Despite their apparent simplicity, the thermal behavior of shell boilers is governed by tightly coupled processes: multi stage radiative and convective heat transfer, natural circulation boiling inside the pressure parts, complex flue gas property variations, and geometry dependent hydraulic losses. Modern operation demands higher efficiency, reduced emissions, increased reliability, and improved control.

This thesis develops a physics based model for a three pass fire tube shell boiler that integrates combustion calculations, detailed flue gas thermophysical properties, multi stage heat transfer modelling, and hydraulic loss estimation. The model is implemented as a one dimensional marching solver applied to six sequential heat exchange stages:

$$
\mathrm{HX_1} \rightarrow \mathrm{HX_2} \rightarrow \mathrm{HX_3}
\rightarrow \mathrm{HX_4} \rightarrow \mathrm{HX_5} \rightarrow \mathrm{HX_6},
$$

representing the furnace, reversal chambers, convective tube banks, and the economizer, see figure \ref{fig:labeled_stages}. On the water side, the boiler drum provides a saturated interface for nucleate boiling in the pressure parts, while the economizer section is treated as a single phase internal flow. Gas side properties are supplied by Cantera, enabling temperature dependent transport, specific heat, thermal conductivity, and radiative behavior to be modelled.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_stages.jpg}
\caption{Shell boiler labeled stages.}
\label{fig:labeled_stages}
\end{figure}

The overall objectives of the study are:

1. To construct a unified combustion-boiler model capable of predicting flue gas temperature, composition, adiabatic flame temperature, and total heat input based on fuel composition and excess air settings.

2. To resolve heat transfer processes along the boiler using stage specific geometries, convection correlations, and a spectral based gas radiation model.

3. To quantify hydraulic losses across each pass using friction factor relations and minor loss coefficients, yielding the total boiler gas side pressure drop.

4. To compute boiler level performance, including useful heat transfer, direct and indirect efficiencies, stack temperature, and stage wise duties.

5. To evaluate sensitivity of boiler performance to key operating parameters, excess air ratio, drum pressure, and fuel mass flow rate.

The numerical framework is structured such that the water/steam mass flow is determined iteratively from the global energy balance. For each operating condition, a fixed point loop between assumed efficiency and resulting steam flow is solved until convergence, ensuring consistency between combustion input, heat transfer output, and steam generation.

The remainder of this thesis is organized as follows. Chapter 2 identifies typical industrial applications of shell boilers and introduces key design features. Chapter 3 describes the boiler geometry and outlines the six heat transfer stages. Chapter 4 develops the combustion and flue gas model, including stoichiometry and adiabatic flame temperature prediction. Chapter 5 covers the heat transfer framework, combining convection and radiation on the gas side with pool boiling and single phase correlations on the water side. Chapter 6 presents the hydraulic model. Chapter 7 reports the resulting boiler performance, while Chapter 8 examines the sensitivity of the system to variations in $\lambda$, pressure, and firing rate. Chapter 9 concludes with a summary of findings.

\newpage
