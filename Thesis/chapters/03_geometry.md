# Configuration

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_parts.png}
\caption{Example of shell boiler setup components}
\label{fig:boiler_parts}
\end{figure}

The simulated unit is a three pass fire tube shell boiler with six distinct gas side heat transfer stages and a single common steam drum on the water/steam side. Hot flue gas from the burner traverses a radiative furnace, two reversal chambers, two convective tube banks, and a final economizer before leaving to the stack.

## Layout

The gas path is represented as:

$$
\mathrm{Burner} \rightarrow \mathrm{HX_1} \rightarrow \mathrm{HX_2} \rightarrow \mathrm{HX_3}
\rightarrow \mathrm{HX_4} \rightarrow \mathrm{HX_5} \rightarrow \mathrm{HX_6} \rightarrow \mathrm{stack}
$$

with the following interpretation:

- $\mathrm{HX_1}$ – Furnace (first pass)  
  Large, single furnace tube where combustion products enter directly from the burner and transfer heat mainly by radiation and high-temperature convection to the surrounding water/steam.

- $\mathrm{HX_2}$ – First reversal chamber  
  Short cylindrical wet back chamber that turns the flow from the furnace outlet into the first convective tube bank (gas direction change = 180°).

- $\mathrm{HX_3}$ – First convective tube bank (second pass)
  Bank of small diameter fire tubes arranged in a staggered pattern inside the shell, to boost convection; flue gas flows inside of the tubes, water/steam outside.

- $\mathrm{HX_4}$ – Second reversal chamber
  Second turning chamber redirecting gas from the first to the second tube bank.

- $\mathrm{HX_5}$ – Second convective tube bank (third pass)
  Second fire-tube bundle, representing the last in-boiler convective pass.

- $\mathrm{HX_6}$ – Economizer
  Separate, downstream tube bank used to preheat feedwater in single-phase operation before entering the drum/boiler circuit, recovering heat, and boosting efficiency of the boiler.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/economizer_section.jpg}
\caption{Cross-section of the economizer tube bundle $\mathrm{HX_6}$, showing gas-side cross-flow and water-side internal flow.}
\label{fig:economizer-cross-section}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_with_economizer.png}
\caption{Three-pass shell boiler with rear-mounted economizer for feedwater preheating.}
\label{fig:boiler-with-economizer}
\end{figure}

## Geometry and surface specification

### Drum configuration {- .unlisted}

The boiler has a single horizontal steam drum. Its inner diameter is $$D_{i,\text{drum}} = 4.5\ \text{m}$$ and its length $$L_{\text{drum}} = 5.0\ \text{m}$$.

The drum is not modelled with internal separators or circulation hardware. It simply supplies the saturated water/steam state at boiler pressure, while all circulation effects are represented by the single 1-D water/steam stream used in the heat-transfer stages.

### Flue gas passes {- .unlisted}

All six pressure part stages of the simulated boiler are represented with a consolidated geometric and surface specification.

Table: Flue gas stages key parameters

|     Element     | Kind         | Di [m] | L [m] | N_tubes [-] | Wall t [mm] | Roughness [µm] | Pool boiling [-] |
| :-------------: | ------------ | :----: | :---: | :---------: | :---------: | :------------: | :--------------: |
| $\mathrm{HX_1}$ | single_tube  |  1.40  | 5.276 |      1      |     2.9     |      0.5       |       true       |
| $\mathrm{HX_2}$ | reversal_ch. |  1.60  | 0.80  |      1      |     2.9     |      0.5       |       true       |
| $\mathrm{HX_3}$ | tube_bank    | 0.076  | 4.975 |     118     |     2.9     |      0.5       |       true       |
| $\mathrm{HX_4}$ | reversal_ch. |  1.60  | 0.80  |      1      |     2.9     |      0.5       |       true       |
| $\mathrm{HX_5}$ | tube_bank    | 0.076  | 5.620 |     100     |     2.9     |      0.5       |       true       |
| $\mathrm{HX_6}$ | economizer   | 0.076  | 7.50  |     160     |     2.5     |      0.5       |      false       |

The input file `stages.yaml`, provided in Annex A, contain the complete detailed specifications and is parsed at runtime by the configuration loader (`new_loader.py`). This separates numerical solution algorithms from geometry and surface data, and allows different boiler variants to be simulated by simply modifying the YAML files.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_cross_section.jpg}
\caption{Detailed cross-section of the simulated boiler, showing drum, furnace, tube banks and reversal chambers.}
\label{fig:boiler-cross-section-2}
\end{figure}

All pressure-part stages ($\mathrm{HX_1}$–$\mathrm{HX_5}$) share the same steel wall thermal conductivity of $\mathrm{k_{wall}} = 16$ $\text{W/m/K}$. The economizer ($\mathrm{HX_6}$) is modelled with a higher wall conductivity $\mathrm{k_{wall}} = 30$ $\text{W/m/K}$ and a clean surface (zero fouling thickness) to represent a best-case heat-recovery configuration.

The YAML configuration supplies wall, surface, and hydraulic properties not captured in the tabulated geometry. Each pressure-part exchanger defines wall thickness, wall conductivity, surface roughness, emissivity, and optional fouling layers with specified thickness and conductivity. Most stages use a uniform carbon-steel wall with smooth surfaces and thin fouling layers, while the economizer uses a thinner, higher-conductivity wall and no fouling to reflect a cleaned section.

The steam drum defines diameter, length, and internal surface properties with its own roughness and fouling settings.

Reversal chambers specify curvature radius and nozzle minor-loss coefficients used in pressure-drop calculations.

Tube-bank stages define full shell-side layout: shell diameter, tube count and pitch, tube-row arrangement (staggered or inline), baffle spacing and cut, and bundle clearances. Evaporator banks use tighter pitch and spacing to enhance shell-side transfer, whereas the economizer uses a more open inline layout with a larger tube count and longer tubes.

These YAML entries are translated by the loader into the geometric and hydraulic quantities required for cross-flow areas, Reynolds numbers, and shell-side heat-transfer evaluation.

\newpage

## Assumptions and limitations

1. Combustion and flue gas

   - Ideal complete combustion, with fixed excess air,
   - Adiabatic flame temperature from equilibrium chemistry, using NASA polynomials.
   - Ideal gas mixture $p = \rho R T$, with transport properties $\mu(T)$ $k(T)$ $c_p(T)$ from polynomial data.
   - Steady state boiler operation, with fixed fuel air and feedwater.
   - Boiler efficiency computed on HHV or LHV basis, using standard energy balance equations.

2. Heat transfer

   - One dimensional steady heat transfer per stage.
   - Uniform wall conductivity and thickness, radial conduction only.
   - Gas side HTC from standard correlations properties **vary** with temperature pressure and composition.
   - Gas radiation via band averaged grey model for $CO_2$ and $H_2O$, no spectral resolution, and no soot formation.
   - Water side HTC uses IAPWS-IF97 properties, homogenized two phase model.
   - Drum at fixed pressure, and perfect steam water separation (no carryover).

3. Hydraulic and thermal performance

   - 1D, steady, single phase flow.
   - Constant mass flow along each stage.
   - Compressibility effects appear only through property variations $\rho(T,P)$ and $\mu(T,P)$ in $\mathrm{Re}$ and $\rho V^2 / 2$.
   - Stage level minor loss coefficients are lumped, and uniformly distributed along the stage.
   - Gas side ΔP in economizer stage is neglected.
