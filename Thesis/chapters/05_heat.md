# Heat Transfer Model

## Fundamental heat-balance equations

The boiler is modelled as a one-dimensional counter-current heat exchanger composed of six stages ($\mathrm{HX_1}$–$\mathrm{HX_5}$). Heat transfer is resolved along the gas flow direction $x$, while water flows in the opposite direction. Each stage is discretized into segments of length $\mathrm{d}x$; all local quantities are defined per unit length.

- Notation (per segment)

- $x$ – axial coordinate along the gas flow [m]
- $\mathrm{d}x$ – marching step in $x$ [m]
- $\dot{m}_g, \dot{m}_w$ – gas and water mass flow rates [kg/s]
- $T_g(x),\,T_w(x)$ – bulk gas and water temperatures [K]
- $T_{gw}(x),\,T_{ww}(x)$ – gas-side and water-side wall temperatures [K]
- $h_g(x),\,h_w(x)$ – total gas-side and water-side heat-transfer coefficients [W/m²·K]
- $P_g, P_w$ – gas-side and water-side wetted perimeters [m]
- $q'(x)$ – linear heat flux (heat per unit length) [W/m]
- $UA'(x)$ – overall conductance per unit length [W/K/m]

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/heat_step.png}
\caption{Cross section of heat transfer network from gas to water/steam}
\label{fig:heat_step}
\end{figure}

## Local energy balance

For each differential segment of length $\mathrm{d}x$, the model enforces a one-dimensional steady-state energy balance between the gas, the water and the tube wall:

- Heat transferred across the wall:

  $$
  q'(x) = UA'(x)\,\bigl[T_g(x) - T_w(x)\bigr]
  $$

- Relation to the segment duty:

  $$
  \mathrm{d}Q(x) = q'(x)\,\mathrm{d}x
  $$

