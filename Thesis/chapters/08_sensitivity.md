# Sensitivity Analysis

This chapter evaluates how the coupled combustion–boiler model responds to variations in three key operating parameters:

- excess air ratio $\lambda$,
- feedwater (drum) pressure,
- fuel mass flow rate (firing rate).

The goal is to quantify how these parameters influence the boiler-level quantities introduced in Chapter&nbsp;7, in particular:

- total useful heat transferred to the water/steam side $Q_\text{useful}$,
- total heat input from combustion $Q_\text{in}$,
- direct and indirect efficiencies $\eta_{\text{direct}}$, $\eta_{\text{indirect}}$,
- stack gas temperature $T_\text{stack}$,
- overall gas-side pressure drop $\Delta P_\text{boiler}$,
- converged water/steam mass flow $\dot{m}_w$.

All sensitivity cases reuse the same geometry, combustion model and heat-transfer model as in Chapters 3–6. Only the selected operating variable is changed in each series, while the remaining inputs are kept at the control values.

---

## Control case

The control case is the reference operating point against which all sensitivity results are compared. It corresponds to the unmodified configuration in the YAML input files and is executed by

- `run_default_case()` in `main.py`, which calls
- `run_boiler_case()` in `boiler_loop.py` with no overrides and `run_id="default_case"`.

The control case thus uses:

- Geometry: drum and stages from `config/drum.yaml` and `config/stages.yaml` (Chapter&nbsp;3).
- Fuel composition and base mass flow: from `config/fuel.yaml` (Chapter&nbsp;4).
- Air composition: from `config/air.yaml` (Chapter&nbsp;4).
- Excess air ratio:

  $$
  \lambda_\text{base} = \texttt{operation["excess\_air\_ratio"]}
  $$

  specified in `config/operation.yaml`.

- Feedwater state: pressure and enthalpy from `config/water.yaml`.
- Heat-transfer and hydraulic models: as described in Chapters 5–6.

### Control-case solution procedure

For any given operating condition (including the control case) the main solver `run_boiler_case()` performs an outer fixed-point iteration on boiler efficiency and water mass flow:

1. The combustion sub-model (`Combustor.run()`) computes a `CombustionResult` containing

   - the lower-heating-value-based firing rate $P_\text{LHV}$,
   - the total combustion heat release $Q_\text{in}$,
   - the adiabatic flame temperature $T_\text{ad}$,
   - the fully burnt flue-gas stream at burner exit.

2. Given a current efficiency guess ${\eta}^{(n)}$ and the combustion result, the corresponding feedwater/steam mass flow $\dot{m}_w^{(n)}$ is computed by `_water_mass_from_efficiency()` as

   $$
   Q_\text{in} = \text{CombustionResult}.Q_\text{in},
   $$

   $$
   h_\text{in} = h_\text{fw}(P_\text{fw}), \qquad
   h_\text{steam} = h_g(P_\text{fw}),
   $$

   $$
   \Delta h = h_\text{steam} - h_\text{in},
   $$

   $$
   Q_\text{target}^{(n)} = \eta^{(n)}\,Q_\text{in},
   $$

   $$
   \dot{m}_w^{(n)} = \frac{Q_\text{target}^{(n)}}{\Delta h}.
   $$

   This is implemented as:

   ```python
   Q_in    = combustion.Q_in.to("W")
   h_in    = water_template.h.to("J/kg")
   h_steam = WaterProps.h_g(water_template.P).to("J/kg")
   delta_h = (h_steam - h_in).to("J/kg")
   Q_target = (eta * Q_in).to("W")
   m_w      = (Q_target / delta_h).to("kg/s")
   ```

3. A `WaterStream` with mass flow $\dot{m}_w^{(n)}$ is created and passed, together with the combustion flue gas and the drum/stage definitions, to the multi-stage heat-exchanger solver `run_hx(...)`.

4. `run_hx` returns per-stage and boiler-level summary rows. From the `TOTAL_BOILER` row the post-processor `summary_from_profile(...)` recovers the indirect efficiency

   $$
   \eta_{\text{indirect}}^{(n)} = \frac{Q_\text{useful}^{(n)}}{Q_\text{in}}.
   $$

