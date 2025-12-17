# Performance analysis

The present chapter evaluates the thermal and hydraulic performance of the fire tube boiler model based on steady state simulations of a reference control case and systematic parameter variations. The analysis is structured to introduce the control case first and then to discuss the influence of excess air factor, fuel mass flow, and drum pressure.

## Control case

Table: Control case performance.

| control                             |     control |
| :---------------------------------- | ----------: |
| fuel mass flow[kg/s]                |         0.1 |
| air flow[kg/s]                      |        1.77 |
| excess air ratio[-]                 |         1.1 |
| feedwater flow[kg/s]                |         1.8 |
| steam capacity[t/h]                 |        6.48 |
| $\eta_{\mathrm{direct}} [-]$        |        0.89 |
| $\eta_{\mathrm{indirect}} [-]$      |           0 |
| conductance [MW/K]                  |        0.01 |
| input heat [MW]                     |         4.7 |
| useful heat [MW]                    |         4.2 |
| pressure drop fric total[pa]        |      -342.6 |
| pressure drop minor total[pa]       |     -760.56 |
| pressure drop total[pa]             |    -1103.16 |
| water pressure drop fric total[pa]  |    -6918.12 |
| water pressure drop minor total[pa] |     -240.98 |
| water pressure drop total[pa]       |     -7159.1 |
| lhv [mj/kg]                         |       46.97 |
| firing rate [MW]                    |         4.7 |
| adiabatic temperature [°C]          |     1915.54 |
| stack temperature[°c]               |      169.39 |
| feedwater pressure[pa]              | 1.00716e+06 |
| drum pressure[pa]                   |       1e+06 |

The control case is explicitly defined by a fuel mass flow of $\dot m_\mathrm{fuel}=0.1\ \mathrm{kg\,s^{-1}}$, an excess air ratio of $\lambda=1.1$, and a drum pressure of $P_\mathrm{drum}=10\ \mathrm{bar}$. These values represent the nominal operating point of the boiler and are used as the reference state throughout this chapter.

## Global boiler performance

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/kpi_overview_all_param_groups.png}
\caption{Overview of key boiler performance indicators for all parameter groups}
\label{fig:kpi_overview_all_param_groups}
\end{figure}

This figure provides a compact summary of how the different parameter groups shift the global performance relative to the control case introduced above. In the remainder of the chapter, each parameter group is analyzed separately.

\newpage

## Influence of excess air factor

$$
\lambda = [1.0, 1.1, 1.2, 1.3]\; [-]
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_excess_air.png}
\caption{Boiler performance as a function of excess air factor}
\label{fig:performance_excess_air}
\end{figure}

At constant fuel input, increasing the excess air ratio reduces the useful heat. At low excess air levels, a moderate increase in $\lambda$ improves combustion completeness and slightly stabilizes heat release, resulting in nearly constant efficiency around the control point. Beyond this region, additional air primarily increases the sensible heat carried by the flue gas, which directly increases stack losses and reduces both direct and indirect efficiency.

The stack temperature increases with excess air. This behavior is caused by the increased flue gas mass flow rate, which raises the total sensible heat capacity of the gas stream and reduces the effective residence time within the convective heat exchanger banks.

Table: Excess air performance analysis.

