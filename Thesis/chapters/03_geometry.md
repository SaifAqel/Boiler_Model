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

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_cross_section.jpg}
\caption{Detailed cross-section of the simulated boiler, showing drum, furnace, tube banks and reversal chambers.}
\label{fig:boiler-cross-section-2}
\end{figure}

### Drum {- .unlisted}

The boiler drum is modelled as a single horizontal cylindrical vessel without internal separators or circulation devices. It provides saturated liquid and vapour at drum pressure.

The inner diameter of the drum is $D_{i,\text{drum}} = 4.5\ \text{m}$ and the total length is $L_{\text{drum}} = 5.0\ \text{m}$

The drum wall is made of carbon steel with a uniform thickness of $t_{\text{drum}} = 0.05\ \text{m}$ and thermal conductivity $k_{\text{drum}} = 40\ \text{W m}^{-1}\text{K}^{-1}$

A fouling layer of thickness $0.1\ \text{mm}$ and conductivity $0.2\ \text{W m}^{-1}\text{K}^{-1}$ is applied on the inner surface.

### Pool boiling stages {- .unlisted}

All five pressure part stages located inside the drum are modelled under pool boiling conditions. These stages represent the furnace and convective passes before the economizer. Internal flow is one dimensional while external boiling occurs at drum saturation conditions.

All stages use steel walls with thermal conductivity $k_{\text{wall}} = 50\ \text{W m}^{-1}\text{K}^{-1}$, with internal roughness $\zeta_{\text{gas}} = 50\ \mu\text{m}$, and outer roughness $\zeta_{\text{water}} = 20\ \mu\text{m}$, while surface emissivity is $0.80$.

Fouling resistance is included via a uniform fouling layer of thickness $0.1\ \text{mm}$ and conductivity $0.2\ \text{W m}^{-1}\text{K}^{-1}$.

The main geometric parameters of the pool boiling stages are summarized in Table~\ref{tab:stages_geom}.

Table: Pool boiling pressure part geometry
\label{tab:stages_geom}

| Element | Kind             | $D_i$ [m] | $L$ [m] | Tube no. | Wall thickness [mm] | Roughness [$\mu$m] |
| :-----: | :--------------- | :-------: | :-----: | :------: | :-----------------: | :----------------: |
|   HX1   | single tube      |   1.40    |  5.276  |    1     |         20          |         50         |
|   HX2   | reversal chamber |   1.60    |  0.80   |    1     |         20          |         50         |
|   HX3   | tube bank        |   0.076   |  4.975  |   118    |         2.9         |         50         |
|   HX4   | reversal chamber |   1.60    |  0.80   |    1     |         20          |         50         |
|   HX5   | tube bank        |   0.076   |  5.620  |   100    |         2.9         |         50         |

The tube banks HX3 and HX5 are staggered arrangements with six tube rows. The transverse and longitudinal pitches are both $S_T = S_L = 0.11\ \text{m}$.

Reversal chambers HX2 and HX4 include curvature effects through a bend radius of $0.8\ \text{m}$

### Economizer {- .unlisted}

The economizer is modelled as a shell and tube heat exchanger operating under single phase conditions on both sides. It is located downstream of the final pool boiling stage.

Flue gas flows on the shell side through a cylindrical duct of inner diameter
$D_{\text{shell}} = 0.95\ \text{m}$.

The tube side consists of four parallel circuits. Each circuit contains sixty tubes of inner diameter $D_{i,\text{eco}} = 0.0337\ \text{m}$ with a total developed tube length of $L_{\text{tube}} = 80\ \text{m}$ per circuit.

The tube bundle is arranged in a staggered configuration. Transverse and longitudinal pitches are $S_T = 0.09\ \text{m}$ and $S_L = 0.10\ \text{m}$ respectively.

Baffle spacing is $0.25\ \text{m}$ with a baffle cut of $0.25$ and a bundle clearance of $10\ \text{mm}$.

The economizer tubes are made of steel with wall thickness $t_{\text{eco}} = 2.6\ \text{mm}$ and thermal conductivity $k_{\text{eco}} = 50\ \text{W m}^{-1}\text{K}^{-1}$. Inner surface roughness is $20\ \mu\text{m}$ and outer surface roughness is $50\ \mu\text{m}$. No fouling resistance is applied in the economizer.

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

\newpage