- Gas stream:

  $$
  \mathrm{d}Q(x) = -\,\dot{m}_g\,\mathrm{d}h_g(x)
  \quad\Rightarrow\quad
  \frac{\mathrm{d}h_g}{\mathrm{d}x} = -\,\frac{q'(x)}{\dot{m}_g}
  $$

- Water stream:
  $$
  \mathrm{d}Q(x) = +\,\dot{m}_w\,\mathrm{d}h_w(x)
  \quad\Rightarrow\quad
  \frac{\mathrm{d}h_w}{\mathrm{d}x} = +\,\frac{q'(x)}{\dot{m}_w}
  $$

In the numerical implementation these equations are applied in finite-difference form over each marching step:

$$
Q_\text{step} = q'(x)\,\Delta x
$$

$$
\Delta h_g = -\frac{Q_\text{step}}{\dot{m}_g},
\qquad
\Delta h_w = +\frac{Q_\text{step}}{\dot{m}_w}
$$

## Overall conductance and resistance network

The overall conductance per unit length $UA'(x)$ is obtained from a radial series of thermal resistances per unit length:

- Gas-side convection:

  $$
  R_g' = \frac{1}{h_g(x)\,P_g}
  $$

- Gas-side fouling:

  $$
  R_{fg}' = R_{fi}'(P_g) \quad\text{(from specified fouling thickness and conductivity)}
  $$

- Tube wall:

  $$
  R_w' = \frac{\ln\!\bigl(D_o/D_i\bigr)}{2\pi k_w}
  $$

- Water-side fouling:

  $$
  R_{fc}' = R_{fo}'(P_w)
  $$

- Water-side convection:
  $$
  R_c' = \frac{1}{h_w(x)\,P_w}
  $$

where $D_i$ and $D_o$ are the tube inner and outer diameters and $k_w$ is the tube wall thermal conductivity. Combining these contributions:

$$
\frac{1}{UA'(x)} = R_g' + R_{fg}' + R_w' + R_{fc}' + R_c'
$$

or equivalently,

$$
UA'(x)
= \left[
\frac{1}{h_g P_g}
+ R_{fg}'
+ R_w'
+ R_{fc}'
+ \frac{1}{h_w P_w}
\right]^{-1}
$$

The linear heat flux then follows directly:

$$
q'(x) = UA'(x)\,\bigl[T_g(x) - T_w(x)\bigr]
$$

## Wall temperature update and thermal convergence

The tube wall temperatures on the gas and water sides, $T_{gw}$ and $T_{ww}$, are updated using a two node wall model in each marching step.

Given $q'(x)$, the wall side energy balances yield:

$$
T_{gw} = T_g - \frac{q'}{h_{g,\text{tot}}}
$$

$$
T_{ww} = T_w + \frac{q'}{h_w}
$$

The wall conduction temperature drop is:

$$
\Delta T_\text{wall} = T_{gw} - T_{ww}
$$

which is also equal to:

$$
\Delta T_\text{wall}
= q' \left[
R_{fg}' + R_w' + R_{fc}'
\right]
$$

A consistency check is applied; if the implied wall temperature difference from conduction differs from the one implied by convection, the marching solver iterates the HTC evaluation once with relaxed updates (default under-relaxation factor 0.35).

In the actual implementation this consistency check is performed by iterating on $T_{gw}$, $T_{ww}$, and $q'$ using the full resistance network (gas convection, gas fouling, wall, water fouling, water convection), with an under-relaxation factor applied to both wall temperatures and the linear heat flux.

If temperature overshoot (negative film coefficient, reversed driving force) is detected within a step, the step is automatically halved and recomputed.

## Stage and boiler level duties

For a stage of length $L_j$, the stage heat duty and stage level conductance are obtained by integrating the local quantities along $x$:

$$
Q_{\text{stage},j}
= \int_0^{L_j} q'(x)\,\mathrm{d}x
\approx \sum_i q'_i\,\Delta x_i
$$

$$
(UA)_j
= \int_0^{L_j} UA'(x)\,\mathrm{d}x
\approx \sum_i UA'_i\,\Delta x_i
$$

The total useful boiler duty is the sum of all stage duties:

$$
Q_\text{useful}
= \sum_{j=1}^{6} Q_{\text{stage},j}
$$

These integrated quantities are later used in the performance and efficiency evaluation (Section 7) and for constructing stage-wise summary tables.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/3_pass_T-Q_diagram.png}
\caption{Representative $T$–$Q$ diagram for the three-pass boiler, showing gas and water/steam temperature evolution and stage heat duties $\mathrm{HX_1}$–$\mathrm{HX_6}$.}
\label{fig:TQ-diagram}
\end{figure}

## Gas side

Gas side heat transfer is computed with geometry aware correlations based on local gas properties from Cantera (`GasProps`) and stage specific geometry from the `GeometryBuilder`. For each marching step, the total gas side HTC is split into a convective and a radiative contribution:

$$
h_{g,\text{tot}} = h_{g,\text{conv}} + h_{g,\text{rad}}
$$

The implementation uses the helper `gas_htc_parts(g, spec, T_{gw})`, which returns $(h_{g,\text{conv}},\,h_{g,\text{rad}})$ in W/m²·K, and then sums them in `gas_htc`.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/gas_path.png}
\caption{Path of flue gas through the 6 stages}
\label{fig:gas_path}
\end{figure}

### Single tube and reversal chamber {#sec-gas-single}

Stages of kind `single_tube` and `reversal_chamber`, corresponding to furnace (first pass), and both reversal chambers, are treated as internal forced convection in a circular duct. The characteristic quantities are:

- Diameter: $D$ (supplied by `stages.yaml`)
- Length: $L$ (supplied by `stages.yaml`)
- Flow area: $A = \frac{1}{4}\,pi\,D^2$ (calculated by geometry builder)
- Velocity:
  $$
  V = \frac{\dot{m}_g}{\rho_g A}
  $$
- Reynolds and Prandtl numbers:
  $$
  \mathrm{Re} = \frac{\rho_g V D}{\mu_g},
  \qquad
  \mathrm{Pr} = \frac{c_{p,g}\,\mu_g}{k_g}
  $$
  Local gas properties $\rho_g, \mu_g, k_g, c_{p,g}$ are obtained from the Cantera mixture via the functions defined in `common\props.py`, at the local gas temperature and pressure. [@mcbride1993]

#### Laminar/developing flow (Graetz-type) {- .unlisted}

For $\mathrm{Re} < 2300$, uses a Graetz correlation for thermally developing laminar flow:

$$
\mathrm{Gz} = \mathrm{Re}\,\mathrm{Pr}\,\frac{D}{L}
$$

$$
\mathrm{Nu} = 3.66 \;+\; \frac{0.0668\,\mathrm{Gz}}
{1 + 0.04\,\mathrm{Gz}^{2/3}}
$$

[@incropera]

#### Turbulent flow (Gnielinski with Petukhov friction factor) {- .unlisted}

For $\mathrm{Re} \ge 2300$, the Gnielinski correlation is applied with a Petukhov friction factor:

$$
f = \left(0.79 \ln \mathrm{Re} - 1.64\right)^{-2}
$$

[@munson]

$$
\mathrm{Nu} =
\frac{\frac{f}{8}(\mathrm{Re} - 1000)\,\mathrm{Pr}}
{1 + 12.7\,\sqrt{\frac{f}{8}}\left(\mathrm{Pr}^{2/3} - 1\right)}
$$

[@incropera]
The local convective heat-transfer coefficient is then:

$$
h_{g,\text{conv}} = \frac{\mathrm{Nu}\,k_g}{D}
$$

[@incropera]

This same internal correlation is used for `single_tube`, `reversal_chamber` and `tube_bank` gas-side flow (see below).

### Tube bank {#sec-gas-bank}

Stages `tube_bank` correspond to tube bundles inside the shell, ie. first and second passes. In this model, the gas side is still treated as internal flow inside the tubes:

- Hot side (gas): inside tubes (inner diameter $D_i$), using the same internal forced convection model as in Section 5.2.1.

Thus the gas side convective HTC in tube-bank stages is:

$$
h_{g,\text{conv}}^\text{(HX3,5)} = \frac{\mathrm{Nu}(\mathrm{Re},\mathrm{Pr})\,k_g}{D_i}
$$

with $\mathrm{Nu}$ given by the Graetz/Gnielinski formulation above, and $\mathrm{Re}$, $\mathrm{Pr}$ computed from the local gas properties and tube hydraulic diameter.

### Economizer {#sec-gas-eco}

The economizer `economiser` stage reverses the roles: gas flows outside the tubes in cross flow, while water flows inside. The gas side convection is then modelled as external cross flow over a tube bank.

Key geometry quantities (from `GeometryBuilder` for the economizer):

- Tube outer diameter: $D = D_o$
- Gas side cross flow area: $A_\text{bulk} = A_\text{hot,flow}$

- Optional maximum/mean velocity factor:

  $$
  V_\text{bulk} = \frac{\dot{m}_g}{\rho_g A_\text{bulk}},
  \qquad
  V = u_\text{max} V_\text{bulk}
  $$

  where $u_\text{max}$ is calculated depending on the tube bank arrangement and spacing between tubes.

- Reynolds and Prandtl numbers:
  $$
  \mathrm{Re} = \frac{\rho_g V D}{\mu_g},
  \qquad
  \mathrm{Pr} = \frac{c_{p,g}\,\mu_g}{k_g}
  $$

For `"economiser"` stages the primary correlation is a banded Zukauskas form for cross flow over tube banks:

$$
\mathrm{Nu} = C\,\mathrm{Re}^{m}\,\mathrm{Pr}^{n}
$$

[@incropera]

where the coefficients $C, m$ are selected from standard bands as a function of Reynolds number and tube arrangement (`inline` vs `staggered`), and the exponent $n$ is:

$$
n =
\begin{cases}
0.36, & \mathrm{Pr} \le 10 \\
0.25, & \mathrm{Pr} > 10
\end{cases}
$$

If $\mathrm{Re}$ falls outside the tabulated bands, the model falls back to the Churchill–Bernstein correlation for cross flow over a single cylinder:

$$
\mathrm{Nu} = 0.3 \;+\;
\frac{0.62\,\mathrm{Re}^{1/2}\,\mathrm{Pr}^{1/3}}
{\left[1 + (0.4/\mathrm{Pr})^{2/3}\right]^{1/4}}
\left[1 + \left(\frac{\mathrm{Re}}{282000}\right)^{5/8}\right]^{4/5}
$$

[@incropera]
The gas-side convective HTC in the economizer is then:

$$
h_{g,\text{conv}}^\text{(HX6)} = \frac{\mathrm{Nu}\,k_g}{D_o}
$$

[@incropera]

### Radiation model

Radiative heat transfer from the flue gas to the furnace surfaces is explicitly accounted for by a participating medium model for the $H₂O$/$CO₂$ mixture. The implementation follows a simplified Smith–Shen–Friedman style four gray model.

For each step, the gas emissivity is computed as:

1. Partial pressures of participating species:

   $$
   p_{\mathrm{H_2O}} = y_{\mathrm{H_2O}}\,P,
   \qquad
   p_{\mathrm{CO_2}} = y_{\mathrm{CO_2}}\,P
   $$

   [@modest]
   where $y_i$ are molar (or mass-fraction-equivalent) composition entries from the flue gas stream, and $P$ is the local gas pressure.

2. Mean beam length:

   $$
   L_b =
   \begin{cases}
   L_\text{rad,override}, & \text{if specified in the stage} \\
   0.9\,D_{h,\text{gas}}, & \text{otherwise}
   \end{cases}
   $$

   [@modest]
   with $D_{h,\text{gas}}$ the gas-side hydraulic diameter.

3. Effective optical thickness in each gray band:

   $$
   p_\text{ratio} =
   \frac{p_{\mathrm{H_2O}} + p_{\mathrm{CO_2}}}{P_\text{atm}}
   $$

   [@modest]

   $$
   \tau_j = K_j\,\left(\frac{T}{1000\,\mathrm{K}}\right)^{T_\text{exp}}\,p_\text{ratio}\,L_b
   $$

   [@modest]

   where $K_j$ and weighting factors $A_j$ are fixed band coefficients, $T$ is the gas temperature, and $T_\text{exp}$ is a temperature exponent (default 0.65, configurable per stage via `rad_Texp`).

4. Total gas emissivity:
   $$
   \varepsilon_g = 1 - \sum_{j=1}^{4} A_j\,\exp(-\tau_j)
   $$
   [@modest]
   with $\varepsilon_g$ constrained to $[0,1]$.

A mean-film temperature is used for the linearized radiative HTC:

$$
T_\text{film} = \frac{T_g + T_{gw}}{2}
$$

$$
h_{g,\text{rad}} = 4\,\sigma\,F\,\varepsilon_g\,T_\text{film}^3
$$

[@modest]

where:

- $\sigma$ is the Stefan–Boltzmann constant,
- $F$ is an effective view factor (default 1.0 or stage-specific `rad_F`).

The gas-side total HTC reported and used in the resistance network is then:

$$
h_{g,\text{tot}} = h_{g,\text{conv}} + h_{g,\text{rad}}
$$

and the corresponding convective/radiative contributions to the linear heat flux are tracked via:

$$
q'_\text{conv} = q'\,\frac{h_{g,\text{conv}}}{h_{g,\text{tot}}},
\qquad
q'_\text{rad} = q' - q'_\text{conv}
$$

These diagnostics are later integrated on a per-stage basis to quantify the share of convective vs radiative heat transfer in each section of the boiler.

## Water side

Water side heat transfer is computed with geometry dependent correlations using local water properties from IAPWS97 (`WaterProps`), with stage specific geometry from the `GeometryBuilder`. The solver always works with a single effective water side heat transfer coefficient $h_w(x)$ per marching step, which may represent:

- pure pool boiling at a saturated surface,
- a Chen type combination of forced convection and nucleate boiling, or
- single phase forced convection.

In the implementation this logic is encapsulated in `water_htc`, which returns $(h_w)$ for each step.

### General formulation and boiling treatment

The six stages of the boiler are divided, from the water-side point of view, into:

- $\mathrm{HX_1}$–$\mathrm{HX_5}$: pool-boiling stages  
  (`pool_boiling = true` in the stage specification)
- $\mathrm{HX_6}$: economizer stage  
  (`pool_boiling = false`)

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_T-S_chart.png}
\caption{Temperature–entropy ($T$–$s$) representation of the feedwater heating and evaporation process across economiser and boiler at the operating pressure.}
\label{fig:boiler-TS}
\end{figure}

The solver applies the following decision tree at each marching step:

1. Pool-boiling stages ($\mathrm{HX_1}$–$\mathrm{HX_5}$)

   If the stage is flagged as `pool_boiling = true`, the bulk water temperature entering the wall-energy balance is fixed at the saturation temperature at the local pressure:

   $$
   T_w = T_\text{sat}(p_w),
   $$

   and the water-side HTC is computed from the Cooper pool boiling correlation for nucleate boiling correlation:

   $$
   h_\text{Cooper}
   =
   55\, p_r^{\,0.12 - 0.2\log_{10}(R_p)}
   \; \bigl[-\log_{10}(p_r)\bigr]^{-0.55}
   \; q''^{0.67}
   $$

   where

   $$
   p_r = \frac{p}{p_\text{crit}} = \text{reduced pressure}, \quad R_p = \text{surface roughness (μm)}, \quad q'' = \text{heat flux}.
   $$

   [@incropera]

   This nucleate-boiling HTC is then used directly:

   $$
   h_w = h_{w,\text{nb}},
   $$

   and the step is always marked as boiling in the post processing.

   In other words, the main boiling surfaces of the boiler (furnace, passes, reversal chambers) are represented as heated surfaces in a saturated pool, with the HTC governed by the local heat flux and surface roughness rather than by a detailed prediction of liquid velocity. This matches the natural circulation character of these sections.

2. Non pool boiling stages ($\mathrm{HX_6}$, economizer)

   For stages with `pool_boiling = false`, the model can represent both single phase convection and flow boiling via a Chen type formulation.

   a. Boiling detection

   A helper determines whether the local state is boiling based on the bulk enthalpy $h$ and, when needed, the wall temperature $T_\text{wall}$:

   - if
     $$
     h_f(p_w) \le h \le h_g(p_w)
     $$
     the state is inside the saturation interval and is treated as two phase;
   - if $h < h_f(p_w)$ (slightly subcooled liquid) but the wall superheat is sufficiently high,
     $$
     T_\text{wall} > T_\text{sat}(p_w) + \Delta T_\text{crit},
     $$
     the state is also treated as boiling;
   - otherwise the flow is treated as single-phase liquid.

   Here $h_f$ and $h_g$ are saturated-liquid and saturated vapor enthalpies at the local pressure, obtained via IAPWS97.

   b. Single-phase regime

   If boiling is not detected, the water side HTC is purely convective:

   $$
   h_w = h_{w,\text{conv}},
   $$

   with $h_{w,\text{conv}}$ obtained from a geometry dependent forced convection correlation (internal tube, external tube bank, or external single tube/bend) as detailed in Sections [\ref{sec-water-eco}]–[\ref{sec-water-single}].

   c. Flow boiling regime (Chen model)

   When boiling is detected in a non pool boiling stage, the HTC is constructed as a Chen type superposition of:

   - a liquid only convective term $h_\text{lo}$, and
   - a nucleate-boiling term $h_\text{nb}$ using the same Cooper correlation as in pool boiling.

   The liquid only HTC is evaluated at the saturation temperature $T_\text{sat}(p)$ and using the appropriate geometry correlation:

   $$
   h_\text{lo} = h_\text{single-phase}\bigl(T_\text{sat}(p), \text{geometry}\bigr),
   $$

   while the nucleate-boiling term is

   $$
   h_\text{nb} = h_\text{Cooper}(p, q'').
   $$

   The Chen combination used in the code is:

   $$
   h_w = F\,h_\text{lo} + S\,h_\text{nb}.
   $$

   [@incropera]

   The convection enhancement factor $F$ is based on a Martinelli type parameter $X_{tt}$,

   $$
   X_{tt}
   = \left(\frac{1 - x}{x}\right)^{0.9}
     \left(\frac{\mu_l}{\mu_g}\right)^{0.1}
     \left(\frac{\rho_g}{\rho_l}\right)^{0.5},
   $$

   where $x$ is the local vapor quality and $\rho_l,\rho_g,\mu_l,\mu_g$ are liquid/vapor densities and viscosities at saturation. A bounded form of the Chen factor is then used:

   $$
   F = 1 + 0.12\,X_{tt}^{-0.8},
   $$

   The suppression factor $S$ modulating the nucleate boiling contribution is a function of mass flux and Reynolds number:

   $$
   S = \frac{1}{1 + C\,\mathrm{Re}_\text{lo}^{\,\alpha}},
   $$

   where $\mathrm{Re}_\text{lo}$ is a liquid only Reynolds number based on the mass flux

   $$
   G = \frac{\dot{m}_w}{A_\text{flow}},
   $$

   and the liquid properties at saturation. In the implementation the constants and bounds are chosen such that $S$ remains between about 0.1 and 1.0, reducing the nucleate boiling influence at very high mass flux (strong forced convection).

   In the present thesis this Chen type flow boiling capability is only exercised in the economizer stage; the main boiling sections ($\mathrm{HX_1}$–$\mathrm{HX_5}$) use the pure pool boiling representation above.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/water_path.pdf}