| excess air [-]                             |        1.05 |        1.00 |        1.15 |        1.10 |       1.20 |        1.30 |
| :----------------------------------------- | ----------: | ----------: | ----------: | ----------: | ---------: | ----------: |
| fuel mass flow[kg/s]                       |         0.1 |         0.1 |         0.1 |         0.1 |        0.1 |         0.1 |
| air flow[kg/s]                             |        1.69 |        1.61 |        1.85 |        1.77 |       1.93 |        2.09 |
| air flow[kg/s] dev[%]                      |       -4.55 |       -9.09 |        4.55 |           0 |       9.09 |       18.18 |
| excess air ratio[-]                        |        1.05 |           1 |        1.15 |         1.1 |        1.2 |         1.3 |
| excess air ratio[-] dev[%]                 |       -4.55 |       -9.09 |        4.55 |           0 |       9.09 |       18.18 |
| feedwater flow[kg/s]                       |         1.8 |         1.8 |        1.79 |         1.8 |       1.79 |        1.78 |
| feedwater flow[kg/s] dev[%]                |         0.2 |        0.37 |       -0.22 |           0 |      -0.46 |          -1 |
| steam capacity[t/h]                        |        6.49 |         6.5 |        6.46 |        6.48 |       6.44 |        6.41 |
| steam capacity[t/h] dev[%]                 |         0.2 |        0.37 |       -0.22 |           0 |      -0.47 |       -1.01 |
| $\eta_{\mathrm{direct}} [-]$               |         0.9 |         0.9 |        0.89 |        0.89 |       0.89 |        0.89 |
| $\eta_{\mathrm{direct}} [-]$               |         0.2 |        0.37 |       -0.22 |           0 |      -0.46 |       -1.01 |
| $\eta_{\mathrm{indirect}} [-]$             |         0.9 |         0.9 |        0.89 |        0.89 |       0.89 |        0.89 |
| $\eta_{\mathrm{indirect}} [-]$             |         0.2 |        0.38 |       -0.23 |           0 |      -0.47 |       -1.02 |
| conductance [MW/K]                         |        0.01 |        0.01 |        0.01 |        0.01 |       0.01 |        0.01 |
| conductance [MW/K] dev[%]                  |       -1.52 |        -3.1 |        1.46 |           0 |       2.86 |        5.52 |
| input heat [MW]                            |         4.7 |         4.7 |         4.7 |         4.7 |        4.7 |         4.7 |
| input heat [MW] dev[%]                     |          -0 |       -0.01 |           0 |           0 |       0.01 |        0.01 |
| useful heat [MW]                           |        4.21 |        4.22 |        4.19 |         4.2 |       4.18 |        4.16 |
| useful heat [MW] dev[%]                    |         0.2 |        0.37 |       -0.22 |           0 |      -0.46 |       -1.01 |
| pressure drop fric total[pa]               |      -313.3 |     -285.37 |     -373.28 |      -342.6 |    -405.33 |     -473.58 |
| pressure drop fric total[pa] dev[%]        |       -8.55 |       -16.7 |        8.95 |          -0 |      18.31 |       38.23 |
| pressure drop minor total[pa]              |     -692.36 |     -627.65 |     -832.28 |     -760.56 |    -907.54 |    -1068.75 |
| pressure drop minor total[pa] dev[%]       |       -8.97 |      -17.48 |        9.43 |          -0 |      19.32 |       40.52 |
| pressure drop total[pa]                    |    -1005.66 |     -913.02 |    -1205.56 |    -1103.16 |   -1312.87 |    -1542.32 |
| pressure drop total[pa] dev[%]             |       -8.84 |      -17.24 |        9.28 |          -0 |      19.01 |       39.81 |
| water pressure drop fric total[pa]         |    -6944.61 |    -6967.55 |    -6888.79 |    -6918.12 |   -6856.89 |    -6786.36 |
| water pressure drop fric total[pa] dev[%]  |        0.38 |        0.71 |       -0.42 |          -0 |      -0.89 |        -1.9 |
| water pressure drop minor total[pa]        |     -241.86 |     -242.61 |     -239.99 |     -240.98 |     -238.9 |     -236.46 |
| water pressure drop minor total[pa] dev[%] |        0.37 |        0.68 |       -0.41 |          -0 |      -0.86 |       -1.87 |
| water pressure drop total[pa]              |    -7186.47 |    -7210.16 |    -7128.78 |     -7159.1 |   -7095.79 |    -7022.82 |
| water pressure drop total[pa] dev[%]       |        0.38 |        0.71 |       -0.42 |          -0 |      -0.88 |        -1.9 |
| lhv [mj/kg]                                |       46.97 |       46.97 |       46.97 |       46.97 |      46.97 |       46.97 |
| firing rate [MW]                           |         4.7 |         4.7 |         4.7 |         4.7 |        4.7 |         4.7 |
| adiabatic temperature [°C]                 |      1981.5 |     2052.36 |     1854.03 |     1915.54 |    1796.53 |     1692.05 |
| adiabatic temperature [°C] dev[%]          |        3.44 |        7.14 |       -3.21 |           0 |      -6.21 |      -11.67 |
| stack temperature[°c]                      |      167.01 |       164.6 |      171.74 |      169.39 |     174.05 |      178.56 |
| stack temperature[°c] dev[%]               |        -1.4 |       -2.83 |        1.39 |           0 |       2.75 |        5.42 |
| feedwater pressure[pa]                     | 1.00719e+06 | 1.00721e+06 | 1.00713e+06 | 1.00716e+06 | 1.0071e+06 | 1.00702e+06 |
| feedwater pressure[pa] dev[%]              |           0 |        0.01 |          -0 |           0 |      -0.01 |       -0.01 |
| drum pressure[pa]                          |       1e+06 |       1e+06 |       1e+06 |       1e+06 |      1e+06 |       1e+06 |

