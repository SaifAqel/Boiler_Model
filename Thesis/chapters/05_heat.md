# Heat-Transfer Calculations

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

---

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

---

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

---

## Stage- and boiler-level duties

For a stage of length $L_j$, the stage heat duty and stage-level conductance are obtained by integrating the local quantities along $x$:

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

## Gas-side

Gas-side heat transfer is computed with geometry-aware correlations based on local gas properties from Cantera (`GasProps`) and stage-specific geometry from the `GeometryBuilder`. For each marching step, the total gas-side HTC is split into a convective and a radiative contribution:

$$
h_{g,\text{tot}} = h_{g,\text{conv}} + h_{g,\text{rad}}
$$

The implementation uses the helper `gas_htc_parts(g, spec, T_{gw})`, which returns $(h_{g,\text{conv}},\,h_{g,\text{rad}})$ in W/m²·K, and then sums them in `gas_htc`.

---

### Single-tube and reversal-chamber (internal)

Stages of kind `"single_tube"` and `"reversal_chamber"` are treated as internal forced convection in a circular duct. The characteristic quantities are:

- Diameter: $D = D_i$ (tube inner diameter)
- Length: $L$ (stage inner length)
- Flow area: $A = A_\text{hot,flow}$ (from geometry builder)
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
  Local gas properties $\rho_g, \mu_g, k_g, c_{p,g}$ are obtained from the Cantera mixture at the local gas temperature and pressure.

Laminar/developing flow (Graetz-type)  
For $\mathrm{Re} < 2300$, uses a Graetz correlation for thermally developing laminar flow:

$$
\mathrm{Gz} = \mathrm{Re}\,\mathrm{Pr}\,\frac{D}{L}
$$

$$
\mathrm{Nu} = 3.66 \;+\; \frac{0.0668\,\mathrm{Gz}}
{1 + 0.04\,\mathrm{Gz}^{2/3}}
$$

[@incropera]

Turbulent flow (Gnielinski with Petukhov friction factor)  
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

This same internal correlation is used for `"single_tube"`, `"reversal_chamber"` and `"tube_bank"` gas-side flow (see below).

---

### Tube-bank (internal)

Stages `"tube_bank"` correspond to tube bundles inside the shell. In this model, the gas side is still treated as internal flow inside the tubes:

- Hot side (gas): inside tubes (inner diameter $D_i$), using the same internal forced convection model as in Section 5.2.1.

Thus the gas-side convective HTC in tube-bank stages is:

$$
h_{g,\text{conv}}^\text{(HX3,5)} = \frac{\mathrm{Nu}_\text{internal}(\mathrm{Re},\mathrm{Pr})\,k_g}{D_i}
$$

with $\mathrm{Nu}_\text{internal}$ given by the Graetz/Gnielinski formulation above, and $\mathrm{Re}$, $\mathrm{Pr}$ computed from the local gas properties and tube hydraulic diameter.

---

### Economizer (external)

The economizer `"economiser"` stage reverses the roles: gas flows outside the tubes in crossflow, while water flows inside. The gas-side convection is then modelled as external crossflow over a tube bank.

Key geometry quantities (from `GeometryBuilder` for the economizer):

- Tube outer diameter: $D = D_o$
- Gas-side crossflow area: $A_\text{bulk} = A_\text{hot,flow}$

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

For `"economiser"` stages the primary correlation is a banded Zukauskas form for crossflow over tube banks:

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

If $\mathrm{Re}$ falls outside the tabulated bands, the model falls back to the Churchill–Bernstein correlation for crossflow over a single cylinder:

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

---

### Gas radiation model

Radiative heat transfer from the flue gas to the furnace surfaces is explicitly accounted for by a participating-medium model for the $H₂O$/$CO₂$ mixture. The implementation follows a simplified Smith–Shen–Friedman style four-gray model.

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

## Water-side

Water-side heat transfer is modelled with geometry-dependent correlations using local water properties from the `WaterProps` helper. The water side appears in two configurations:

1. Water inside tubes (economizer)
2. Water outside tubes in crossflow ($\mathrm{HX_1}$-$\mathrm{HX_5}$)

The total water-side HTC is computed at each marching step as:

$$
h_w = h_{w,\text{conv}}
$$

Water-side radiation is neglected.

In the present work, the water-side model is used in two distinct regimes:

- HX*1–HX_5 are treated as boiling surfaces in contact with a pool at saturation temperature. In these stages the bulk water temperature is forced to $T*\text{sat}(p)$ and the heat-transfer coefficient is obtained from a pure pool-boiling correlation.
- HX_6 (economizer) is treated as a single-phase / flow-boiling tube bundle with water flowing inside the tubes and heated by the flue-gas crossflow.

