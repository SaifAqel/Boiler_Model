# Performance analysis

The present chapter evaluates the thermal and hydraulic performance of the fire tube boiler model based on steady state simulations of a reference control case and systematic parameter variations.

## Control case

The control case is defined by a fuel mass flow of $\dot m_\mathrm{fuel}=0.1\ \mathrm{kg\,s^{-1}}$, an excess air ratio of $\lambda=1.1$, and a drum pressure of $P_\mathrm{drum}=10\ \mathrm{bar}$. These values represent the nominal operating point of the boiler and are used as the reference state throughout this chapter.

Table: Control case performance.

| control                              | control |
| :----------------------------------- | ------: |
| fuel mass flow[kg/s]                 |     0.1 |
| air flow[kg/s]                       |    1.77 |
| excess air ratio[-]                  |     1.1 |
| feedwater flow[kg/s]                 |     1.8 |
| steam capacity[t/h]                  |    6.48 |
| $\eta_{\mathrm{direct}}$ [-]         |    0.89 |
| $\eta_{\mathrm{indirect}}$ [-]       |    0.89 |
| conductance [MW/K]                   |    0.01 |
| input heat [MW]                      |     4.7 |
| useful heat [MW]                     |     4.2 |
| pressure drop fric total[kpa]        |   -0.34 |
| pressure drop minor total[kpa]       |   -0.76 |
| pressure drop total[kpa]             |    -1.1 |
| water pressure drop fric total[kpa]  |   -6.92 |
| water pressure drop minor total[kpa] |   -0.24 |
| water pressure drop total[kpa]       |   -7.16 |
| lhv [mj/kg]                          |   46.97 |
| firing rate [MW]                     |     4.7 |
| adiabatic temperature [°C]           | 1915.54 |
| stack temperature[°c]                |  169.39 |
| feedwater pressure[kpa]              | 1007.16 |
| drum pressure[kpa]                   |    1000 |

## Global boiler performance

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/kpi_overview_all_param_groups.png}
\caption{Overview of key boiler performance indicators for all parameter groups}
\label{fig:kpi_overview_all_param_groups}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/scatter_efficiency_vs_stack_temperature_all_runs.png}
\caption{Scatter diagram showing stack temperature and direct efficiency}
\label{fig:scatter_stack_eta}
\end{figure}

\newpage

## Influence of excess air factor

$$
\lambda = [1.00, 1.05, 1.10, 1.15, 1.20, 1.30]\; [-]
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_excess_air.png}
\caption{Boiler performance as a function of excess air factor}
\label{fig:performance_excess_air}
\end{figure}

At low excess air levels, a moderate increase in $\lambda$ improves combustion completeness and slightly stabilizes heat release, resulting in nearly constant efficiency around the control point. Beyond this region, additional air primarily increases the sensible heat carried by the flue gas, which directly increases stack losses and reduces efficiency.

Table: Excess air performance analysis.