\caption{Path of water/steam through the 6 stages}
\label{fig:water_path}
\end{figure}

### Economizer {#sec-water-eco}

In the economizer stage ($\mathrm{HX_6}$, `kind = "economiser"`), water flows inside the tubes and is heated by the flue gas flowing externally in cross flow. This stage is the only one where `pool_boiling = false` and where the full single phase/Chen type boiling formulation is used.

#### Velocity and dimensionless groups {- .unlisted}

The relevant geometric quantities for the water side are:

- tube inner diameter: $D_i$,
- tube length: $L$,
- cold-side flow area: $A_{\text{cold,flow}}$.

The bulk water velocity, Reynolds and Prandtl numbers are:

$$
V_w = \frac{\dot{m}_w}{\rho_w A_{\text{cold,flow}}},
$$

$$
\mathrm{Re}_w = \frac{\rho_w V_w D_i}{\mu_w},
\qquad
\mathrm{Pr}_w = \frac{c_{p,w}\,\mu_w}{k_w},
$$

with $\rho_w, \mu_w, k_w, c_{p,w}$ evaluated from IAPWS97 at the film temperature. [@iapws1997]

#### Single phase internal flow correlation {- .unlisted}

When no boiling is detected in the economizer, the Nusselt number is computed using a Gnielinski type internal flow correlation with a viscosity ratio correction:

