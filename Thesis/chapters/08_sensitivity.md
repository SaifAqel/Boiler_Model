# Sensitivity Analysis

This chapter evaluates how the coupled combustion boiler model responds to variations in three operating parameters:

- excess air ratio $\lambda$
- drum pressure
- fuel mass flow rate (firing rate)

The goal is to quantify how these parameters influence the boiler level quantities defined in Chapter 7:

- total useful heat transferred to the water and steam side $Q_\text{useful}$
- total heat input from combustion $Q_\text{in}$
- direct and indirect efficiencies $\eta_{\text{direct}}$, $\eta_{\text{indirect}}$
- stack gas temperature $T_\text{stack}$
- overall gas side pressure drop $\Delta P_\text{boiler}$
- converged water and steam mass flow $\dot{m}_w$

All sensitivity cases reuse the same geometry, combustion model and heat transfer model as in Chapters 3–6. Only the selected operating variable changes in each series, while the remaining inputs are kept at the control values.

All results in Chapters 4 and 7 correspond to the control case.

## Methodology

All sensitivity studies use the same numerical procedure as the control case and differ only in one input parameter. The helper function `run_boiler_case()` accepts optional override dictionaries for

- `operation_overrides` (for example `{"excess_air_ratio": Q_(ea, "")}`)
- `water_overrides` (for example `{"P": Q_(P_bar, "bar")}`)
- `fuel_overrides` (for example `{"mass_flow": Q_(mdot, "kg/s")}`)

which modify the corresponding YAML derived objects before each run.

For each value in a parameter sweep:

1. The relevant override is applied.
2. Combustion is recomputed for the new condition.
3. The water flow and efficiency iteration is executed until convergence.
4. Three CSV files are written to disk for later post processing:

   - `<run_id>_steps.csv` – per step marching data
   - `<run_id>_stages_summary.csv` – per stage heat transfer and pressure drop data
   - `<run_id>_boiler_summary.csv` – boiler level performance summary

The analysis in this chapter is based on plots and tables generated from the boiler summary and stage summary CSVs of these runs.

## Control case

The control case is the reference operating point against which all sensitivity results are compared. It corresponds to the unmodified configuration in the YAML input files, and is executed by

- `run_default_case()` in `main.py` which calls
- `run_boiler_case()` in `boiler_loop.py` with no overrides

The control case thus uses

- geometry from `config/drum.yaml` and `config/stages.yaml`
- fuel stream from `config/fuel.yaml`
- air stream from `config/air.yaml`
- excess air ratio from `config/operation.yaml`
- feedwater stream from `config/water.yaml`

Unless stated otherwise, all values and results in preceding chapters refer to this control case.

---

## Excess Air Ratio

### Simulation setup {#sec-lambda-setup} {- .unlisted}

The effect of excess air on boiler performance is investigated by `run_excess_air_sensitivity()` in `main.py`. The following values of the excess air ratio $\lambda$ are considered

$$
\lambda = 1.0,\ 1.1,\ 1.2,\ 1.3
$$

Each case is run as

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

The fuel mass flow is kept constant, so the chemical heat input $P_\text{LHV}$ remains fixed. With increasing $\lambda$:

- air mass flow and total flue gas mass flow increase
- flue gas composition shifts to higher $\mathrm{O_2}$ and slightly lower $CO_2$ and $H_2O$
- adiabatic flame temperature $T_\text{ad}$ decreases
- gas side convective and radiative driving forces change in all stages

---

### Observed trends {#sec-lambda-observed} {- .unlisted}

Boiler level quantities

- $\eta_{\text{direct}}$ and $\eta_{\text{indirect}}$ show a clear maximum close to $\lambda = 1.0$ to $1.1$.  
  For $\lambda = 1.0 \to 1.3$  
  $\eta_{\text{direct}}$ decreases from about $0.891$ to $0.876$.  
  $\eta_{\text{indirect}}$ follows the same trend.

