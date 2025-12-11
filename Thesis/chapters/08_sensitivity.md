# Boiler performance analysis

The present chapter evaluates the thermal and hydraulic performance of the fire tube boiler model based on steady state simulations of a reference control case and systematic parameter variations. The analysis is structured to introduce the control case first and then to discuss the influence of excess air factor, fuel mass flow, and drum pressure, followed by a stage wise interpretation of heat transfer and gas side hydraulics.

## Control case

Table: Control case performance.

| Control                        | control |
| :----------------------------- | ------: |
| fuel mass flow[kg/s]           |     0.1 |
| air flow[kg/s]                 |    1.77 |
| excess air ratio[-]            |     1.1 |
| water flow[kg/s]               |    1.78 |
| steam capacity[t/h]            |    7.45 |
| $\eta_{\mathrm{direct}} [-]$   |    0.89 |
| $\eta_{\mathrm{indirect}} [-]$ |    0.89 |
| Conductance [MW/K]             |    0.01 |
| Input heat [MW]                |     4.7 |
| Useful heat [MW]               |    4.17 |
| pressure drop fric total[Pa]   |  -59.43 |
| pressure drop minor total[Pa]  |  -15.54 |
| pressure drop total[Pa]        |  -74.96 |
| LHV [MJ/kg]                    |   46.97 |
| Firing rate [MW]               |     4.7 |
| Adiabatic temperature [°C]     | 1900.61 |
| stack temperature[°C]          |  181.41 |

The control case corresponds to the nominal design operation introduced in the previous chapters and serves as the reference state for all relative comparisons in this chapter.

## Global boiler performance

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/kpi_overview_all_param_groups.png}
\caption{Overview of key boiler performance indicators for all parameter groups}
\label{fig:kpi_overview_all_param_groups}
\end{figure}

This figure provides a compact summary of how the different parameter groups shift the global performance relative to the control case introduced above. In the remainder of the chapter, each parameter group is analyzed separately.

## Influence of excess air factor

$$
\lambda = [1.0, 1.1, 1.2, 1.3]
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_excess_air.png}
\caption{Boiler performance as a function of excess air factor}
\label{fig:performance_excess_air}
\end{figure}

Decreasing $\lambda$ towards stoichiometric conditions increases $T_{\mathrm{ad}}$ and the fraction of duty absorbed in the radiant section, while increasing $\lambda$ leads to higher stack losses due to additional sensible heat in the flue gas.

Table: Excess air performance analysis. {#tbl:excess_air_performance}

| Excess air [-]                 |    1.00 |    1.10 |    1.20 |    1.30 |
| :----------------------------- | ------: | ------: | ------: | ------: |
| fuel mass flow[kg/s]           |     0.1 |     0.1 |     0.1 |     0.1 |
| air flow[kg/s]                 |    1.61 |    1.77 |    1.93 |    2.09 |
| excess air ratio[-]            |       1 |     1.1 |     1.2 |     1.3 |
| water flow[kg/s]               |    1.79 |    1.78 |    1.77 |    1.76 |
| steam capacity[t/h]            |    7.48 |    7.45 |     7.4 |    7.36 |
| $\eta_{\mathrm{direct}} [-]$   |    0.89 |    0.89 |    0.88 |    0.88 |
| $\eta_{\mathrm{indirect}} [-]$ |    0.89 |    0.89 |    0.88 |    0.88 |
| Conductance [MW/K]             |    0.01 |    0.01 |    0.01 |    0.01 |
| Input heat [MW]                |     4.7 |     4.7 |     4.7 |     4.7 |
| Useful heat [MW]               |    4.19 |    4.17 |    4.14 |    4.12 |
| pressure drop fric total[Pa]   |  -49.46 |  -59.43 |  -70.27 |  -81.95 |
| pressure drop minor total[Pa]  |  -12.82 |  -15.54 |  -18.49 |  -21.65 |
| pressure drop total[Pa]        |  -62.28 |  -74.96 |  -88.76 |  -103.6 |
| LHV [MJ/kg]                    |   46.97 |   46.97 |   46.97 |   46.97 |
| Firing rate [MW]               |     4.7 |     4.7 |     4.7 |     4.7 |
| Adiabatic temperature [°C]     | 2036.41 | 1900.61 | 1782.51 | 1678.83 |
| stack temperature[°C]          |  175.78 |  181.41 |  186.78 |  191.89 |

Key observations from [@tbl:excess_air_performance] are:

- Increasing excess air from $\lambda = 1.0$ to $\lambda = 1.3$ decreases the direct efficiency from about $0.891$ to $0.876$ ($\approx 1.5\%$).
- Over the same range, stack temperature increases from approximately 176 °C to 192 °C, indicating higher sensible heat losses with the flue gas.
- The total gas side pressure drop rises from about −62 Pa to −104 Pa as air flow and hence gas mass flow increase.
- The useful heat $Q_\mathrm{useful}$ decreases slightly with $\lambda$, while the overall conductance $UA$ increases modestly due to higher gas side Reynolds numbers.

## Influence of fuel mass flow

$$
\dot{m}_\mathrm{fuel} = [0.10, 0.075, 0.050, 0.025]
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_fuel_flow.png}
\caption{Boiler performance as a function of fuel mass flow}
\label{fig:performance_fuel_flow}
\end{figure}

