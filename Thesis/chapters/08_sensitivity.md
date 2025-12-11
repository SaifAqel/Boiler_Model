# Sensitivity analysis

This section summarizes how key operating parameters move the boiler away from a single reference case. Each sensitivity run changes exactly one parameter and reruns the full coupled model until convergence. All results are interpreted relative to the control case.

## Control case

The control case corresponds to all configurations and results discusses in previous chapters, defining the reference results profiles .At this point the model predicts:

Table: Key results of control case

| Parameter                      | Symbol                     | Value      |
| ------------------------------ | -------------------------- | ---------- |
| Steam capacity                 | $\dot m_{\mathrm{steam}}$  | 7.45 t h⁻¹ |
| Direct efficiency              | $\eta_{\mathrm{direct}}$   | 0.887      |
| Indirect efficiency            | $\eta_{\mathrm{indirect}}$ | 0.886      |
| Total heat input               | $Q_{\mathrm{in}}$          | 4.70 MW    |
| Useful heat input              | $Q_{\mathrm{useful}}$      | 4.17 MW    |
| Adiabatic flame temperature    | $T_{\mathrm{ad}}$          | 1900 °C    |
| Stack temperature              | $T_{\mathrm{stack}}$       | 181 °C     |
| Overall gas-side pressure loss | $\Delta p_{\mathrm{gas}}$  | 75 Pa      |

A global overview of flow rates and thermal performance over all runs is provided by the boiler level plots

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/plotty/boiler_flows_and_capacity_vs_param.png}
\caption{Boiler fuel air and water mass flows and steam capacity as functions of the varied parameter for each sensitivity group}
\label{fig:boiler_flows_and_capacity_vs_param}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/plotty/boiler_thermal_performance_vs_param.png}
\caption{Boiler thermal performance metrics as functions of the varied parameter}
\label{fig:boiler_thermal_performance_vs_param}
\end{figure}

Stage wise temperatures duties and hydraulic behavior for all runs are summarized in the heat exchanger overview

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/plotty/hx_temperatures_vs_stage.png}
\caption{Gas and water inlet and outlet temperatures along the heat exchanger train for all simulated runs}
\label{fig:hx_temperatures_vs_stage}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/plotty/hx_heat_transfer_and_UA_vs_stage.png}
\caption{Convective radiative and total heat duties together with overall conductance $UA$ as functions of heat exchanger stage index for all runs}
\label{fig:hx_heat_transfer_and_UA_vs_stage}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/plotty/hx_pressures_velocities_dp_vs_stage.png}
\caption{Gas and water pressures velocities and frictional minor and total gas side pressure drops along the heat exchanger stages}
\label{fig:hx_pressures_velocities_dp_vs_stage}
\end{figure}

Additional per run diagnostic plots for the control case and for each sensitivity run are used later in the chapter for detailed interpretation of individual stages

## Sensitivity parameters

Each sensitivity series changes only one input while all other boundary conditions and geometry remain fixed. The three groups are excess air ratio $\lambda$, drum pressure $p_{\mathrm{drum}}$ and fuel mass flow $\dot m_{\mathrm f}$.

A compact global view of how key boiler level indicators respond to the varied parameters is given by

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/plotty/boiler_temperatures_and_pressure_drops_vs_param.png}
\caption{Adiabatic flame temperature stack temperature and gas side pressure drops as functions of the varied parameter across all sensitivity groups}
\label{fig:boiler_temperatures_and_pressure_drops_vs_param}
\end{figure}

### Excess air ratio

The excess air series modifies the combustion air flow around the control point. This runs the model for the values of $$\lambda = [1.0, 1.1, 1.2, 1.3]$$

#### Boiler level effects {- .unlisted #sec-ea}

At constant firing rate the total chemical energy input is unchanged so changes in efficiency mainly reflect stack and other losses. The main trends with increasing $\lambda$ are

- direct and indirect efficiencies decrease as colder combustion with higher dry flue gas loss offsets.
- stack temperature $T_{\mathrm{stack}}$ increases due to the larger flue gas flow.
- gas side pressure loss magnitude increases almost proportionally to flue gas mass flow

These tendencies are shown in the following plots:

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_lambda_boiler_overview.png}
\caption{Performance indicators as a function of excess air ratio}
\label{fig:lambda_boiler_overview}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_lambda_compact_summary.png}
\caption{Compact summary of boiler efficiency stack temperature steam capacity and gas side pressure drop as a function of excess air ratio $\lambda$}
\label{fig:lambda_compact_summary}
\end{figure}

Stage wise temperatures and duties

Dilution by additional air lowers flame temperature and early stage gas temperatures but increases gas mass flow through the entire train. The model predicts that