Increasing the excess air ratio reduces the direct efficiency, the total gas side pressure drop increases as higher air flow leads to greater flue gas mass flow.

From an operational perspective, the results indicate an optimal excess air range rather than a single value. Around the control point at $\lambda \approx 1.1$, the boiler achieves a favorable balance between thermal efficiency, acceptable gas side pressure drop, and sufficient combustion stability margin. Further increases in excess air provide limited operational benefit while incurring efficiency and hydraulic penalties.

\newpage

## Influence of fuel mass flow

$$
\dot{m}_\mathrm{fuel} = [0.10, 0.075, 0.050, 0.025]\; \frac{kg}{s}
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_fuel_flow.png}
\caption{Boiler performance as a function of fuel mass flow}
\label{fig:performance_fuel_flow}
\end{figure}

At low firing rates, steam capacity increases approximately linearly with fuel input, indicating that the available heat transfer surface is sufficient to absorb the additional duty. As the firing rate approaches the nominal design value, deviations from linearity become apparent, reflecting increasing limitations in heat transfer effectiveness rather than fuel input.

Radiative heat transfer increases with fuel mass flow due to its strong dependence on flame temperature. Since radiative heat flux scales approximately with $T_\mathrm{flame}^4$ according to the Stefan Boltzmann relation, even moderate increases in flame temperature lead to a strong rise in radiative duty in the upstream sections. This effect explains the increasing dominance of the radiant section at high load.

Table: Fuel flow performance analysis.