| excess air [-]                       |    1.00 |    1.05 |    1.10 |    1.15 |    1.20 |    1.30 |
| :----------------------------------- | ------: | ------: | ------: | ------: | ------: | ------: |
| fuel mass flow[kg/s]                 |     0.1 |     0.1 |     0.1 |     0.1 |     0.1 |     0.1 |
| air flow[kg/s]                       |    1.61 |    1.69 |    1.77 |    1.85 |    1.93 |    2.09 |
| excess air ratio[-]                  |       1 |    1.05 |     1.1 |    1.15 |     1.2 |     1.3 |
| feedwater flow[kg/s]                 |     1.8 |     1.8 |     1.8 |    1.79 |    1.79 |    1.78 |
| steam capacity[t/h]                  |     6.5 |    6.49 |    6.48 |    6.46 |    6.44 |    6.41 |
| $\eta_{\mathrm{direct}}$ [-]         |     0.9 |     0.9 |    0.89 |    0.89 |    0.89 |    0.89 |
| $\eta_{\mathrm{indirect}}$ [-]       |     0.9 |     0.9 |    0.89 |    0.89 |    0.89 |    0.89 |
| conductance [MW/K]                   |    0.01 |    0.01 |    0.01 |    0.01 |    0.01 |    0.01 |
| input heat [MW]                      |     4.7 |     4.7 |     4.7 |     4.7 |     4.7 |     4.7 |
| useful heat [MW]                     |    4.22 |    4.21 |     4.2 |    4.19 |    4.18 |    4.16 |
| pressure drop fric total[kpa]        |   -0.29 |   -0.31 |   -0.34 |   -0.37 |   -0.41 |   -0.47 |
| pressure drop minor total[kpa]       |   -0.63 |   -0.69 |   -0.76 |   -0.83 |   -0.91 |   -1.07 |
| pressure drop total[kpa]             |   -0.91 |   -1.01 |    -1.1 |   -1.21 |   -1.31 |   -1.54 |
| water pressure drop fric total[kpa]  |   -6.97 |   -6.94 |   -6.92 |   -6.89 |   -6.86 |   -6.79 |
| water pressure drop minor total[kpa] |   -0.24 |   -0.24 |   -0.24 |   -0.24 |   -0.24 |   -0.24 |
| water pressure drop total[kpa]       |   -7.21 |   -7.19 |   -7.16 |   -7.13 |    -7.1 |   -7.02 |
| lhv [mj/kg]                          |   46.97 |   46.97 |   46.97 |   46.97 |   46.97 |   46.97 |
| firing rate [MW]                     |     4.7 |     4.7 |     4.7 |     4.7 |     4.7 |     4.7 |
| adiabatic temperature [°C]           | 2052.36 |  1981.5 | 1915.54 | 1854.03 | 1796.53 | 1692.05 |
| stack temperature[°c]                |   164.6 |  167.01 |  169.39 |  171.74 |  174.05 |  178.56 |
| feedwater pressure[kpa]              | 1007.21 | 1007.19 | 1007.16 | 1007.13 |  1007.1 | 1007.02 |
| drum pressure[kpa]                   |    1000 |    1000 |    1000 |    1000 |    1000 |    1000 |

Increasing the excess air ratio increases the total gas side pressure drop as higher air flow leads to greater flue gas mass flow.

\newpage

## Influence of fuel mass flow

$$
\dot{m}_\mathrm{fuel} = [0.025, 0.050, 0.075, 0.10, 0.20]\; \frac{kg}{s}
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_fuel_flow.png}
\caption{Boiler performance as a function of fuel mass flow}
\label{fig:performance_fuel_flow}
\end{figure}

Steam capacity increases approximately linearly with fuel input, indicating that the available heat transfer surface is sufficient to absorb the additional duty. As the firing rate approaches the nominal design value, deviations from linearity become apparent, reflecting increasing limitations in heat transfer effectiveness rather than fuel input.

Table: Fuel flow performance analysis.

| fuel flow [kg/s]                     |    0.02 |    0.05 |    0.08 |    0.10 |    0.20 |
| :----------------------------------- | ------: | ------: | ------: | ------: | ------: |
| fuel mass flow[kg/s]                 |    0.02 |    0.05 |    0.08 |     0.1 |     0.2 |
| air flow[kg/s]                       |    0.44 |    0.89 |    1.33 |    1.77 |    3.54 |
| excess air ratio[-]                  |     1.1 |     1.1 |     1.1 |     1.1 |     1.1 |
| feedwater flow[kg/s]                 |    0.46 |    0.91 |    1.36 |     1.8 |    3.53 |
| steam capacity[t/h]                  |    1.65 |    3.27 |    4.88 |    6.48 |    12.7 |
| $\eta_{\mathrm{direct}}$ [-]         |    0.91 |     0.9 |     0.9 |    0.89 |    0.88 |
| $\eta_{\mathrm{indirect}}$ [-]       |    0.91 |     0.9 |     0.9 |    0.89 |    0.88 |
| conductance [MW/K]                   |       0 |    0.01 |    0.01 |    0.01 |    0.02 |
| input heat [MW]                      |    1.18 |    2.35 |    3.53 |     4.7 |     9.4 |
| useful heat [MW]                     |    1.07 |    2.12 |    3.17 |     4.2 |    8.24 |
| pressure drop fric total[kpa]        |   -0.02 |   -0.09 |   -0.19 |   -0.34 |   -1.42 |
| pressure drop minor total[kpa]       |   -0.04 |   -0.18 |   -0.42 |   -0.76 |   -3.38 |
| pressure drop total[kpa]             |   -0.07 |   -0.27 |   -0.61 |    -1.1 |   -4.79 |
| water pressure drop fric total[kpa]  |   -0.57 |   -1.97 |   -4.11 |   -6.92 |  -24.46 |
| water pressure drop minor total[kpa] |   -0.02 |   -0.06 |   -0.14 |   -0.24 |   -0.93 |
| water pressure drop total[kpa]       |   -0.59 |   -2.04 |   -4.24 |   -7.16 |  -25.38 |
| lhv [mj/kg]                          |   46.97 |   46.97 |   46.97 |   46.97 |   46.97 |
| firing rate [MW]                     |    1.17 |    2.35 |    3.52 |     4.7 |    9.39 |
| adiabatic temperature [°C]           | 1915.54 | 1915.54 | 1915.54 | 1915.54 | 1915.54 |
| stack temperature[°c]                |  135.16 |  146.82 |  158.25 |  169.39 |  209.97 |
| feedwater pressure[kpa]              | 1000.59 | 1002.04 | 1004.24 | 1007.16 | 1025.38 |
| drum pressure[kpa]                   |    1000 |    1000 |    1000 |    1000 |    1000 |