5. The new efficiency estimate is set to the indirect efficiency,

   $$
   \eta^{(n+1)} := \eta_{\text{indirect}}^{(n)},
   $$

   and the procedure is repeated until the change in water mass flow between iterations is below the specified tolerance

   $$
   \left|\dot{m}_w^{(n)} - \dot{m}_w^{(n-1)}\right| < 10^{-3}\,\mathrm{kg/s},
   $$

   or a maximum number of iterations is reached.

At convergence, the control case yields a unique pair:

- converged water/steam mass flow $\dot{m}_{w,\text{base}}$,
- converged indirect efficiency $\eta_{\text{indirect,base}}$,

together with the corresponding boiler summary quantities (stack temperature, total pressure drop, etc.). These are exported to CSV as `default_case_boiler_summary.csv` via `write_results_csvs(...)` and form the reference for the sensitivity analysis.

---

## Methodology for sensitivity runs

All sensitivity studies use the same numerical procedure as the control case and differ only in how one input parameter is modified. The helper function `run_boiler_case(...)` accepts optional override dictionaries for:

- `operation_overrides` (e.g. `{"excess_air_ratio": Q_(ea, "")}`),
- `water_overrides` (e.g. `{"P": Q_(P_bar, "bar")}`),
- `fuel_overrides` (e.g. `{"mass_flow": Q_(mdot, "kg/s")}`),

which temporarily modify the corresponding YAML-derived objects before each run.

For each value in a parameter sweep:

1. The relevant override is applied.
2. Combustion is recomputed for the new condition.
3. The outer mass-flow/efficiency iteration is executed until convergence.
4. Three CSV files are written to disk for later post-processing:

   - `<run_id>_steps.csv` – per-step marching data,
   - `<run_id>_stages_summary.csv` – per-stage heat-transfer and pressure-drop data,
   - `<run_id>_boiler_summary.csv` – boiler-level performance summary.

Each sweep is controlled by a dedicated function in `main.py`:

- `run_excess_air_sensitivity()` – excess air ratio,
- `run_water_pressure_sensitivity()` – feedwater/drum pressure,
- `run_fuel_flow_sensitivity()` – fuel mass flow.

In each case the parameter is varied one-factor-at-a-time (OFAT), i.e. only the parameter of interest is changed, while all other inputs remain at their control values.

The analysis in this chapter is based on plots and tables generated from the boiler-summary CSVs of these runs. Wherever possible, trends are discussed in terms of dimensionless relative changes, e.g.

$$
\Delta \eta_{\text{indirect}}^\% =
\frac{\eta_{\text{indirect}} - \eta_{\text{indirect,base}}}
     {\eta_{\text{indirect,base}}} \times 100\%.
$$

---

## Excess Air Ratio

### Simulation setup {#sec-lambda-setup}

The effect of excess air on boiler performance is investigated by the function
`run_excess_air_sensitivity()` in `main.py`. The following values of the excess air ratio $\lambda$ are considered:

- $\lambda = 1.0,\, 1.1,\, 1.2,\, 1.3$.

For each value, the boiler loop is executed as

```python
run_boiler_case(
    operation_overrides={"excess_air_ratio": Q_(ea, "")},
    eta_guess=Q_(0.90, ""),
    tol_m=Q_(1e-3, "kg/s"),
    max_iter=20,
    write_csv=True,
    run_id=f"excess_air_{ea}",
)
```

All other configuration files (`stages.yaml`, `fuel.yaml`, `air.yaml`, `water.yaml`, `drum.yaml`) are left unchanged relative to the control case. The fuel mass flow is therefore constant across the excess-air sweep, so the chemical heat input on an LHV basis $P_\text{LHV}$ remains fixed. What changes with $\lambda$ is:

- the air mass flow and hence total flue-gas mass flow,
- the flue-gas composition (residual $\mathrm{O_2}$ level, minor change in $CO_2$ and $H_2O$ fractions),
- the adiabatic flame temperature $T_\text{ad}$,
- the gas-side convective and radiative driving forces in all stages.