- gas outlet temperature from $\mathrm{HX}_1$ decreases with $\lambda$
- downstream stages see slightly higher inlet and outlet temperatures because of increased gas flow and reduced approach to the water side
- water outlet temperatures change only mildly since the water side duty is limited by saturation and approach temperatures

These patterns are visible in the stage temperature plot

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_lambda_stage_temperatures.png}
\caption{Stage wise gas and water outlet temperature profiles along the heat exchanger train for different excess air ratios $\lambda$}
\label{fig:lambda_stage_temperatures}
\end{figure}

Radiative duty in the furnace dominated stage decreases with $\lambda$ due to lower gas temperature and emissivity while convective duty in later tube banks gains relative importance. The combination is shown by

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_lambda_stage_duties.png}
\caption{Variation of stage heat duties and overall conductance $UA$ with excess air ratio $\lambda$ for each heat exchanger stage}
\label{fig:lambda_stage_duties}
\end{figure}

Hydraulics

Higher flue gas flow causes increased frictional pressure losses particularly in tube banks $\mathrm{HX}_3$ and $\mathrm{HX}_5$. Minor losses in reversal chambers scale similarly but contribute less to the total. The trend is documented in

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_lambda_stage_dp.png}
\caption{Gas side pressure loss per heat exchanger stage as a function of excess air ratio $\lambda$}
\label{fig:lambda_stage_dp}
\end{figure}

### Drum pressure

The drum pressure series changes the saturation pressure on the water side at fixed firing rate and air supply and thus modifies saturation temperature thermodynamic properties and steam capacity.

Boiler level effects

Increasing drum pressure raises saturation temperature and enthalpy of evaporation which has two main consequences

- steam mass flow $\dot m_{\mathrm{steam}}$ decreases when moving from low to high pressure because more energy per unit mass is required to reach the higher saturation state
- indirect efficiency $\eta_{\mathrm{indirect}}$ changes only slightly since the total heat absorbed remains close to the control case and stack temperature varies modestly

These effects are summarized in the pressure sensitivity overview and compact plots

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_pressure_boiler_overview.png}
\caption{Boiler level performance indicators as a function of drum pressure including heat input efficiencies water flow rate steam capacity stack temperature and gas side pressure drop}
\label{fig:pressure_boiler_overview}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_pressure_compact_summary.png}
\caption{Summary of boiler efficiency stack temperature steam capacity and steam enthalpy as a function of drum pressure}
\label{fig:pressure_compact_summary}
\end{figure}

The trade off between steam flow and steam specific enthalpy is highlighted explicitly in

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_pressure_steam_tradeoff.png}
\caption{Trade off between steam mass flow rate and steam specific enthalpy as drum pressure is varied}
\label{fig:pressure_steam_tradeoff}
\end{figure}

Stage wise duties and economizer behavior

Because the gas side boundary conditions are almost unchanged, gas temperatures and pressure drops along the stages show only minor variation with drum pressure. Instead the redistribution happens largely on the water side

- early radiant and convective stages adjust their outlet water temperatures according to the new saturation level
- the economizer duty becomes more sensitive to pressure because it heats subcooled water up to a pressure dependent approach to saturation

These effects are captured in

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_pressure_stage_duties.png}
\caption{Stage wise total heat duties as a function of drum pressure for each heat exchanger stage}
\label{fig:pressure_stage_duties}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_pressure_economiser.png}
\caption{Economizer temperature levels and heat duty as a function of drum pressure including gas and water inlet and outlet temperatures and the economizer heat load}
\label{fig:pressure_economiser}
\end{figure}

### Fuel mass flow

The fuel flow series scales the firing rate over a range from approximately $\dot m_{\mathrm f} = 0.025$ to $0.1 \ \mathrm{kg \ s^{-1}}$ while maintaining a constant excess air ratio and drum pressure. This effectively changes the boiler load.

Boiler level effects

The primary observation is an almost linear relation between firing rate and both useful duty and steam capacity within the investigated range

- total input $Q_{\mathrm{in}}$ and useful output $Q_{\mathrm{useful}}$ increase nearly proportionally to $\dot m_{\mathrm f}$
- steam capacity $\dot m_{\mathrm{steam}}$ follows the same nearly linear trend
- direct and indirect efficiencies remain roughly constant with small deviations at the lowest and highest loads
- stack temperature $T_{\mathrm{stack}}$ and gas side pressure loss $\Delta p_{\mathrm{gas}}$ increase with firing rate due to higher gas temperatures and velocities

These relations are illustrated in the boiler overview and linearity plots

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_fuel_boiler_overview.png}
\caption{Boiler performance as a function of fuel firing rate showing heat input efficiencies steam capacity stack temperature and gas side pressure drop}
\label{fig:fuel_boiler_overview}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_fuel_linearity.png}
\caption{Linearity of useful heat output and steam capacity with respect to boiler firing rate comparing against and steam capacity against fuel mass flow}
\label{fig:fuel_linearity}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_fuel_compact_summary.png}
\caption{Compact summary of boiler efficiency stack temperature steam capacity and gas side pressure drop as a function of fuel mass flow}
\label{fig:fuel_compact_summary}
\end{figure}