- Laminar / developing regime ($\mathrm{Re}_w < 2300$): a Graetz type form is used

  $$
  \mathrm{Gz}_w = \mathrm{Re}_w\,\mathrm{Pr}_w\,\frac{D_i}{L},
  $$

  $$
  \mathrm{Nu}_w = 3.66 + \frac{0.0668\,\mathrm{Gz}_w}{1 + 0.04\,\mathrm{Gz}_w^{2/3}}.
  $$

- Turbulent regime ($\mathrm{Re}\_w \ge 2300$): Gnielinski correlation with friction factor
  $$
  f_w = \left(0.79\ln\mathrm{Re}_w - 1.64\right)^{-2},
  $$
  [@munson]
  $$
  \mathrm{Nu}_w =
  \frac{\frac{f_w}{8}(\mathrm{Re}_w - 1000)\,\mathrm{Pr}_w}
  {1 + 12.7\sqrt{\frac{f_w}{8}}\left(\mathrm{Pr}_w^{2/3}-1\right)},
  $$
  [@incropera]
  scaled by a viscosity-ratio correction:
  $$
  \mathrm{Nu}_w \leftarrow \mathrm{Nu}_w
  \left(\frac{\mu_b}{\mu_w}\right)^{0.11},
  $$
  where $\mu_b$ is evaluated at the bulk temperature and $\mu_w$ at the wall temperature.