For each $\lambda$, the final boiler summary provides:

- $Q_\text{useful}(\lambda)$,
- $Q_\text{in}(\lambda)$ (combustion heat release),
- $\eta_\text{direct}(\lambda)$, $\eta_\text{indirect}(\lambda)$,
- stack gas temperature $T_\text{stack}(\lambda)$,
- total gas-side pressure drops $\Delta P_\text{fric}(\lambda)$, $\Delta P_\text{minor}(\lambda)$, $\Delta P_\text{total}(\lambda)$,
- converged water/steam mass flow $\dot{m}_w(\lambda)$.

### Observed trends {#sec-lambda-observed}

The simulation results are consistent with textbook expectations for gas-fired boilers:

- As $\lambda$ increases above stoichiometric conditions, the adiabatic flame temperature decreases due to the additional inert air mass that must be heated. This reduces the radiative heat transfer in the furnace (HX$_1$) and, to a lesser extent, the convective temperature differences in subsequent passes.
- At the same time, the larger air and flue-gas mass flow raise the stack loss $Q_\text{loss,stack}$, because more mass leaves the boiler at high temperature even if the temperature itself decreases moderately.

In terms of efficiency:

- The indirect efficiency $\eta_\text{indirect}(\lambda)$ typically exhibits a shallow maximum in the vicinity of the design excess air ratio specified for the control case (here $\lambda \approx 1.1$). For $\lambda$ significantly below this value, incomplete combustion would start to appear in a real boiler; in the present model, which assumes complete burnout, this is manifested mainly as a reduction in available excess $O_2$ and higher $T_\text{ad}$.
- For $\lambda$ increased from the base value towards 1.3, the simulations show a gradual decrease in both $\eta_\text{direct}$ and $\eta_\text{indirect}$, reflecting the growing stack loss.

Regarding stack temperature and pressure drop:

- The stack temperature $T_\text{stack}(\lambda)$ changes more mildly than the efficiency. The dominant effect of excess air on efficiency comes from the increased flue-gas mass flow rather than a large change in exit temperature.
- The total gas-side pressure drop $\Delta P_\text{boiler}$ increases with $\lambda$ because the flue-gas density and velocity change: higher volumetric flow rates in the same geometry yield higher dynamic pressures and thus larger frictional losses.

### Interpretation {#sec-lambda-interpretation}

Operationally, the excess air ratio is adjusted to reconcile three competing objectives:

1. Complete combustion with sufficiently low CO and unburned hydrocarbons.
2. Acceptable NO$_x$ emissions (not explicitly modelled here but strongly linked to $T_\text{ad}$).
3. High boiler efficiency (low stack loss).

The present simulations quantify how sensitive the boiler efficiency and stack conditions are to realistic variations in $\lambda$ around the design value. They confirm that modest deviations in excess air lead to measurable, but not catastrophic, efficiency penalties and provide a basis for selecting control set-points in practice.

---

## Drum / feedwater pressure

### Simulation setup {#sec-pressure-setup}

The influence of pressure on boiler performance is studied by varying the feedwater (and implicitly drum) pressure using `run_water_pressure_sensitivity()` in `main.py`. The investigated absolute pressure levels are:

- $P_\text{fw} = 4\,\text{bar},\;10\,\text{bar},\;16\,\text{bar}$.

For each value, the boiler loop is executed as:

```python
run_boiler_case(
    water_overrides={"P": Q_(P_bar, "bar")},
    eta_guess=Q_(0.90, ""),
    tol_m=Q_(1e-3, "kg/s"),
    max_iter=20,
    write_csv=True,
    run_id=f"water_pressure_{P_bar}bar",
)
```

The override replaces the feedwater pressure in the `WaterStream` object used as template in `_water_mass_from_efficiency()`. The same pressure is also used for saturation properties in the drum and boiling surfaces via `WaterProps`.

For a given pressure $P$, the saturation temperature and phase-change enthalpy are

$$
T_\text{sat}(P) = \text{WaterProps.Tsat}(P),
$$

