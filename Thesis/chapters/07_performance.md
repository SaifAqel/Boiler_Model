# Performance

This section summarizes the boiler level performance obtained from the coupled combustion heat transfer simulation. All numerical values are extracted from the stages summary and boiler summary data produced by the post-processing step `heat/postproc.py`.

## solution procedure

For any given operating conditions, the main solver `run_boiler_case()` performs an outer fixed point iteration, on boiler efficiency, and water mass flow:

1. The combustion sub-model called by `Combustor.run()`, returns:

   - the lower heating value based firing rate $P_\text{LHV}$,
   - the total combustion heat release $Q_\text{in}$,
   - the adiabatic flame temperature $T_\text{ad}$,
   - the fully burnt flue-gas stream at burner exit.

2. Given a current efficiency guess ${\eta}^{(n)}$ and the combustion result, the corresponding feedwater/steam mass flow $\dot{m}_w^{(n)}$ is computed by `_water_mass_from_efficiency()` as

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

3. A `WaterStream` with mass flow $\dot{m}_w^{(n)}$ is created and passed, together with the combustion flue gas `GasStream` and the drum/stage definitions, to the multi stage heat exchanger solver `run_hx()`.

4. `run_hx()` returns per stage and boiler level summary tables.

5. The new efficiency estimate is set to the indirect efficiency,

   $$
   \eta^{(n+1)} := \eta_{\text{indirect}}^{(n)},
   $$

And the procedure is repeated until the change in water mass flow between iterations is below the specified tolerance

$$
\left|\dot{m}_w^{(n)} - \dot{m}_w^{(n-1)}\right| < 10^{-3}\,\mathrm{kg/s},
$$

or a maximum number of iterations is reached.

At convergence, returning:

- converged water/steam mass flow $\dot{m}_{w,\text{base}}$,
- converged indirect efficiency $\eta_{\text{indirect,base}}$,

together with the corresponding boiler summary quantities (stack temperature, total pressure drop, etc.). These and more are exported to CSV as `boiler_summary.csv` and `stages_summary.csv`.

## Energy balance

The total useful heat transferred from the flue gas to the water/steam side is obtained by integrating the local line heat flux $q'(x)$ over all stages:

$$
Q_\text{useful} \;=\; \sum_{k=1}^{6} Q_{\text{stage},k}
\;=\; \sum_{k=1}^{6} \int_ q'(x)\,\mathrm{d}x
$$

The total input heat from combustion $Q_\text{in}$ is taken from the combustion module as the rate of heat release from complete fuel burnout:

## Efficiency

Two boiler efficiencies are reported:

- Direct efficiency (LHV):

  $$
  \eta_\text{direct}
  \;=\;
  \frac{Q_\text{useful}}{P_\text{LHV}}
  $$

- Indirect efficiency:
  $$
  \eta_\text{indirect}
  \;=\;
  1 - \frac{Q_\text{losses}}{Q_\text{in}}
  $$

## Water/Steam flow rate convergence

The water/steam mass flow rate is obtained iteratively from an assumed overall boiler efficiency and the combustion heat input. At each iteration $n$ the code:

1. Assumes an efficiency $\eta^{(n)}$.
2. Computes the target useful duty:
   $$
   Q_\text{target}^{(n)} = \eta^{(n)}\,Q_\text{in}
   $$
3. Determines the required water mass flow $\dot m_\text{w}^{(n)}$ from the enthalpy rise between feedwater and saturated steam at drum pressure:
   $$
   \dot m_\text{w}^{(n)} \;=\;
   \frac{Q_\text{target}^{(n)}}{h_\text{steam}(P_\text{drum}) - h_\text{fw}}
   $$
4. Runs the full multi-stage heat-exchanger model with $\dot m_\text{w}^{(n)}$ and reads back the resulting indirect efficiency $\eta_\text{indirect}^{(n)}$.
5. Sets the next efficiency guess $\eta^{(n+1)} = \eta_\text{indirect}^{(n)}$ and repeats until the mass flow change is below the specified tolerance:
   $$
   \bigl|\dot m_\text{w}^{(n)} - \dot m_\text{w}^{(n-1)}\bigr|
   < 10^{-3}\,\text{kg/s}
   $$

## Stage level performance

Stage level performance table returned by the post processor `heat/postproc.py`. For each stage $k$ the following quantities are available:

- Heat duty: `Q_stage[MW]`
- Overall conductance: `UA_stage[MW/K]`
- Gas inlet/outlet temperatures: `gas_in_T[°C]`, `gas_out_T[°C]`
- Water inlet/outlet temperatures: `water_in_T[°C]`, `water_out_T[°C]`
- Gas side pressure drops: `ΔP_stage_fric[Pa]`, `ΔP_stage_minor[Pa]`, `ΔP_stage_total[Pa]`
- Decomposition of duty into convection and radiation: `Q_conv_stage[MW]`, `Q_rad_stage[MW]`

Table: Stages summary results.

| Kind         | $T_{g,\text{in}}$ [°C] | $T_{g,\text{out}}$ [°C] | $T_{w,\text{in}}$ [°C] | $T_{w,\text{out}}$ [°C] | $Q_\text{stage}$ [MW] | $UA_\text{stage}$ [MW/K] | $\Delta P_\text{stage}$ [Pa] |
| ------------ | ---------------------- | ----------------------- | ---------------------- | ----------------------- | --------------------- | ------------------------ | ---------------------------- |
| single tube  | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| reversal ch. | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| tube bank    | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| reversal ch. | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| tube bank    | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| economizer   | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |

## Boiler performance

The overall boiler performance is summarized using the boiler summary table, supplied by `heat/postproc.py`:

Table: Boiler summary results.

| Quantity                       | Symbol                  | Value |
| ------------------------------ | ----------------------- | ----- |
| Fuel firing (LHV basis)        | $P_\text{LHV}$          |       |
| Total heat input (combustion)  | $Q_\text{in}$           |       |
| Useful heat to water/steam     | $Q_\text{useful}$       |       |
| Direct efficiency (LHV basis)  | $\eta_\text{direct}$    |       |
| Indirect efficiency            | $\eta_\text{indirect}$  |       |
| Stack gas temperature          | $T_\text{stack}$        |       |
| Gas side friction loss         | $\Delta P_\text{fric}$  |       |
| Gas side minor losses          | $\Delta P_\text{minor}$ |       |
| Total gas side pressure drop   | $\Delta P_\text{tot}$   |       |
| Total convective heat transfer | $Q_\text{conv}$         |       |
| Total radiative heat transfer  | $Q_\text{rad}$          |       |

These boiler level results provide the basis for the sensitivity analysis in Section 8 and for comparing alternative design or operating scenarios.

\newpage