Stage wise temperatures duties and hydraulics

Increasing firing rate raises gas temperatures and velocities through all stages

- $\mathrm{HX}_1$ and $\mathrm{HX}_3$ experience the largest increase in duty and gas velocity
- water outlet temperatures rise, especially in earlier stages, while economizer approach temperature remains constrained by design
- gas side pressure losses grow strongly with load, dominated by friction in tube banks

These effects are documented in the stage plots

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_fuel_stage_temperatures.png}
\caption{Gas and water outlet temperature profiles along the heat exchanger train for various boiler firing rates}
\label{fig:fuel_stage_temperatures}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/sens/fig_fuel_stage_duty_dp.png}
\caption{Stage wise heat duties and gas side pressure losses as a function of fuel mass flow for all heat exchanger stages}
\label{fig:fuel_stage_duty_dp}
\end{figure}

## Cross comparison and global patterns

The global sensitivity landscape can be inspected by combining all runs across parameter groups

- Changes in excess air ratio $\lambda$ mostly affect efficiency and gas side hydraulics at almost constant steam capacity
- Changes in drum pressure mainly alter the balance between steam mass flow and enthalpy with minor efficiency impact
- Changes in fuel flow have the strongest impact on absolute duties steam capacity and pressure drops while leaving efficiencies relatively flat

The correlation between efficiency and stack temperature across all cases is shown in

\begin{figure}[p]
\centering
\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/sens/fig_global_eta_vs_stack.png}
\caption{Global relationship between indirect boiler efficiency and stack gas temperature across all sensitivity runs}
\label{fig:global_eta_vs_stack}
\end{minipage}

\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_Q_total.png}
\caption{Heat duty per heat exchanger stage and simulation run shown as a run stage heatmap of total duty}
\label{fig:heatmap_Q_total}
\end{minipage}
\end{figure}
\clearpage

Additional structure in the run and stage dimensions is captured by the heatmap set

\begin{figure}[p]
\centering
\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_Q_conv.png}
\caption{Convective part of the heat duty per heat exchanger stage and simulation run}
\label{fig:heatmap_Q_conv}
\end{minipage}

\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_Q_rad.png}
\caption{Radiative part of the heat duty per heat exchanger stage and simulation run}
\label{fig:heatmap_Q_rad}
\end{minipage}
\end{figure}
\clearpage

\begin{figure}[p]
\centering
\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_UA.png}
\caption{Overall heat transfer conductance $UA$ per heat exchanger stage and simulation run}
\label{fig:heatmap_UA}
\end{minipage}

\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_T_gas_in.png}
\caption{Gas inlet temperature distribution over runs and heat exchanger stages}
\label{fig:heatmap_T_gas_in}
\end{minipage}
\end{figure}
\clearpage

Temperature distributions across runs and stages are summarized as

\begin{figure}[p]
\centering
\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_T_gas_out.png}
\caption{Gas outlet temperature distribution over runs and heat exchanger stages}
\label{fig:heatmap_T_gas_out}
\end{minipage}

\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_T_water_in.png}
\caption{Water inlet temperature distribution over runs and heat exchanger stages}
\label{fig:heatmap_T_water_in}
\end{minipage}
\end{figure}
\clearpage

\begin{figure}[p]
\centering
\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_T_water_out.png}
\caption{Water outlet temperature distribution over runs and heat exchanger stages}
\label{fig:heatmap_T_water_out}
\end{minipage}

\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_v_gas.png}
\caption{Gas velocity per heat exchanger stage and simulation run}
\label{fig:heatmap_v_gas}
\end{minipage}
\end{figure}
\clearpage

The hydraulic and velocity structure is presented by

\begin{figure}[p]
\centering
\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_v_water.png}
\caption{Water velocity per heat exchanger stage and simulation run}
\label{fig:heatmap_v_water}
\end{minipage}

\begin{minipage}{\textwidth}
\centering
\includegraphics[width=\textwidth,height=0.45\textheight,keepaspectratio]{results/plots/map/heatmap_dp_total.png}
\caption{Total gas side pressure drop per heat exchanger stage and simulation run}
\label{fig:heatmap_dp_total}
\end{minipage}
\end{figure}
\clearpage

Together the sensitivity series show that the boiler is most sensitive in absolute capacity and hydraulic load to the firing rate $\dot m_{\mathrm f}$ while mixture control via $\lambda$ is the dominant lever for efficiency and stack loss and drum pressure mainly tunes the thermodynamic quality and quantity of the generated steam