$$
h_\text{f}(P) = \text{WaterProps.h\_f}(P), \qquad h_\text{g}(P) = \text{WaterProps.h\_g}(P),
$$

and the enthalpy rise per kg of steam is

$$
\Delta h(P) = h_g(P) - h_\text{fw}(P),
$$

with $h_\text{fw}$ taken from the inlet water enthalpy in `water.yaml` at the new pressure.

### Observed trends {#sec-pressure-observed}

The simulation series highlights the following qualitative effects:

- As pressure increases, the saturation temperature rises. Consequently, the mean water/steam temperature in the boiling sections (HX$_1$–HX$_5$) increases, and the temperature difference between flue gas and boiling surfaces is reduced, especially towards the cooler end of the gas path.
- The latent heat of vaporisation per unit mass decreases with pressure. For the same useful heat duty $Q_\text{useful}$, a higher-pressure boiler therefore requires a larger enthalpy rise in the feedwater but a smaller contribution from phase change.

For the converged performance measures:

- The steam mass flow $\dot{m}_w(P)$ produced for a given $Q_\text{in}$ decreases with increasing pressure, as expected from

  $$
  \dot{m}_w(P) =
  \frac{\eta_\text{indirect}(P)\,Q_\text{in}}{\Delta h(P)}.
  $$

  Even if $\eta_\text{indirect}$ remains nearly constant, the reduction in $\Delta h(P)$ with pressure leads to a lower steam capacity in $\text{t/h}$.

- The indirect efficiency $\eta_\text{indirect}(P)$ generally varies only weakly across the investigated pressure range, because the global energy balance is dominated by the same firing rate and similar overall gas-to-water temperature profiles. Small changes arise from the altered water-side heat-transfer coefficients and the different mean temperature levels in each stage.
- The stack temperature $T_\text{stack}(P)$ is influenced by two competing mechanisms:
  - at higher pressures, the water/steam is hotter, which tends to extract more sensible heat from the flue gas;
  - however, the reduced steam mass flow and altered boiling behaviour modify the stage-wise duties and may slightly increase or decrease $T_\text{stack}$ depending on the detailed balance.

In the simulated cases the net impact on both efficiency and stack temperature is moderate compared with the effect of excess air.

### Interpretation {#sec-pressure-interpretation}

From a design and operational viewpoint, the pressure sensitivity study illustrates that:

- The primary effect of increasing drum pressure at fixed firing rate is a change in steam _quantity_ rather than a dramatic change in boiler _efficiency_.
- Higher-pressure operation delivers steam at higher temperature and higher specific exergy but at lower mass flow for the same $Q_\text{in}$. This is consistent with the thermodynamic trade-offs discussed in Chapter&nbsp;2.
- For medium-pressure shell boilers in the investigated range, the model suggests that efficiency penalties associated purely with pressure changes are relatively small, provided that other parameters (notably excess air and heat-transfer surface cleanliness) are kept under control.

---

## Fuel mass-flow rate (firing rate)

### Simulation setup {#sec-fuel-setup}

The sensitivity of boiler performance to firing rate is assessed by varying the fuel mass flow in `run_fuel_flow_sensitivity()` in `main.py`. The following fuel mass-flow rates are considered:

- $\dot{m}_f = 0.10,\, 0.075,\, 0.050,\, 0.025\ \mathrm{kg/s}$.

Each case is run as:

```python
run_boiler_case(
    fuel_overrides={"mass_flow": Q_(mdot, "kg/s")},
    eta_guess=Q_(0.90, ""),
    tol_m=Q_(1e-3, "kg/s"),
    max_iter=20,
    write_csv=True,
    run_id=f"fuel_flow_{mdot}kgs",
)
```

For each $\dot{m}_f$ the combustion model recomputes:

- the firing rate on an LHV basis

  $$
  P_\text{LHV}(\dot{m}_f) =
  \dot{m}_f \, \text{LHV}_\text{mix},
  $$

- the total heat input $Q_\text{in}(\dot{m}_f)$,
- the adiabatic flame temperature (slightly dependent on fuel/air preheat and composition),
- the fully burnt flue-gas mass flow and composition.