The underlying implementation is more general (it contains a full Chen-type flow-boiling formulation valid for internal forced convection), but for the final boiler calculations this capability is only used in the economizer; in HX_1–HX_5 the water side is deliberately simplified to a pool-boiling model.

---

### Economizer (internal)

For the economiser stage (kind `"economiser"`, $\mathrm{HX_6}$), where water flows inside the tubes, the model uses standard internal-flow correlations augmented with a viscosity-ratio correction and, when needed, a Chen-type flow-boiling enhancement. The tube inner diameter $D_i$ is used as characteristic length.

#### Velocity and nondimensional groups

$$
V_w = \frac{\dot{m}_w}{\rho_w A_{\text{cold,flow}}}
$$

$$
\mathrm{Re}_w = \frac{\rho_w V_w D_i}{\mu_w},
\qquad
\mathrm{Pr}_w = \frac{c_{p,w}\,\mu_w}{k_w}
$$

Local water-side properties $\rho_w, \mu_w, k_w, c_{p,w}$ are evaluated at the bulk water temperature.

#### Laminar regime ($\mathrm{Re}<2300$)

For fully developed laminar internal flow in a circular tube:

$$
\mathrm{Nu}_w = 3.66
$$

[@incropera]
For developing laminar flow, the same Graetz form used on the gas side is applied:

$$
\mathrm{Gz}_w = \mathrm{Re}_w \,\mathrm{Pr}_w\,\frac{D_i}{L}
$$

$$
\mathrm{Nu}_w = 3.66 + \frac{0.0668\,\mathrm{Gz}_w}{1 + 0.04\,\mathrm{Gz}_w^{2/3}}
$$

[@incropera]

#### Turbulent regime ($\mathrm{Re}\ge 2300$)

The Gnielinski correlation is used:

$$
f_w = \left(0.79\ln\mathrm{Re}_w - 1.64\right)^{-2}
$$

[@munson]

$$
\mathrm{Nu}_w =
\frac{\frac{f_w}{8}(\mathrm{Re}_w - 1000)\,\mathrm{Pr}_w}
{1 + 12.7\sqrt{\frac{f_w}{8}}\left(\mathrm{Pr}_w^{2/3}-1\right)}
$$

[@incropera]
In the implementation, the Nusselt number is multiplied by a viscosity-ratio correction $(\mu_b/\mu_w)^{0.11}$ evaluated at bulk and wall temperatures, following the common Gnielinski extension for heated internal flow.

Finally:

$$
h_{w,\text{conv}} = \frac{\mathrm{Nu}_w\,k_w}{D_i}
$$

[@incropera]

---

### Tube-bank (external)

In the boiling sections ($\mathrm{HX_1}$–$\mathrm{HX_5}$) the water occupies the shell-side region around the heated tubes. When a crossflow description is needed (e.g. in HX_3 and HX_5), a Zukauskas-type correlation is applied for flow over a tube bundle on the water side, using the outer tube diameter $D_o$ and the cold-side flow area $A*{\text{cold,flow}}$ supplied by the geometry builder.

#### Geometry inputs from `GeometryBuilder`

- Tube outer diameter: $D_o$
- Cold-side flow area: $A_{\text{cold,flow}}$

- Water velocity:

  $$
  V_w = \frac{\dot{m}_w}{\rho_w A_{\text{cold,flow}}}
  $$

- Reynolds and Prandtl numbers:
  $$
  \mathrm{Re}_w = \frac{\rho_w V_w D_o}{\mu_w},
  \qquad
  \mathrm{Pr}_w = \frac{c_{p,w}\,\mu_w}{k_w}
  $$

#### Zukauskas banded correlation

$$
\mathrm{Nu}_w = C\,\mathrm{Re}_w^m\,\mathrm{Pr}_w^n
$$

Coefficient selection:

- $C,m$ chosen based on the Reynolds band and bundle arrangement (`inline` or `staggered`).
- Exponent $n$:
  $$
  n =
  \begin{cases}
  0.36, & \mathrm{Pr}_w \le 10\\
  0.25, & \mathrm{Pr}_w > 10
  \end{cases}
  $$

If the Reynolds number lies outside the valid Zukauskas range, the model falls back to Churchill–Bernstein:

$$
\mathrm{Nu}_w =
0.3 +
\frac{0.62\,\mathrm{Re}_w^{1/2}\,\mathrm{Pr}_w^{1/3}}
{\left[1+(0.4/\mathrm{Pr}_w)^{2/3}\right]^{1/4}}
\left[1 + \left(\frac{\mathrm{Re}_w}{282000}\right)^{5/8}\right]^{4/5}
$$

[@incropera]