- $Q_\text{useful}$ is almost constant but decreases slightly with excess air.  
  The useful duty drops by roughly $1\ \%$ between $\lambda = 1.0$ and $\lambda = 1.3$.

- Stack temperature $T_\text{stack}$ increases monotonically with $\lambda$  
  from about $176^\circ\text{C}$ at $\lambda = 1.0$ to about $192^\circ\text{C}$ at $\lambda = 1.3$.

- Total gas side pressure drop magnitude increases with $\lambda$  
  as higher flue gas flow raises velocities and friction losses.

- Water mass flow and steam capacity decrease slightly with $\lambda$  
  because lower gas side temperatures reduce the mean temperature difference.

Stage level quantities

- Gas inlet temperature to the first convective bank (HX_3) decreases with $\lambda$  
  due to lower flame temperature and stronger dilution by air.

- Along the convective pass the gas temperature profiles for different $\lambda$ remain almost parallel  
  but shifted downwards for low $\lambda$ and upwards for high $\lambda$.

- The economiser contribution $Q_\text{HX6}$ changes modestly with $\lambda$,  
  but the main sensitivity is in the radiant and first convective surfaces (HX_1 and HX_3).

---

### Interpretation {#sec-lambda-interpretation} {- .unlisted}

- Lower excess air (around $\lambda = 1.0$ to $1.1$) yields higher flame temperature and stronger driving force for both radiation and convection.  
  This improves $Q_\text{useful}$ and reduces stack losses at essentially unchanged $Q_\text{in}$.

- At very low $\lambda$ the improvement is limited by approach to stoichiometric conditions and the need for safe operation with sufficient $\mathrm{O_2}$ in the stack.  
  The current range does not yet show a sharp efficiency penalty at $\lambda = 1.0$.

- Higher excess air ($\lambda \geq 1.2$) cools the flame, increases flue gas mass flow and raises stack temperature.  
  More sensible heat leaves with the stack, so indirect efficiency drops.

- Pressure drop grows with $\lambda$ mainly because of the higher gas mass flow through all passes.  
  The effect is approximately quadratic in mass flow, with the furnace pass and tube banks dominating.

Overall the model predicts an efficiency optimum in the range

$$
1.0 \lesssim \lambda \lesssim 1.1
$$

with a shallow sensitivity, and a clear penalty toward richer air operation.

---

### Suggested plots for excess air

Boiler level overview

```markdown
![Excess air sweep boiler level](figs/excess_air/fig_lambda_boiler_overview.png)

Figure X.1 Excess air sweep boiler level quantities.  
Top left: $Q_\text{useful}$ and $Q_\text{in}$ versus $\lambda$.  
Top right: $\eta_{\text{direct}}$ and $\eta_{\text{indirect}}$ versus $\lambda$.  
Bottom left: stack temperature $T_\text{stack}$ and water mass flow $/dot{m}_w$ versus $\lambda$.  
Bottom right: total gas side pressure drop $\Delta P_\text{boiler}$ versus $\lambda$.
```

Stage temperatures

```markdown
![Excess air gas water temperature profile](figs/excess_air/fig_lambda_stage_temperatures.png)

Figure X.2 Gas and water temperature profile per heat exchanger stage for the excess air sweep.  
Horizontal axis: stage index HX*1 to HX_6.  
Solid lines: gas outlet temperature $T*{g,\text{out}}$ for each $\lambda$.  
Dashed lines: water outlet temperature $T_{w,\text{out}}$ for each $\lambda$.
```

Stage duties and conductance

```markdown
![Excess air stage duties](figs/excess_air/fig_lambda_stage_duties.png)

Figure X.3 Stage wise heat duties and global conductance for excess air sweep.  
Left: $Q_{\text{conv}}$, $Q_{\text{rad}}$, and $Q_{\text{total}}$ per stage versus $\lambda$.  
Right: global $UA$ of each stage versus $\lambda$.
```

Pressure losses