The excess air ratio $\lambda$, geometry, and feedwater/drum pressure are kept at their control-case values.

### Observed trends {#sec-fuel-observed}

The fuel-flow sweep explores a range from very low to comparatively high firing rates. The main qualitative trends observed in the simulations are:

- The useful duty $Q_\text{useful}(\dot{m}_f)$ scales approximately linearly with the firing rate, as long as the boiler remains within its designed heat-transfer capacity and no severe pinch in temperature difference occurs at either end of the flue-gas path.
- The converged water/steam mass flow $\dot{m}_w(\dot{m}_f)$ also increases roughly proportionally with $\dot{m}_f$, according to

  $$
  \dot{m}_w(\dot{m}_f) \approx
  \frac{\eta_\text{indirect}(\dot{m}_f)\,Q_\text{in}(\dot{m}_f)}{\Delta h},
  $$

  with $\Delta h$ fixed by the pressure and feedwater enthalpy.

- The boiler efficiencies $\eta_\text{direct}$ and $\eta_\text{indirect}$ remain relatively flat across the central part of the firing-range, with mild degradation at very low loads. This behaviour is typical:

  - at low firing rates the gas-side convective coefficients decrease (lower Reynolds numbers), and a larger fraction of the surface area operates at small temperature differences, which increases relative losses;
  - at high firing rates, gas-side heat-transfer coefficients improve, but the approach to pinch points and increased stack temperatures can offset some of the gains.

- The total gas-side pressure drop $\Delta P_\text{boiler}(\dot{m}_f)$ increases significantly with firing rate due to the quadratic dependence on velocity:

  $$
  \Delta P_{\mathrm{fric}} \propto f \frac{L}{D_h}\left(\frac{\rho V^2}{2}\right),
  $$

  where the mass flux and velocity grow approximately in proportion to $\dot{m}_f$. This is particularly noticeable in the furnace and tube-bank stages (HX$_1$, HX$_3$, HX$_5$).

- Stack temperature $T_\text{stack}(\dot{m}_f)$ tends to rise slightly with firing rate once the boiler surfaces approach their design heat flux limits, because a smaller fraction of the additional heat input can be absorbed before the gas reaches the stack.

### Interpretation {#sec-fuel-interpretation}

From an operational standpoint, the firing-rate sensitivity highlights the practical load range of the modeled boiler:

- In the mid-load region the boiler behaves nearly “proportionally”: steam capacity and useful duty increase roughly linearly with fuel input, and efficiency remains close to the control-case value.
- At very low loads the model indicates a deterioration of heat-transfer effectiveness and efficiency, consistent with the well-known part-load penalties of shell boilers (more cycling, lower gas velocities, increased relative losses).
- At the upper end of the firing range, the rising pressure drop and stack temperature suggest that fan capacity and allowable stack losses will ultimately limit further increases in $\dot{m}_f$, even if the geometry could accommodate higher heat fluxes.

---

## Summary

The sensitivity analysis presented in this chapter shows that:

- Excess air ratio $\lambda$ has a clear and direct impact on boiler efficiency and stack loss. Around the design value (e.g. $\lambda \approx 1.1$) the indirect efficiency exhibits a shallow maximum, while both leaner and richer (higher $\lambda$) operation produce measurable efficiency penalties and altered stack conditions.
- Drum/feedwater pressure mainly affects the _quantity_ of steam generated for a given firing rate; efficiency and stack temperature are comparatively insensitive within the investigated pressure range. Higher pressures yield less mass flow of steam but at higher temperature and specific exergy.
- Fuel mass flow (firing rate) controls the overall scale of heat transfer and steam capacity. For moderate variations the useful duty and steam flow scale almost linearly with firing rate, whereas very low and very high loads show departures from ideal behaviour, reflected in efficiency changes and increased pressure drops.

Together, these simulations provide a quantitative basis for recommending operating windows that balance efficiency, capacity, and hydraulic constraints for the modeled industrial shell boiler. They also demonstrate that the numerical framework developed in Chapters 3–7 is robust and can be used as a tool for design exploration and optimisation of real boiler plants.

\newpage
