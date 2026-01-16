# Heat Transfer Model

This model simulates heat transfer from hot flue gas to the water/steam mixture in the drum, flue gas entering first pass, is specified by the results of the combustion model, and water entering the economizer, specified by user at $105^{\circ}\text{C}$ temperature with the mass flow to be calculated iteratively until convergence of water in and steam produced.

## Fundamental heat balance equations

The boiler is modelled as a one dimensional counter current heat exchanger composed of six stages ($\mathrm{HX_1}$–$\mathrm{HX_6}$). Heat transfer is resolved along the gas flow direction $x$, while water flows in the opposite direction. Each stage is discretized into segments of length $\mathrm{d}x$; all local quantities are defined per unit length.

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

For each differential segment of length $\mathrm{d}x$, the model enforces a one dimensional steady state energy balance between the gas, the water and the tube wall:

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

In the numerical implementation these equations are applied in finite difference form over each marching step:

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

- Gas side convection:

  $$
  R_g' = \frac{1}{h_g(x)\,P_g}
  $$

- Gas side fouling:

  $$
  R_{fg}' = R_{fi}'(P_g) \quad\text{(from specified fouling thickness and conductivity)}
  $$

- Tube wall:

  $$
  R_w' = \frac{\ln\!\bigl(D_o/D_i\bigr)}{2\pi k_w}
  $$

- Water side fouling:

  $$
  R_{fc}' = R_{fo}'(P_w)
  $$

- Water side convection:
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
T_{gw} = T_g - \frac{q'}{{h_{g,\text{tot}}}{P_g }}
$$

$$
T_{ww} = T_w + \frac{q'}{{h_w}{P_w}}
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

A consistency check is applied; if the implied wall temperature difference from conduction differs from the one implied by convection, the marching solver iterates the HTC evaluation once with relaxed updates.

In the actual implementation this consistency check is performed by iterating on $T_{gw}$, $T_{ww}$, and $q'$ using the full resistance network (gas convection, gas fouling, wall, water fouling, water convection), with an under-relaxation factor applied to both wall temperatures and the linear heat flux.

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

These integrated quantities are later used in the performance and efficiency evaluation (Chapter 7) and for constructing stage-wise summary tables.

## Heat Transfer Coefficient

### Gas side

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

#### Internal flow

Stages of kind `single_tube`, `reversal_chamber`, and `tube_bank` corresponding to furnace (first pass), both reversal chambers, and both tube banks are treated as internal forced convection in a circular duct. The characteristic quantities are:

- Diameter: $D$ (supplied by `stages.yaml`)
- Length: $L$ (supplied by `stages.yaml`)
- Tubes number: $n$ (supplied by `stages.yaml` for tube banks)
- Flow area: $A = \frac{1}{4}\pi n D^2$ (calculated by geometry builder)
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

##### Laminar/developing flow (Graetz-type) {- .unlisted}

For $\mathrm{Re} < 2300$, uses a Graetz correlation for thermally developing laminar flow:

$$
\mathrm{Gz} = \mathrm{Re}\,\mathrm{Pr}\,\frac{D}{L}
$$

$$
\mathrm{Nu} = 3.66 \;+\; \frac{0.0668\,\mathrm{Gz}}
{1 + 0.04\,\mathrm{Gz}^{2/3}}
$$

[@incropera]

##### Turbulent flow (Gnielinski with Petukhov friction factor) {- .unlisted}

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

#### Cross flow

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

#### Radiation model

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

### Water side

Water side heat transfer is computed with geometry dependent correlations using local water properties from IAPWS97 (`WaterProps`), with stage specific geometry from the `GeometryBuilder`. The solver always works with a single effective water side heat transfer coefficient $h_w(x)$ per marching step, which may represent:

- pure pool boiling at a saturated surface,
- single phase forced convection.

In the implementation this logic is encapsulated in `water_htc`, which returns $(h_w)$ for each step.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_T-S_chart.png}
\caption{Temperature–entropy ($T$–$s$) representation of the feedwater heating and evaporation process across economiser and boiler at the operating pressure (reproduced from \cite{heat_engines_lecture7}).}
\label{fig:boiler-TS}
\end{figure}

The six stages of the boiler are divided, from the water-side point of view, into:

- $\mathrm{HX_1}$–$\mathrm{HX_5}$: pool-boiling stages  
  (`pool_boiling = true` in the stage specification)
- $\mathrm{HX_6}$: economizer stage  
  (`pool_boiling = false`)

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/water_path.pdf}
\caption{Path of water/steam through the 6 stages}
\label{fig:water_path}
\end{figure}

#### Internal Flow

In the economiser stage ($\mathrm{HX_6}$), feedwater flows inside tubes and is heated by flue gas in external crossflow.  
The water remains in the single-phase liquid region throughout this section, and the water-side heat transfer coefficient is therefore computed using forced convection correlations for internal flow.

Stages of kind `single_tube`, `reversal_chamber`, and `tube_bank` corresponding to furnace (first pass), both reversal chambers, and both tube banks are treated as internal forced convection in a circular duct. The characteristic quantities are:

- Diameter: $D$ (supplied by `stages.yaml`)
- Length: $L$ (supplied by `stages.yaml`)
- Tubes number: $n$ (supplied by `stages.yaml` for tube banks)
- Flow area: $A = \frac{1}{4}\pi n D^2$ (calculated by geometry builder)
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

##### Laminar/developing flow {- .unlisted}

For $\mathrm{Re} < 2300$, uses a Graetz correlation for thermally developing laminar flow:

$$
\mathrm{Gz} = \mathrm{Re}\,\mathrm{Pr}\,\frac{D}{L}
$$

$$
\mathrm{Nu} = 3.66 \;+\; \frac{0.0668\,\mathrm{Gz}}
{1 + 0.04\,\mathrm{Gz}^{2/3}}
$$

[@incropera]

##### Turbulent flow {- .unlisted}

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

A viscosity correction is applied:

$$
\mathrm{Nu}_w \leftarrow \mathrm{Nu}_w
\left(\frac{\mu_b}{\mu_w}\right)^{0.11}.
$$

[@incropera]

The local convective heat-transfer coefficient is then:

$$
h_{g,\text{conv}} = \frac{\mathrm{Nu}\,k_g}{D}
$$

[@incropera]

#### Pool Boiling

The main boiler heating surfaces ($\mathrm{HX_1}$–$\mathrm{HX_5}$) are modelled as pool boiling surfaces immersed in saturated water at the local pressure.  
These sections represent the furnace walls, passes, and reversal chambers, where heat transfer is governed primarily by nucleate boiling rather than by a well-defined bulk liquid velocity.

For these stages, the bulk water temperature entering the wall energy balance is fixed at the saturation temperature:

$$
T_w = T_\text{sat}(p_w).
$$

The water-side heat transfer coefficient is computed using the Cooper correlation for nucleate pool boiling:

$$
h_\text{nb}
=
55\,
p_r^{0.12}\,
R_p^{-0.55}\,
M_\mathrm{w}^{-0.5}\,
\bigl(q''\bigr)^{0.67},
$$

[@cooper1984_poolboiling]

where

$$
p_r = \frac{p}{p_\text{crit}},
$$

$R_p$ is the surface roughness in $\mu$m, $M_\mathrm{w}$ is the molecular weight of water, and $q''$ is the local heat flux.

The resulting coefficient is used directly:

$$
h_w = h_\text{nb}.
$$

This approach reflects the natural circulation character of the boiler, where boiling heat transfer is dominated by surface conditions and heat flux rather than by forced convection effects.

\newpage
