# Boiler Performance Results

This section summarizes the boiler‐level performance obtained from the coupled combustion–heat-transfer simulation. All numerical values are extracted from the stage summary and boiler summary data produced by the post-processing step (fields `Q_stage[MW]`, `UA_stage[MW/K]`, `η_direct[-]`, `η_indirect[-]`, `Q_total_useful[MW]`, `Q_in_total[MW]`, `P_LHV[MW]`, `stack_temperature[°C]`, etc.).

## Energy balance ($Q_\text{in}$, $Q_\text{useful}$)

The total useful heat transferred from the flue gas to the water/steam side is obtained by integrating the local line heat flux $q'(x)$ over all stages:

$$
Q_\text{useful} \;=\; \sum_{k=1}^{6} Q_{\text{stage},k}
\;=\; \sum_{k=1}^{6} \int_{\text{stage }k} q'(x)\,\mathrm{d}x
$$

In the implementation this appears as the sum of `Q_stage[MW]` over all stages in `summary_rows`, with the boiler-level result reported in the `TOTAL_BOILER` row as `Q_total_useful[MW]`.

The total input heat from combustion $Q_\text{in}$ is taken from the combustion module as the rate of heat release from complete fuel burnout (field `Q_in_total[MW]` in the `TOTAL_BOILER` row):

$$
Q_\text{in} \;=\; Q_\text{in,total}
$$

For reference, the firing rate on an LHV basis is also reported as `P_LHV[MW]`, obtained from the fuel lower heating value and the fuel mass flow rate.

A concise numerical statement (to be filled from the CSV):

- $Q_\text{in} = Q_\text{in,total} = \texttt{[Q\_in\_total MW]}$
- $Q_\text{useful} = Q_\text{total,useful} = \texttt{[Q\_total\_useful MW]}$

where the bracketed placeholders are to be replaced by the corresponding values from the `TOTAL_BOILER` row.

## Efficiencies (direct and indirect)

Two boiler efficiencies are reported:

- **Direct efficiency (LHV basis)**  
  Direct efficiency is defined as the ratio of useful heat transferred to the firing rate based on fuel LHV:

  $$
  \eta_\text{direct}
  \;=\;
  \frac{Q_\text{useful}}{P_\text{LHV}}
  $$

  where $P_\text{LHV}$ is the firing capacity (field `P_LHV[MW]`).

- **Indirect efficiency (heat-balance basis)**  
  Indirect efficiency is defined as the ratio of useful heat to the total heat released by combustion:
  $$
  \eta_\text{indirect}
  \;=\;
  \frac{Q_\text{useful}}{Q_\text{in}}
  $$

In the post-processing, these appear as the boiler-level fields in the `TOTAL_BOILER` row:

- `η_direct[-]` → $\eta_\text{direct}$
- `η_indirect[-]` → $\eta_\text{indirect}$

Text to be instantiated in the final report (numbers from CSV):

- Direct (LHV) efficiency: $\eta_\text{direct} = \texttt{[η\_direct · 100]}~\%$
- Indirect efficiency: $\eta_\text{indirect} = \texttt{[η\_indirect · 100]}~\%$

## Steam generation rate and mass-flow convergence

The water/steam mass flow rate is not prescribed but obtained iteratively from an assumed overall boiler efficiency and the combustion heat input. At each iteration $n$ the code:

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
4. Runs the full multi-stage heat-exchanger model with $\dot m_\text{w}^{(n)}$ and reads back the resulting indirect efficiency $\eta_\text{indirect}^{(n)}$ from the `TOTAL_BOILER` row.
5. Sets the next efficiency guess $\eta^{(n+1)} = \eta_\text{indirect}^{(n)}$ and repeats until the mass-flow change is below the specified tolerance:
   $$
   \bigl|\dot m_\text{w}^{(n)} - \dot m_\text{w}^{(n-1)}\bigr|
   < 10^{-3}\,\text{kg/s}
   $$

The final converged values to be reported are:

- Converged feedwater/steam mass flow:
  $$
  \dot m_\text{w} = \texttt{[m\_w, kg/s]}
  $$
