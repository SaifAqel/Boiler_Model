# Performance

This section summarizes the boiler level performance obtained from the coupled combustion heat transfer simulation. All numerical values are extracted from the stages summary and boiler summary data produced by the post-processing step `heat/postproc.py`.

## Solution procedure

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

\newpage