The fuel mass flow sweep explores operation between $25\%$ and $100\%$ of nominal firing rate. As the load increases, the higher gas mass flow and gas side Reynolds numbers enhance convective heat transfer, particularly in HX3 and HX5, while also increasing gas side pressure drops and velocities.

Table: Fuel flow performance analysis. {#tbl:fuel_flow_performance}

| Fuel flow [kg/s]               |    0.02 |    0.05 |    0.08 |    0.10 |
| :----------------------------- | ------: | ------: | ------: | ------: |
| fuel mass flow[kg/s]           |    0.02 |    0.05 |    0.08 |     0.1 |
| air flow[kg/s]                 |    0.44 |    0.89 |    1.33 |    1.77 |
| excess air ratio[-]            |     1.1 |     1.1 |     1.1 |     1.1 |
| water flow[kg/s]               |    0.46 |     0.9 |    1.35 |    1.78 |
| steam capacity[t/h]            |    1.91 |    3.78 |    5.62 |    7.45 |
| $\eta_{\mathrm{direct}} [-]$   |    0.91 |     0.9 |    0.89 |    0.89 |
| $\eta_{\mathrm{indirect}} [-]$ |    0.91 |     0.9 |    0.89 |    0.89 |
| Conductance [MW/K]             |       0 |    0.01 |    0.01 |    0.01 |
| Input heat [MW]                |    1.18 |    2.35 |    3.53 |     4.7 |
| Useful heat [MW]               |    1.07 |    2.11 |    3.15 |    4.17 |
| pressure drop fric total[Pa]   |   -2.79 |  -15.03 |  -33.54 |  -59.43 |
| pressure drop minor total[Pa]  |   -0.68 |   -3.25 |   -8.13 |  -15.54 |
| pressure drop total[Pa]        |   -3.47 |  -18.28 |  -41.67 |  -74.96 |
| LHV [MJ/kg]                    |   46.97 |   46.97 |   46.97 |   46.97 |
| Firing rate [MW]               |    1.17 |    2.35 |    3.52 |     4.7 |
| Adiabatic temperature [°C]     | 1900.61 | 1900.61 | 1900.61 | 1900.61 |
| stack temperature[°C]          |  131.25 |  150.24 |  166.78 |  181.41 |

Key observations from [@tbl:fuel_flow_performance] are:

- As fuel mass flow increases from 0.025 to 0.1 kg/s (25% to 100% load), steam capacity rises from about 1.9 t/h to 7.4 t/h.
- The direct efficiency decreases slightly with load, from around 0.908 at 25% load to 0.887 at 100% load.
- The gas-side pressure drop increases strongly with load, from about −3 Pa to −75 Pa, reflecting the approximate quadratic dependence on gas mass flow.
- Stack temperature increases from roughly 131 °C at 25% load to 181 °C at full load, which indicates less complete heat recovery at high firing rates.

## Influence of drum pressure

$$
P_\mathrm{Drum} = [4.0, 10.0, 16.0] bar
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_water_pressure.png}
\caption{Boiler performance as a function of drum pressure}
\label{fig:performance_water_pressure}
\end{figure}

The drum pressure variation modifies the steam saturation temperature and thus the driving temperature difference between flue gas and water or steam on each heat exchanger surface.