| fuel flow [kg/s]                           |        0.02 |        0.05 |        0.08 |        0.10 |
| :----------------------------------------- | ----------: | ----------: | ----------: | ----------: |
| fuel mass flow[kg/s]                       |        0.02 |        0.05 |        0.08 |         0.1 |
| fuel mass flow[kg/s] dev[%]                |         -75 |         -50 |         -25 |           0 |
| air flow[kg/s]                             |        0.44 |        0.89 |        1.33 |        1.77 |
| air flow[kg/s] dev[%]                      |         -75 |         -50 |         -25 |           0 |
| excess air ratio[-]                        |         1.1 |         1.1 |         1.1 |         1.1 |
| excess air ratio[-] dev[%]                 |           0 |           0 |           0 |           0 |
| feedwater flow[kg/s]                       |        0.46 |        0.91 |        1.36 |         1.8 |
| feedwater flow[kg/s] dev[%]                |      -74.61 |      -49.48 |       -24.6 |           0 |
| steam capacity[t/h]                        |        1.65 |        3.27 |        4.88 |        6.48 |
| steam capacity[t/h] dev[%]                 |      -74.59 |      -49.45 |       -24.6 |           0 |
| $\eta_{\mathrm{direct}} [-]$               |        0.91 |         0.9 |         0.9 |        0.89 |
| $\eta_{\mathrm{direct}} [-]$               |        1.64 |        1.08 |        0.54 |           0 |
| $\eta_{\mathrm{indirect}} [-]$             |        0.91 |         0.9 |         0.9 |        0.89 |
| $\eta_{\mathrm{indirect}} [-]$             |        1.64 |        1.08 |        0.54 |           0 |
| conductance [MW/K]                         |           0 |        0.01 |        0.01 |        0.01 |
| conductance [MW/K] dev[%]                  |      -64.06 |      -38.77 |      -18.25 |           0 |
| input heat [MW]                            |        1.18 |        2.35 |        3.53 |         4.7 |
| input heat [MW] dev[%]                     |         -75 |         -50 |         -25 |           0 |
| useful heat [MW]                           |        1.07 |        2.12 |        3.17 |         4.2 |
| useful heat [MW] dev[%]                    |      -74.59 |      -49.46 |       -24.6 |           0 |
| pressure drop fric total[pa]               |      -22.96 |      -88.51 |     -194.04 |      -342.6 |
| pressure drop fric total[pa] dev[%]        |       -93.3 |      -74.16 |      -43.36 |          -0 |
| pressure drop minor total[pa]              |      -43.57 |     -179.44 |     -415.82 |     -760.56 |
| pressure drop minor total[pa] dev[%]       |      -94.27 |      -76.41 |      -45.33 |          -0 |
| pressure drop total[pa]                    |      -66.53 |     -267.95 |     -609.86 |    -1103.16 |
| pressure drop total[pa] dev[%]             |      -93.97 |      -75.71 |      -44.72 |          -0 |
| water pressure drop fric total[pa]         |     -572.65 |    -1974.81 |    -4106.66 |    -6918.12 |
| water pressure drop fric total[pa] dev[%]  |      -91.72 |      -71.45 |      -40.64 |          -0 |
| water pressure drop minor total[pa]        |      -15.54 |      -61.48 |     -136.98 |     -240.98 |
| water pressure drop minor total[pa] dev[%] |      -93.55 |      -74.49 |      -43.16 |          -0 |
| water pressure drop total[pa]              |     -588.19 |    -2036.29 |    -4243.64 |     -7159.1 |
| water pressure drop total[pa] dev[%]       |      -91.78 |      -71.56 |      -40.72 |          -0 |
| lhv [mj/kg]                                |       46.97 |       46.97 |       46.97 |       46.97 |
| firing rate [MW]                           |        1.17 |        2.35 |        3.52 |         4.7 |
| firing rate [MW] dev[%]                    |         -75 |         -50 |         -25 |           0 |
| adiabatic temperature [°C]                 |     1915.54 |     1915.54 |     1915.54 |     1915.54 |
| stack temperature[°c]                      |      135.16 |      146.82 |      158.25 |      169.39 |
| stack temperature[°c] dev[%]               |      -20.21 |      -13.33 |       -6.58 |           0 |
| feedwater pressure[pa]                     | 1.00059e+06 | 1.00204e+06 | 1.00424e+06 | 1.00716e+06 |
| feedwater pressure[pa] dev[%]              |       -0.65 |       -0.51 |       -0.29 |           0 |
| drum pressure[pa]                          |       1e+06 |       1e+06 |       1e+06 |       1e+06 |

As the fuel mass flow increases, the steam generation capacity rises, the direct efficiency decreases slightly, and the stack temperature increases, indicating reduced effectiveness of heat recovery at higher firing rates.

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