The single phase water side HTC in the economizer is then:

$$
h_{w,\text{conv}}^\text{(HX6)} = \frac{\mathrm{Nu}_w\,k_w}{D_i}.
$$

[@incropera]

#### Flow boiling in the economizer {- .unlisted}

If boiling is detected in the economizer (according to the criteria in the general formulation), the same geometry and mass flux information are used to form the liquid only HTC $h_\text{lo}$ and the Cooper nucleate boiling HTC $h_\text{nb}$. The total water side HTC is then:

$$
h_w = F\,h_\text{lo} + S\,h_\text{nb},
$$

with $F$ and $S$ given by the Chen type relations described above, using the local vapor quality, mass flux, and saturation properties. This provides a smooth transition between predominantly convective and predominantly nucleate boiling regimes in the economizer.

### Tube bank stages {#sec-water-bank}

For completeness, the water side model also includes correlations for cross flow over tube banks on the cold side (`kind = "tube_bank"`), although in the present thesis these stages are operated in pool boiling mode (so that only the Cooper correlation is used). When a tube bank description is required on the water side, the geometry is:

- tube outer diameter: $D_o$,
- cold-side flow area: $A_{\text{cold,flow}}$,
- number of rows: $N_\text{rows}$,
- transverse and longitudinal pitches: $S_T$, $S_L$,
- bundle arrangement: `inline` or `staggered`.