The external HTC is then:

$$
h_{w,\text{conv}} = \frac{\mathrm{Nu}_w\,k_w}{D_o}
$$

---

### Treatment of boiling

Boiling is treated differently in the pool-boiling stages (HX_1–HX_5) and in the economiser (HX_6).

#### Pool-boiling

For stages flagged as `pool_boiling = true` (HX_1–HX_5), the water side is deliberately simplified to a pure pool-boiling model:

- The bulk water temperature entering the wall-energy balance is fixed at the saturation temperature corresponding to the local pressure:
  $$
  T_w = T_\text{sat}(p_w).
  $$
- The water-side heat-transfer coefficient is taken from a Cooper-type pool-boiling correlation:

  $$
  h_{w,\text{nb}} = h_\text{Cooper}(p_w, q'')
  $$

  [@incropera]
  where $q''$ is the local heat flux on the water side and the roughness of the boiling surface enters through the correlation.

- This nucleate-boiling coefficient is used directly as the water-side HTC:
  $$
  h_w = h_{w,\text{nb}},
  $$
  and the region is always tagged as “boiling” in the post-processing.

In other words, HX_1–HX_5 are modelled as heated surfaces immersed in a saturated pool, with boiling controlled by the local heat flux and surface roughness rather than by a detailed prediction of the liquid velocity. This reflects the natural-circulation behavior of the boiler riser and furnace sections and follows the modelling simplification requested for the thesis.

#### Economizer

For the economizer stage HX_6 (`pool_boiling = false`), the model uses a more general internal-flow formulation that can represent both single-phase convection and flow boiling:

1. Boiling detection.  
   A helper function checks whether the local state falls into the saturation enthalpy interval $[h_f(p), h_g(p)]$ or, for slightly subcooled liquid, whether the wall superheat exceeds a threshold. If neither condition is met, the flow is treated as single-phase liquid.

2. Single-phase regime.  
   In single-phase operation, the water-side HTC is computed from an internal forced-convection correlation (Gnielinski with viscosity-ratio correction), as described in Section 5.3.1.

3. Flow-boiling regime (Chen-type model).  
    When boiling is detected, the HTC is assembled from a liquid-only contribution and a nucleate-boiling contribution:
   $$
   h_\text{lo} = \text{single-phase liquid HTC at } T_\text{sat}(p),
   $$
   $$
   h_\text{nb} = h_\text{Cooper}(p, q''),
   $$
   $$
   h_w = F\,h_\text{lo} + S\,h_\text{nb}.
   $$
   [@incropera]
   The factor $F$ accounts for the effect of two-phase flow on the convective heat transfer (via a Martinelli-type parameter), while $S$ modulates the nucleate-boiling contribution as a function of Reynolds number and mass flux. Both are bounded to remain within reasonable engineering limits.

In the present thesis, this full Chen-type flow-boiling capability is only exercised in the economizer stage. In the main boiling sections (HX_1–HX_5), where circulation is dominated by buoyancy and the flow pattern is closer to pool boiling, the simpler pool-boiling representation described above is preferred.

---

## Per-step resistance insertion

The water-side resistance per unit length used in the overall $UA'$ assembly is:

$$
R_c' = \frac{1}{h_w P_w}
$$

where the wetted perimeter is:

- $P_w = \pi D_i$ when water is inside the tubes.
- $P_w = N_{\text{tubes}} \pi D_o$ effective per bundle pitch when water is outside tubes, handled automatically by `GeometryBuilder`.

Fouling is added in series:

$$
R_{fc}' = \frac{\delta_{f,\text{water}}}{k_{f,\text{water}}\,P_w}
$$

Total water-side contribution:

$$
R_{w,\text{side}}' = R_{fc}' + R_c'
$$

This resistance is passed into the overall conductance formulation (Section 5.1.2).

---

## Wall-temperature update and thermal convergence

The tube wall temperatures on the gas and water sides, $T_{gw}$ and $T_{ww}$, are updated using a two-node wall model in each marching step.

Given $q'(x)$, the wall-side energy balances yield:

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

A consistency check is applied; if the implied wall temperature difference from conduction differs from the one implied by convection, the marching solver iterates the HTC evaluation once with relaxed updates (default under-relaxation factor 0.35). Full Picard iteration is omitted for performance reasons.

In the actual implementation this consistency check is performed by iterating on $T_{gw}$, $T_{ww}$, and $q'$ using the full resistance network (gas convection, gas fouling, wall, water fouling, water convection), with an under-relaxation factor applied to both wall temperatures and the linear heat flux.

If temperature overshoot (negative film coefficient, reversed driving force) is detected within a step, the step is automatically halved and recomputed.

\newpage