```markdown
![Excess air stage pressure drop](figs/excess_air/fig_lambda_stage_dp.png)

Figure X.4 Gas side pressure loss breakdown for excess air sweep.  
Friction, minor and total pressure drop per stage, plotted versus $\lambda$.
```

Compact conclusion panel

```markdown
![Excess air compact summary](figs/excess_air/fig_lambda_compact_summary.png)

Figure X.5 Compact summary for excess air sweep.  
Four panels:  
(a) $\eta_{\text{direct}}$ and $\eta_{\text{indirect}}$  
(b) stack temperature  
(c) steam capacity  
(d) total gas pressure drop  
All plotted versus $\lambda$.
```

---

## Drum pressure

### Simulation setup {#sec-pressure-setup} {- .unlisted}

The influence of drum pressure on boiler performance is studied with `run_water_pressure_sensitivity()` in `main.py`. The absolute pressure levels are

$$
P = 4\ \text{bar},\ 10\ \text{bar},\ 16\ \text{bar}
$$

Each case is run as

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

The override replaces the drum pressure in the `WaterStream` template used in `_water_mass_from_efficiency()`. The same pressure is used for saturation properties in the drum and boiling surfaces through `WaterProps`.

---

### Observed trends {#sec-pressure-observed} {- .unlisted}

Boiler level quantities

- Fuel mass flow and $Q_\text{in}$ are identical for all three cases.

- $\eta_{\text{direct}}$ and $\eta_{\text{indirect}}$ decrease mildly with pressure  
  from about $0.895$ at $4\ \text{bar}$ to about $0.882$ at $16\ \text{bar}$.

- Water mass flow and steam capacity decrease with pressure.  
  For the same firing rate the boiler produces more mass at $4\ \text{bar}$ than at $16\ \text{bar}$,  
  consistent with higher latent heat at low pressure.

- Stack temperature increases with pressure from about $163^\circ\text{C}$ at $4\ \text{bar}$  
  to about $192^\circ\text{C}$ at $16\ \text{bar}$.

- Total gas side pressure drop changes only marginally with drum pressure  
  because gas side flow conditions remain almost unchanged.

Stage level quantities

- Gas side temperatures and enthalpies are nearly identical at $P = 10\ \text{bar}$ and in the control case,  
  confirming that gas side behaviour is insensitive to water side pressure over this range.

- Water inlet temperature and enthalpy vary with saturation properties.  
  At higher pressure the boiling temperature rises and the economiser outlet temperature shifts upward.

- The distribution of $Q$ among stages changes slightly with pressure.  
  The economiser and final tube bank show the strongest sensitivity,  
  since they operate closest to saturation and depend on the approach to the drum temperature.

---

### Interpretation {#sec-pressure-interpretation} {- .unlisted}

- Raising drum pressure increases saturation temperature and reduces latent heat per unit mass.  
  With fixed firing rate the boiler delivers less steam mass flow but at higher specific enthalpy.

- The small efficiency trend with pressure reflects changes in approach temperatures at the final surfaces.  
  At high pressure the flue gas leaves at higher temperature, which slightly increases stack loss.

- Gas side hydraulics are almost unaffected by drum pressure,  
  since gas properties and mass flow are dominated by combustion conditions.

Within the investigated range the primary role of pressure is to trade steam mass flow against steam enthalpy,  
with only minor influence on efficiency and gas side pressure drop.

---

### Suggested plots for drum pressure

Boiler level overview

```markdown
![Drum pressure sweep boiler level](figs/water_pressure/fig_pressure_boiler_overview.png)

Figure Y.1 Drum pressure sweep boiler level quantities.  
Top left: $Q_\text{useful}$ and $Q_\text{in}$ versus drum pressure.  
Top right: $\eta_{\text{direct}}$ and $\eta_{\text{indirect}}$ versus drum pressure.  
Bottom left: water mass flow and steam capacity versus drum pressure.  
Bottom right: stack temperature and total gas pressure drop versus drum pressure.
```

Steam property trade off