The water velocity, Reynolds and Prandtl numbers are:

$$
V_w = \frac{\dot{m}_w}{\rho_w A_{\text{cold,flow}}},
$$

$$
\mathrm{Re}_w = \frac{\rho_w V_w D_o}{\mu_w},
\qquad
\mathrm{Pr}_w = \frac{c_{p,w}\,\mu_w}{k_w}.
$$

A Zukauskas-type banded correlation is then applied:

$$
\mathrm{Nu}_w = C\,\mathrm{Re}_w^m\,\mathrm{Pr}_w^n,
$$

[@incropera]
where:

- $C, m$ are selected from standard Zukauskas bands based on $\mathrm{Re}_w$ and the arrangement (`inline` or `staggered`),
- the exponent $n$ is
  $$
  n =
  \begin{cases}
  0.36, & \mathrm{Pr}_w \le 10\\
  0.25, & \mathrm{Pr}_w > 10
  \end{cases}
  $$

The raw Nusselt number is further modified by:

- a row factor $f_\text{row}(N_\text{rows})$ that accounts for the finite number of tube rows, and
- a spacing factor $\phi(S_T, S_L, D_o)$ that accounts for maximum velocity effects in the tube bank (greater constriction $\Rightarrow$ higher HTC).

If $\mathrm{Re}_w$ falls outside the Zukauskas validity range, the model falls back to the Churchill Bernstein correlation for cross flow over a single cylinder:

