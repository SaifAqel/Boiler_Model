# Boiler Performance Results

This section summarizes the boiler level performance obtained from the coupled combustion–heat-transfer simulation. All numerical values are extracted from the stage summary and boiler summary data produced by the post-processing step (fields `Q_stage[MW]`, `UA_stage[MW/K]`, `η_direct[-]`, `η_indirect[-]`, `Q_total_useful[MW]`, `Q_in_total[MW]`, `P_LHV[MW]`, `stack_temperature[°C]`, etc.).

## Energy balance ($\mathrm{Q_{in}}$, $\mathrm{Q_{useful}}$)

The total useful heat transferred from the flue gas to the water/steam side is obtained by integrating the local line heat flux $q'(x)$ over all stages:

$$
Q_\text{useful} \;=\; \sum_{k=1}^{6} Q_{\text{stage},k}
\;=\; \sum_{k=1}^{6} \int_{\text{stage }k} q'(x)\,\mathrm{d}x
$$

In the implementation this appears as the sum of `Q_stage[MW]` over all stages in `summary_rows`, with the boiler-level result reported in the `TOTAL_BOILER` row as `Q_total_useful[MW]`.

The total input heat from combustion $Q_\text{in}$ is taken from the combustion module as the rate of heat release from complete fuel burnout (field `Q_in_total[MW]`):

$$
Q_\text{in} \;=\; Q_\text{in,total}
$$

For reference, the firing rate on an LHV basis is also reported as `P_LHV[MW]`, obtained from the fuel lower heating value and the fuel mass flow rate.

A concise numerical statement:

- $Q*\text{in} = Q*\text{in,total} =
- $Q*\text{useful} = Q*\text{total,useful} =

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/boiler_T-S_chart.png}
\caption{Temperature–entropy ($T$–$s$) representation of the feedwater heating and evaporation process across economiser and boiler at the operating pressure.}
\label{fig:boiler-TS}
\end{figure}

## Efficiencies (direct and indirect)

Two boiler efficiencies are reported:

- Direct efficiency (LHV basis)  
  Direct efficiency is defined as the ratio of useful heat transferred to the firing rate based on fuel LHV:

  $$
  \eta_\text{direct}
  \;=\;
  \frac{Q_\text{useful}}{P_\text{LHV}}
  $$

  where $P_\text{LHV}$ is the firing capacity (field `P_LHV[MW]`).

- Indirect efficiency (heat-balance basis)  
  Indirect efficiency is defined as the ratio of useful heat to the total heat released by combustion:
  $$
  \eta_\text{indirect}
  \;=\;
  \frac{Q_\text{losses}}{Q_\text{in}}
  $$

In the post-processing, these appear as the boiler-level fields:

- Direct (LHV) efficiency: $\eta\_\text{direct} =$
- Indirect efficiency: $\eta\_\text{indirect} =$

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
4. Runs the full multi-stage heat-exchanger model with $\dot m_\text{w}^{(n)}$ and reads back the resulting indirect efficiency $\eta_\text{indirect}^{(n)}$.
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

## Stage level performance

Stage level performance is summarized from the per-stage rows in the summary table returned by the post-processor. For each stage $k$ the following quantities are available:

- Heat duty: `Q_stage[MW]`
- Overall conductance: `UA_stage[MW/K]`
- Gas inlet/outlet temperatures: `gas_in_T[°C]`, `gas_out_T[°C]`
- Water inlet/outlet temperatures: `water_in_T[°C]`, `water_out_T[°C]`
- Gas side pressure drops: `ΔP_stage_fric[Pa]`, `ΔP_stage_minor[Pa]`, `ΔP_stage_total[Pa]`
- Decomposition of duty into convection and radiation: `Q_conv_stage[MW]`, `Q_rad_stage[MW]`

| Kind         | $T_{g,\text{in}}$ [°C] | $T_{g,\text{out}}$ [°C] | $T_{w,\text{in}}$ [°C] | $T_{w,\text{out}}$ [°C] | $Q_\text{stage}$ [MW] | $UA_\text{stage}$ [MW/K] | $\Delta P_\text{stage}$ [Pa] |
| ------------ | ---------------------- | ----------------------- | ---------------------- | ----------------------- | --------------------- | ------------------------ | ---------------------------- |
| single tube  | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| reversal ch. | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| tube bank    | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| reversal ch. | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| tube bank    | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |
| economiser   | [·]                    | [·]                     | [·]                    | [·]                     | [·]                   | [·]                      | [·]                          |

## Overall boiler summary

The overall boiler performance is finally summarized using the boiler summary table:

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

These boiler-level results provide the basis for the sensitivity analysis in Section 8 and for comparing alternative design or operating scenarios.

\newpage