```markdown
![Drum pressure steam tradeoff](figs/water_pressure/fig_pressure_steam_tradeoff.png)

Figure Y.2 Steam delivery trade off with drum pressure.  
Left: steam mass flow $/dot{m}_w$ versus drum pressure.  
Right: specific steam enthalpy at drum conditions versus drum pressure.
```

Stage distribution

```markdown
![Drum pressure stage duties](figs/water_pressure/fig_pressure_stage_duties.png)

Figure Y.3 Stage wise heat duties for drum pressure sweep.  
Stacked bars or grouped bars for $Q_{\text{total}}$ in HX_1 to HX_6 at each pressure.
```

Economiser detail

```markdown
![Drum pressure economiser](figs/water_pressure/fig_pressure_economiser.png)

Figure Y.4 Economiser performance as a function of drum pressure.  
Gas inlet and outlet temperatures, water inlet and outlet temperatures, and $Q_{\text{HX6}}$ versus pressure.
```

Compact conclusion panel

```markdown
![Drum pressure compact summary](figs/water_pressure/fig_pressure_compact_summary.png)

Figure Y.5 Compact summary for drum pressure sweep.  
Four panels:  
(a) efficiency versus pressure  
(b) stack temperature versus pressure  
(c) steam capacity versus pressure  
(d) steam enthalpy versus pressure.
```

---

## Fuel mass flow rate (firing rate)

### Simulation setup {#sec-fuel-setup} {- .unlisted}

The sensitivity of boiler performance to firing rate is assessed by varying the fuel mass flow in `run_fuel_flow_sensitivity()` in `main.py`. The following fuel mass flow rates are considered

$$
\dot{m}\_f = 0.025,\ 0.050,\ 0.075,\ 0.100\ \text{kg s}^{-1}
$$

Each case is run as

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

The excess air ratio, geometry and drum pressure are kept at their control case values.

---

### Observed trends {#sec-fuel-observed} {- .unlisted}

Boiler level quantities

- Chemical heat input $Q_\text{in}$ scales almost linearly with fuel mass flow  
  from about $1.18\ \text{MW}$ at $0.025\ \text{kg s}^{-1}$ to about $4.70\ \text{MW}$ at $0.10\ \text{kg s}^{-1}$.

- $Q_\text{useful}$ also scales nearly linearly over most of the range.  
  At the lowest firing rate the ratio $Q_\text{useful} / Q_\text{in}$ is slightly higher.

- $\eta_{\text{direct}}$ decreases from about $0.908$ at the lowest load  
  to about $0.887$ at the highest load.  
  The indirect efficiency exhibits the same trend.

- Steam capacity follows $Q_\text{useful}$ almost linearly.  
  Deviations from linearity are most visible at very low and very high firing rate.

- Stack temperature $T_\text{stack}$ increases with fuel mass flow  
  from about $131^\circ\text{C}$ at $0.025\ \text{kg s}^{-1}$  
  to about $181^\circ\text{C}$ at $0.10\ \text{kg s}^{-1}$.

- Total gas pressure drop increases strongly with firing rate,  
  with an almost quadratic dependence on gas mass flow.

Stage level quantities

- The furnace outlet temperature changes little with firing rate,  
  because flame temperature is set mainly by stoichiometry and less by absolute rate.

- Gas temperatures throughout the convective pass are higher at higher firing rate,  
  hence each stage processes more heat at increased duty.

- Stage pressure drops scale strongly with load.  
  Tube bank stages (HX_3 and HX_5) show the largest increase in $\Delta P$ with fuel mass flow.

- Water side velocities increase with load, particularly in boiling and riser sections,  
  but remain within the same order of magnitude across the studied range.

---

### Interpretation {#sec-fuel-interpretation} {- .unlisted}

- For moderate variations of fuel mass flow the boiler behaves close to an ideal linear system.  
  Both $Q_\text{useful}$ and steam capacity scale with firing rate.