$$
\mathrm{Nu}_w =
0.3 +
\frac{0.62\,\mathrm{Re}_w^{1/2}\,\mathrm{Pr}_w^{1/3}}
{\left[1+(0.4/\mathrm{Pr}_w)^{2/3}\right]^{1/4}}
\left[1 + \left(\frac{\mathrm{Re}_w}{282000}\right)^{5/8}\right]^{4/5}.
$$

[@incropera]

The corresponding water side HTC for a tube-bank configuration is:

$$
h_{w,\text{conv}}^\text{(bank)} = \frac{\mathrm{Nu}_w\,k_w}{D_o}.
$$

[@incropera]

When such a tube bank model is used inside the Chen formulation, $h_\text{lo}$ is taken from this $h_{w,\text{conv}}^\text{(bank)}$.

### Single tube and reversal chamber stages {#sec-water-single}

Stages of kind `single_tube` and `reversal_chamber` correspond, on the water side, to external flow around one or more tubes within the drum/shell region. In the current thesis these are also operated in pool boiling mode (`pool_boiling = true`), so the Cooper pool boiling correlation described in the general formulation dominates their behavior. Nevertheless, the implementation includes external forced convection correlations for completeness.

For these stages the characteristic length for the water side is the tube outer diameter $D_o$, and the cold side flow area $A_{\text{cold,flow}}$ is defined by the drum cross section minus the tube area(s). When a cross flow description is used for single-phase or liquid only HTC:

- water velocity, Reynolds and Prandtl numbers:
  $$
  V_w = \frac{\dot{m}_w}{\rho_w A_{\text{cold,flow}}},
  $$
  $$
  \mathrm{Re}_w = \frac{\rho_w V_w D_o}{\mu_w},
  \qquad
  \mathrm{Pr}_w = \frac{c_{p,w}\,\mu_w}{k_w}.
  $$

For a single tube in cross flow (or, by approximation, a relatively open bundle) a Churchill Bernstein style correlation is used:

$$
\mathrm{Nu}_w =
0.3 +
\frac{0.62\,\mathrm{Re}_w^{1/2}\,\mathrm{Pr}_w^{1/3}}
{\left[1+(0.4/\mathrm{Pr}_w)^{2/3}\right]^{1/4}}
\left[1 + \left(\frac{\mathrm{Re}_w}{282000}\right)^{5/8}\right]^{4/5},
$$

[@incropera]
leading to

$$
h_{w,\text{conv}}^\text{(single)} = \frac{\mathrm{Nu}_w\,k_w}{D_o}.
$$

In reversal chamber segments, the tubes are bent, and the model applies the same base correlation multiplied by a curvature (bend) factor:

$$
h_{w,\text{conv}}^\text{(rev)} =
\phi_\text{bend}(D_o, R_c)\,
\frac{\mathrm{Nu}_w\,k_w}{D_o},
$$

where $R_c$ is the bend radius and $\phi_\text{bend} \ge 1$ is a modest enhancement (up to roughly 1.25) for tight bends, reflecting locally increased turbulence around the bend region.

In pool boiling operation these external convection correlations are only used implicitly inside the liquid only component $h_\text{lo}$ when the Chen type formulation is invoked. For the main boiling sections in this thesis, however, the water side is predominantly controlled by the Cooper pool boiling correlation with $T_w = T_\text{sat}(p)$.

\newpage