Table: Drum pressure performance analysis. {#tbl:drum_pressure_performance}

| Water pressure [bar]           |    4.00 |   10.00 |   16.00 |
| :----------------------------- | ------: | ------: | ------: |
| fuel mass flow[kg/s]           |     0.1 |     0.1 |     0.1 |
| air flow[kg/s]                 |    1.77 |    1.77 |    1.77 |
| excess air ratio[-]            |     1.1 |     1.1 |     1.1 |
| water flow[kg/s]               |    1.83 |    1.78 |    1.76 |
| steam capacity[t/h]            |    7.09 |    7.45 |    7.71 |
| $\eta_{\mathrm{direct}} [-]$   |    0.89 |    0.89 |    0.88 |
| $\eta_{\mathrm{indirect}} [-]$ |    0.89 |    0.89 |    0.88 |
| Conductance [MW/K]             |    0.01 |    0.01 |    0.01 |
| Input heat [MW]                |     4.7 |     4.7 |     4.7 |
| Useful heat [MW]               |     4.2 |    4.17 |    4.14 |
| pressure drop fric total[Pa]   |   -57.2 |  -59.43 |  -60.78 |
| pressure drop minor total[Pa]  |  -15.46 |  -15.54 |  -15.59 |
| pressure drop total[Pa]        |  -72.66 |  -74.96 |  -76.37 |
| LHV [MJ/kg]                    |   46.97 |   46.97 |   46.97 |
| Firing rate [MW]               |     4.7 |     4.7 |     4.7 |
| Adiabatic temperature [°C]     | 1900.61 | 1900.61 | 1900.61 |
| stack temperature[°C]          |  162.68 |  181.41 |  192.08 |

Key observations from [@tbl:drum_pressure_performance] are:

- At fixed fuel and air flows, increasing drum pressure from 4 bar to 16 bar increases steam capacity from about 7.1 t/h to 7.7 t/h due to higher steam enthalpy.
- The direct efficiency decreases from about 0.895 at 4 bar to 0.882 at 16 bar, as higher water/steam temperatures reduce the driving temperature difference on the gas side.
- Stack temperature increases from approximately 163 °C at 4 bar to 192 °C at 16 bar, reflecting the reduced potential for additional heat recovery.
- Gas-side pressure drops remain essentially unchanged with drum pressure because gas mass flow and gas-side geometry are not affected.

## Stage wise heat transfer behavior

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/stages_param_groups.png}
\caption{Stage wise heat exchanger duty, conductance, outlet temperature, and pressure drop for all parameter groups}
\label{fig:stages_param_groups}
\end{figure}

Variations in $\lambda$ primarily affect $Q_{\mathrm{stage}}$ and $UA$ in the radiant section and the first convective bank, while load changes affect both the magnitude and the distribution of duty along the gas path. The drum pressure variation, alters the effective $UA$ utilization in each stage.

Variations in $\lambda$ primarily affect $Q_{\mathrm{stage}}$ and $UA$ in the radiant section (HX1) and the first convective bank (HX3). At lower excess air (higher $T_{\mathrm{ad}}$), these stages absorb a larger fraction of the total duty, while the downstream convective banks see a reduced relative share. Increasing $\lambda$ shifts some duty towards the later convective stages but also raises stack losses.

Load changes affect both the magnitude and the distribution of duty along the gas path. At low load, duty is concentrated in the early stages and the later convective banks are underutilized, resulting in low gas velocities and small pressure drops. As load increases, $Q_{\mathrm{stage}}$ grows in all stages, with a particularly strong relative increase in the convective banks where the higher gas-side Reynolds numbers strongly enhance $UA$.

The drum pressure variation mainly alters the effective utilization of $UA$ in each stage rather than the absolute $UA$ values. Higher drum pressure increases water/steam temperature and therefore reduces the local temperature differences, especially in the later convective stages where gas temperatures are already low. This leads to a shift of the effective heat transfer towards the upstream stages and contributes to the observed increase in stack temperature at high pressure.

## Gas side hydraulics and heat transfer decomposition

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/stages_velocity_pressure_Qsum_UA.png}
\caption{Stage wise gas velocity, gas pressure, heat transfer decomposition, and conductance}
\label{fig:stages_velocity_pressure_Qsum_UA}
\end{figure}

The figure clarifies how changes in fuel mass flow and excess air factor translate into different velocity and pressure profiles and how this in turn influences heat transfer modes in each heat exchanger. The presented data enable a consistent interpretation of how hydraulic margins evolve with operating point and how close individual stages approach practical constraints such as allowable gas velocity or pressure drop. In combination with the previous plots, this information supports the identification of an operating window that balances efficiency, steam conditions, and hydraulic safety.

Figure clarifies how changes in fuel mass flow and excess air factor translate into different velocity and pressure profiles and how this in turn influences heat transfer modes in each heat exchanger. For increasing load, the gas velocity in all stages increases approximately in proportion to mass flow, and the stage-wise pressure drops increase roughly with the square of velocity. This behavior is most pronounced in the convective tube banks, where friction losses dominate.

At high load and high excess air, the maximum stage-wise gas velocity approaches the upper range of typical design values for fire tube boilers, while the total pressure drop remains within the available fan head. At low load, gas velocities are small, especially in the last convective stage, which may limit convective heat transfer and affect combustion stability in practice.

The presented data therefore enable a consistent interpretation of how hydraulic margins evolve with operating point and how close individual stages approach practical constraints such as allowable gas velocity or pressure drop. In combination with the previous plots, this information supports the identification of an operating window that balances efficiency, steam conditions, and hydraulic safety.
