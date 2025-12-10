# Sensitivity Analysis

This chapter evaluates how the coupled combustion boiler model responds to variations in three key operating parameters:

- excess air ratio $\lambda$,
- drum pressure,
- fuel mass flow rate (firing rate).

The goal is to quantify how these parameters influence the boiler level quantities introduced in Chapter&nbsp;7, in particular:

- total useful heat transferred to the water/steam side $Q_\text{useful}$,
- total heat input from combustion $Q_\text{in}$,
- direct and indirect efficiencies $\eta_{\text{direct}}$, $\eta_{\text{indirect}}$,
- stack gas temperature $T_\text{stack}$,
- overall gas side pressure drop $\Delta P_\text{boiler}$,
- converged water/steam mass flow $\dot{m}_w$.

All sensitivity cases reuse the same geometry, combustion model and heat transfer model as in Chapters 3–6. Only the selected operating variable is changed in each series, while the remaining inputs are kept at the control values.

All results included in the Chapters 4 & 7, are of the control case.

## Methodology

All sensitivity studies use the same numerical procedure as the control case and **differ only in one input parameter**. The helper function `run_boiler_case()` accepts optional override dictionaries for:

- `operation_overrides` (e.g. `{"excess_air_ratio": Q_(ea, "")}`),
- `water_overrides` (e.g. `{"P": Q_(P_bar, "bar")}`),
- `fuel_overrides` (e.g. `{"mass_flow": Q_(mdot, "kg/s")}`),

which modify the corresponding YAML derived objects before each run.

For each value in a parameter sweep:

1. The relevant override is applied.
2. Combustion is recomputed for the new condition.
3. The water flow/efficiency iteration is executed until convergence.
4. Three CSV files are written to disk for later post-processing:

   - `<run_id>_steps.csv` – per step marching data,
   - `<run_id>_stages_summary.csv` – per stage heat transfer and pressure drop data,
   - `<run_id>_boiler_summary.csv` – boiler level performance summary.

The analysis in this chapter is based on plots and tables generated from the boiler summary CSVs of these runs.

## Control case

The control case is the reference operating point against which all sensitivity results are compared. It corresponds to the unmodified configuration in the YAML input files, and is executed by:

- `run_default_case()` in `main.py`, which calls
- `run_boiler_case()` in `boiler_loop.py` with no overrides.

The control case thus uses:

- Geometry: drum and stages from `config/drum.yaml` and `config/stages.yaml`.
- Fuel stream: from `config/fuel.yaml`.
- Air stream: from `config/air.yaml`.
- Excess air ratio: specified in `config/operation.yaml`.
- Feedwater stream: from `config/water.yaml`.

All configuration YAML files are provided in Appendix A.

Unless stated otherwise, all values and results discussed in preceding chapters refer to this control case.

## Excess Air Ratio

### Simulation setup {#sec-lambda-setup} {- .unlisted}

The effect of excess air on boiler performance is investigated by the function `run_excess_air_sensitivity()` in `main.py`. The following values of the excess air ratio $\lambda$ are considered:

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

All other configuration files (`stages.yaml`, `fuel.yaml`, `air.yaml`, `water.yaml`, `drum.yaml`) are left unchanged relative to the control case. The fuel mass flow is therefore constant across the excess air sweep, so the chemical heat input on an LHV basis $P_\text{LHV}$ remains fixed. What changes with $\lambda$ is:

- the air mass flow and hence total flue gas mass flow,
- the flue gas composition (residual $\mathrm{O_2}$ level, minor change in $CO_2$ and $H_2O$ fractions),
- the adiabatic flame temperature $T_\text{ad}$,
- the gas side convective and radiative driving forces in all stages.

### Observed trends {#sec-lambda-observed} {- .unlisted}

### Interpretation {#sec-lambda-interpretation} {- .unlisted}

## Drum pressure

### Simulation setup {#sec-pressure-setup} {- .unlisted}

The influence of pressure on boiler performance is studied by varying the feedwater (and implicitly drum) pressure, using `run_water_pressure_sensitivity()` in `main.py`. The investigated absolute pressure levels are:

- $P = 4\,\text{bar},\;10\,\text{bar},\;16\,\text{bar}$.

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

The override replaces the drum pressure in the `WaterStream` object used as template in `_water_mass_from_efficiency()`. The same pressure is also used for saturation properties in the drum and boiling surfaces via `WaterProps`.

### Observed trends {#sec-pressure-observed} {- .unlisted}

### Interpretation {#sec-pressure-interpretation} {- .unlisted}

## Fuel mass-flow rate (firing rate)

### Simulation setup {#sec-fuel-setup} {- .unlisted}

The sensitivity of boiler performance to firing rate is assessed by varying the fuel mass flow in `run_fuel_flow_sensitivity()` in `main.py`. The following fuel mass flow rates are considered:

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

The excess air ratio, geometry, and drum pressure are kept at their control case values.

### Observed trends {#sec-fuel-observed} {- .unlisted}

### Interpretation {#sec-fuel-interpretation} {- .unlisted}

## Summary

The sensitivity analysis presented in this chapter shows that:

- Excess air ratio $\lambda$ has a clear and direct impact on boiler efficiency and stack loss. Around the design value ($\lambda = 1.1$) the indirect efficiency exhibits a shallow maximum, while both leaner and richer (higher $\lambda$) operation produce measurable efficiency penalties and altered stack conditions.
- Drum/feedwater pressure mainly affects the _quantity_ of steam generated for a given firing rate; efficiency and stack temperature are comparatively insensitive within the investigated pressure range. Higher pressures yield less mass flow of steam but at higher temperature and specific energy.
- Fuel mass flow (firing rate) controls the overall scale of heat transfer and steam capacity. For moderate variations the useful duty and steam flow scale almost linearly with firing rate, whereas very low and very high loads show departures from ideal behavior, reflected in efficiency changes and increased pressure drops.

Together, these simulations provide a quantitative basis for recommending operating windows that balance efficiency, capacity, and hydraulic constraints for the modeled industrial shell boiler. They also demonstrate that the numerical framework developed in Chapters 3–7 is robust and can be used as a tool for design exploration and optimization of real boiler plants.

\newpage