\newpage

## Influence of drum pressure

$$
P_\mathrm{Drum} = [4.0, 10.0, 16.0]\; \mathrm{bar}
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_water_pressure.png}
\caption{Boiler performance as a function of drum pressure}
\label{fig:performance_water_pressure}
\end{figure}

The drum pressure variation modifies the steam saturation temperature and thus the driving temperature difference between flue gas and water/steam on each heat exchanger surface.

Table: Drum pressure performance analysis. {#tbl:drum_pressure_performance}

| drum pressure [bar]                  |    4.00 |   10.00 |   16.00 |
| :----------------------------------- | ------: | ------: | ------: |
| fuel mass flow[kg/s]                 |     0.1 |     0.1 |     0.1 |
| air flow[kg/s]                       |    1.77 |    1.77 |    1.77 |
| excess air ratio[-]                  |     1.1 |     1.1 |     1.1 |
| feedwater flow[kg/s]                 |    1.84 |     1.8 |    1.78 |
| steam capacity[t/h]                  |    6.64 |    6.48 |     6.4 |
| $\eta_{\mathrm{direct}}$ [-]         |     0.9 |    0.89 |    0.89 |
| $\eta_{\mathrm{indirect}}$ [-]       |     0.9 |    0.89 |    0.89 |
| conductance [MW/K]                   |    0.01 |    0.01 |    0.01 |
| input heat [MW]                      |     4.7 |     4.7 |     4.7 |
| useful heat [MW]                     |    4.24 |     4.2 |    4.18 |
| pressure drop fric total[kpa]        |   -0.32 |   -0.34 |   -0.35 |
| pressure drop minor total[kpa]       |   -0.72 |   -0.76 |   -0.78 |
| pressure drop total[kpa]             |   -1.05 |    -1.1 |   -1.14 |
| water pressure drop fric total[kpa]  |   -7.26 |   -6.92 |   -6.77 |
| water pressure drop minor total[kpa] |   -0.25 |   -0.24 |   -0.24 |
| water pressure drop total[kpa]       |   -7.51 |   -7.16 |      -7 |
| lhv [mj/kg]                          |   46.97 |   46.97 |   46.97 |
| firing rate [MW]                     |     4.7 |     4.7 |     4.7 |
| adiabatic temperature [°C]           | 1915.54 | 1915.54 | 1915.54 |
| stack temperature[°c]                |  152.15 |  169.39 |  179.55 |
| feedwater pressure[kpa]              |  407.51 | 1007.16 |    1607 |
| drum pressure[kpa]                   |     400 |    1000 |    1600 |

Increasing the drum pressure, raises the steam capacity because the latent heat of vaporization decreases with increasing pressure, allowing a larger steam mass flow to be generated for the same absorbed thermal duty. The direct efficiency decreases, since higher water and steam temperatures reduce the available driving temperature difference on the gas side. Consistent with this, the stack temperature increases, indicating a diminished potential for further heat recovery.

\newpage

## Influence of fouling

$$
f = [0.5,\; 1.0,\; 2.0,\; 5.0,\; 10.0]\;[-]
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_fouling.png}
\caption{Boiler performance as a function of fouling factor}
\label{fig:performance_fouling}
\end{figure}

The fouling factor represents a degradation of the effective heat transfer surfaces on the gas side and water side heat exchangers. Increasing fouling reduces the overall heat transfer coefficient, directly lowering the effective conductance, weakening heat recovery throughout the boiler, resulting in higher stack temperatures and reduced boiler efficiency.