- At very low load fixed parasitic losses and finite approach temperatures become more important.  
  The stack temperature is reduced and indirect efficiency increases slightly.

- At high load gas side approach temperatures grow and stack temperature rises.  
  This increases stack loss and reduces $\eta$ at constant fuel quality.

- Gas side pressure drop becomes a limiting factor at high firing rate.  
  The strong growth of $\Delta P$ indicates higher fan power and possible constraints for operation near full load.

The model therefore predicts a useful load window where efficiency is high and pressure drops remain acceptable.  
Outside this window efficiency penalties and hydraulic constraints become more pronounced.

---

### Suggested plots for firing rate

Boiler level overview

```markdown
![Firing rate sweep boiler level](figs/fuel_flow/fig_fuel_boiler_overview.png)

Figure Z.1 Firing rate sweep boiler level quantities.  
Top left: $Q_\text{useful}$ and $Q_\text{in}$ versus fuel mass flow.  
Top right: $\eta_{\text{direct}}$ and $\eta_{\text{indirect}}$ versus fuel mass flow.  
Bottom left: steam capacity versus fuel mass flow.  
Bottom right: stack temperature and total gas pressure drop versus fuel mass flow.
```

Linearity check

```markdown
![Firing rate linearity](figs/fuel_flow/fig_fuel_linearity.png)

Figure Z.2 Linearity of boiler response with firing rate.  
Left: $Q_\text{useful}$ versus $Q_\text{in}$ with a reference straight line.  
Right: steam capacity versus fuel mass flow with a reference straight line.
```

Stage duties and pressure losses

```markdown
![Firing rate stage duties and dp](figs/fuel_flow/fig_fuel_stage_duty_dp.png)

Figure Z.3 Stage wise heat duties and pressure drops as a function of fuel mass flow.  
Top: $Q_{\text{total}}$ in HX_1 to HX_6 versus fuel mass flow.  
Bottom: friction, minor and total pressure drop per stage versus fuel mass flow.
```

Temperature profiles

```markdown
![Firing rate temperature profiles](figs/fuel_flow/fig_fuel_stage_temperatures.png)

Figure Z.4 Gas and water temperature profile per stage for the firing rate sweep.  
Horizontal axis: stage index HX_1 to HX_6.  
Series: one curve for each firing rate for gas outlet temperature and one for water outlet temperature.
```

Compact conclusion panel

```markdown
![Firing rate compact summary](figs/fuel_flow/fig_fuel_compact_summary.png)

Figure Z.5 Compact summary for firing rate sweep.  
Four panels:  
(a) efficiency versus fuel mass flow  
(b) stack temperature versus fuel mass flow  
(c) steam capacity versus fuel mass flow  
(d) total gas pressure drop versus fuel mass flow.
```

---

## Summary

The sensitivity analysis presented in this chapter shows that

- Excess air ratio $\lambda$ has a clear and direct impact on boiler efficiency and stack loss.  
  Around the design value $\lambda = 1.0$ to $1.1$ the indirect efficiency exhibits a shallow maximum.  
  Higher values of $\lambda$ lead to measurable efficiency penalties, higher stack temperature and higher gas pressure drop.

- Drum and feedwater pressure mainly affect the quantity of steam generated for a given firing rate.  
  Efficiency and stack temperature are comparatively insensitive within the investigated pressure range.  
  Higher pressure yields less steam mass flow but at higher temperature and specific enthalpy.

- Fuel mass flow (firing rate) controls the overall scale of heat transfer and steam capacity.  
  For moderate variations the useful duty and steam flow scale almost linearly with firing rate.  
  Very low and very high loads show departures from ideal behaviour, reflected in efficiency changes and increased pressure drops.

Together these simulations provide a quantitative basis for selecting operating windows that balance efficiency, capacity and hydraulic constraints for the modelled industrial shell boiler.  
They demonstrate that the numerical framework from Chapters 3–7 is robust and suitable as a tool for design exploration and optimisation of real boiler plants.