| drum pressure [bar]                        |       10.00 |     16.00 |     4.00 |
| :----------------------------------------- | ----------: | --------: | -------: |
| fuel mass flow[kg/s]                       |         0.1 |       0.1 |      0.1 |
| air flow[kg/s]                             |        1.77 |      1.77 |     1.77 |
| excess air ratio[-]                        |         1.1 |       1.1 |      1.1 |
| feedwater flow[kg/s]                       |         1.8 |      1.78 |     1.84 |
| feedwater flow[kg/s] dev[%]                |           0 |     -1.15 |     2.55 |
| steam capacity[t/h]                        |        6.48 |       6.4 |     6.64 |
| steam capacity[t/h] dev[%]                 |           0 |     -1.16 |     2.54 |
| $\eta_{\mathrm{direct}} [-]$               |        0.89 |      0.89 |      0.9 |
| $\eta_{\mathrm{direct}} [-]$               |           0 |     -0.49 |     0.83 |
| $\eta_{\mathrm{indirect}} [-]$             |        0.89 |      0.89 |      0.9 |
| $\eta_{\mathrm{indirect}} [-]$             |           0 |     -0.49 |     0.83 |
| conductance [MW/K]                         |        0.01 |      0.01 |     0.01 |
| conductance [MW/K] dev[%]                  |           0 |      1.73 |    -2.61 |
| input heat [MW]                            |         4.7 |       4.7 |      4.7 |
| useful heat [MW]                           |         4.2 |      4.18 |     4.24 |
| useful heat [MW] dev[%]                    |           0 |     -0.49 |     0.83 |
| pressure drop fric total[pa]               |      -342.6 |   -353.29 |  -324.65 |
| pressure drop fric total[pa] dev[%]        |          -0 |      3.12 |    -5.24 |
| pressure drop minor total[pa]              |     -760.56 |   -781.92 |   -724.6 |
| pressure drop minor total[pa] dev[%]       |          -0 |      2.81 |    -4.73 |
| pressure drop total[pa]                    |    -1103.16 |  -1135.22 | -1049.24 |
| pressure drop total[pa] dev[%]             |          -0 |      2.91 |    -4.89 |
| water pressure drop fric total[pa]         |    -6918.12 |  -6766.22 | -7257.95 |
| water pressure drop fric total[pa] dev[%]  |          -0 |      -2.2 |     4.91 |
| water pressure drop minor total[pa]        |     -240.98 |   -235.71 |  -252.98 |
| water pressure drop minor total[pa] dev[%] |          -0 |     -2.19 |     4.98 |
| water pressure drop total[pa]              |     -7159.1 |  -7001.93 | -7510.92 |
| water pressure drop total[pa] dev[%]       |          -0 |      -2.2 |     4.91 |
| lhv [mj/kg]                                |       46.97 |     46.97 |    46.97 |
| firing rate [MW]                           |         4.7 |       4.7 |      4.7 |
| firing rate [MW] dev[%]                    |           0 |         0 |        0 |
| adiabatic temperature [°C]                 |     1915.54 |   1915.54 |  1915.54 |
| stack temperature[°c]                      |      169.39 |    179.55 |   152.15 |
| stack temperature[°c] dev[%]               |           0 |         6 |   -10.18 |
| feedwater pressure[pa]                     | 1.00716e+06 | 1.607e+06 |   407511 |
| feedwater pressure[pa] dev[%]              |           0 |     59.56 |   -59.54 |
| drum pressure[pa]                          |       1e+06 |   1.6e+06 |   400000 |
| drum pressure[pa] dev[%]                   |           0 |        60 |      -60 |

Increasing the drum pressure, raises the steam capacity because the latent heat of vaporization decreases with increasing pressure, allowing a larger steam mass flow to be generated for the same absorbed thermal duty. The direct efficiency decreases, since higher water and steam temperatures reduce the available driving temperature difference on the gas side. Consistent with this, the stack temperature increases, indicating a diminished potential for further heat recovery.

## Stage wise heat transfer and hydraulics

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