The effect of fouling is distributed across all stages, but its impact is most pronounced in the downstream convective sections where heat transfer is already limited by smaller temperature differences. As fouling increases, these sections lose effectiveness first.

Table: Fouling performance analysis.

| fouling [-]                          |    0.50 |    1.00 |    2.00 |    5.00 |   10.00 |
| :----------------------------------- | ------: | ------: | ------: | ------: | ------: |
| fuel mass flow[kg/s]                 |     0.1 |     0.1 |     0.1 |     0.1 |     0.1 |
| air flow[kg/s]                       |    1.77 |    1.77 |    1.77 |    1.77 |    1.77 |
| excess air ratio[-]                  |     1.1 |     1.1 |     1.1 |     1.1 |     1.1 |
| feedwater flow[kg/s]                 |     1.8 |     1.8 |     1.8 |    1.79 |    1.78 |
| steam capacity[t/h]                  |    6.48 |    6.48 |    6.47 |    6.45 |    6.42 |
| $\eta_{\mathrm{direct}}$ [-]         |     0.9 |    0.89 |    0.89 |    0.89 |    0.89 |
| $\eta_{\mathrm{indirect}}$ [-]       |    0.89 |    0.89 |    0.89 |    0.89 |    0.89 |
| conductance [MW/K]                   |    0.01 |    0.01 |    0.01 |    0.01 |    0.01 |
| input heat [MW]                      |     4.7 |     4.7 |     4.7 |     4.7 |     4.7 |
| useful heat [MW]                     |     4.2 |     4.2 |     4.2 |    4.19 |    4.17 |
| pressure drop fric total[kpa]        |   -0.34 |   -0.34 |   -0.34 |   -0.35 |   -0.37 |
| pressure drop minor total[kpa]       |   -0.76 |   -0.76 |   -0.76 |   -0.78 |    -0.8 |
| pressure drop total[kpa]             |    -1.1 |    -1.1 |   -1.11 |   -1.13 |   -1.17 |
| water pressure drop fric total[kpa]  |   -6.92 |   -6.92 |   -6.91 |   -6.87 |    -6.8 |
| water pressure drop minor total[kpa] |   -0.24 |   -0.24 |   -0.24 |   -0.24 |   -0.24 |
| water pressure drop total[kpa]       |   -7.16 |   -7.16 |   -7.15 |   -7.11 |   -7.04 |
| lhv [mj/kg]                          |   46.97 |   46.97 |   46.97 |   46.97 |   46.97 |
| firing rate [MW]                     |     4.7 |     4.7 |     4.7 |     4.7 |     4.7 |
| adiabatic temperature [°C]           | 1915.54 | 1915.54 | 1915.54 | 1915.54 | 1915.54 |
| stack temperature[°c]                |  168.67 |  169.39 |  170.94 |  176.36 |  187.53 |
| feedwater pressure[kpa]              | 1007.16 | 1007.16 | 1007.15 | 1007.11 | 1007.04 |
| drum pressure[kpa]                   |    1000 |    1000 |    1000 |    1000 |    1000 |

While the boiler can continue to operate under fouled conditions, the results highlight the importance of maintaining clean heat transfer surfaces to ensure higher efficiency.

## Stage-wise heat transfer and hydraulics

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/stages_heat.png}
\caption{Stage wise heat transfer profile}
\label{fig:stages_param_groups}
\end{figure}

Across all runs the stage pattern stays the same: gas temperature drops from HX 1 to HX 6, stage heat duty is highest in the first stages and decreases downstream, and early stages are driven mainly by radiative transfer while later stages are relatively more convective. Control cases sit between the minimum and maximum parameter cases, showing smooth scaling rather than any stage wise regime change.

Excess air mainly shifts and weakens heat transfer: higher excess air lowers upstream gas temperatures and reduces early stage duties, pushes a larger share of recovery downstream, and increases gas velocity and total pressure drop across stages. Fuel flow scales everything up or down: higher fuel flow increases gas temperatures, stage duties, and both convective and radiative contributions in all stages, with the biggest absolute changes in the first tube bank section and upstream units, while also increasing pressure drop. Drum pressure has a smaller gas side impact but adjusts downstream recovery through water side conditions, slightly shifting late stage duties and conductance without changing the overall stage wise shape.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/stages_hydraulics.png}
\caption{Stage wise hydraulics and conductance profile }
\label{fig:stages_velocity_pressure_Qsum_UA}
\end{figure}

\newpage