- Number of outer iterations to achieve $\bigl|\Delta\dot m_\text{w}\bigr| < 10^{-3}\,\text{kg/s}$:
  $$
  N_\text{iter} = \texttt{[N]}
  $$

In the narrative, this subsection should state that the mass-flow/efficiency fixed point converged and that the final efficiency used in the performance summary is the converged $\eta_\text{indirect}$.

## Stage-level performance

Stage-level performance is summarized from the per-stage rows (`stage_name ≠ "TOTAL_BOILER"`) in the summary table returned by the post-processor. For each stage $k$ the following quantities are available:

- Heat duty: `Q_stage[MW]`
- Overall conductance: `UA_stage[MW/K]`
- Gas inlet/outlet temperatures: `gas_in_T[°C]`, `gas_out_T[°C]`
- Water inlet/outlet temperatures: `water_in_T[°C]`, `water_out_T[°C]`
- Gas‐side pressure drops: `ΔP_stage_fric[Pa]`, `ΔP_stage_minor[Pa]`, `ΔP_stage_total[Pa]`
- Decomposition of duty into convection and radiation: `Q_conv_stage[MW]`, `Q_rad_stage[MW]`

A compact table layout for the report (values to be filled from the CSV) is:

| Kind         | $T_{g,\text{in}}$ [°C] | $T_{g,\text{out}}$ [°C] | $T_{w,\text{in}}$ [°C] | $T_{w,\text{out}}$ [°C] | $Q_\text{stage}$ [MW] | $UA_\text{stage}$ [MW/K] | $\Delta P_\text{stage}$ [Pa] |
| ------------ | ---------------------- | ----------------------- | ---------------------- | ----------------------- | --------------------- | ------------------------ | ---------------------------- |
| single tube  | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| reversal ch. | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| tube bank    | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| reversal ch. | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| tube bank    | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| economiser   | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |

If desired, an additional column can be added to show the fraction of radiative heat transfer in each stage:

$$
\phi_{\text{rad},k} = \frac{Q_{\text{rad},k}}{Q_{\text{stage},k}} =
\frac{\texttt{Q\_rad\_stage[MW]}}{\texttt{Q\_stage[MW]}}
$$

This highlights the dominance of radiation in the furnace/reversal stages and convection in the tube banks and economiser.

## Overall boiler summary

The overall boiler performance is finally summarized using the `TOTAL_BOILER` row of the summary table. A suggested boiler summary table is:

| Quantity                       | Symbol                  | Value                   |
| ------------------------------ | ----------------------- | ----------------------- |
| Fuel firing (LHV basis)        | $P_\text{LHV}$          | `P_LHV[MW]`             |
| Total heat input (combustion)  | $Q_\text{in}$           | `Q_in_total[MW]`        |
| Useful heat to water/steam     | $Q_\text{useful}$       | `Q_total_useful[MW]`    |
| Direct efficiency (LHV basis)  | $\eta_\text{direct}$    | `η_direct[-]`           |
| Indirect efficiency            | $\eta_\text{indirect}$  | `η_indirect[-]`         |
| Stack gas temperature          | $T_\text{stack}$        | `stack_temperature[°C]` |
| Gas‐side friction loss         | $\Delta P_\text{fric}$  | `ΔP_stage_fric[Pa]`     |
| Gas‐side minor losses          | $\Delta P_\text{minor}$ | `ΔP_stage_minor[Pa]`    |
| Total gas‐side pressure drop   | $\Delta P_\text{tot}$   | `ΔP_stage_total[Pa]`    |
| Total convective heat transfer | $Q_\text{conv}$         | `Q_conv_stage[MW]`      |
| Total radiative heat transfer  | $Q_\text{rad}$          | `Q_rad_stage[MW]`       |

In the narrative text, the key messages of this subsection should be:

- The final converged steam production rate and overall efficiency.
- The relative contributions of convective and radiative heat transfer.
- The resulting stack temperature and global gas-side pressure drop across the boiler.

These boiler-level results provide the basis for the sensitivity analysis in Section 8 and for comparing alternative design or operating scenarios.

\newpage
