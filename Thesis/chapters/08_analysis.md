# Performance Analysis

## Purpose, parameters, and methodology

The purpose of this chapter is to evaluate the thermal and hydraulic performance of the developed fire tube shell boiler model under representative operating conditions and systematic parameter variations. The analysis aims to quantify how key controllable and design relevant parameters influence boiler efficiency, steam production, heat transfer distribution, and pressure losses.

### Investigated parameters and ranges

The following parameters are selected for investigation based on their practical importance in industrial boiler operation:

- **Excess air ratio $\lambda$**

  Controls combustion completeness, flue gas mass flow, adiabatic flame temperature, and stack losses.

  $$
  \lambda = [1.00,\;1.05,\;1.10,\;1.15,\;1.20,\;1.30]
  $$

- **Fuel mass flow rate $\dot m_\mathrm{fuel}$**

  Governs firing rate, heat input, and steam generation capacity.

  $$
  \dot m_\mathrm{fuel} = [0.025,\;0.050,\;0.075,\;0.10,\;0.125]\;\mathrm{kg\,s^{-1}}
  $$

- **Drum pressure $P_\mathrm{drum}$**

  Influences saturation temperature, latent heat of vaporization, and available driving temperature difference.

  $$
  P_\mathrm{drum} = [4,\;10,\;16]\;\mathrm{bar}
  $$

- **Fouling factor $f$**

  Represents degradation of effective heat transfer surfaces due to deposits on gas-side and water-side walls.

  $$
  f = [0.5,\;1.0,\;2.0,\;5.0,\;10.0]
  $$

These ranges span typical industrial operating conditions and extend into off-design regimes to reveal performance limits and sensitivities.

### Control case definition

A single reference operating point is defined as the **control case**, against which all parameter variations are compared. The control case represents nominal boiler operation:

- Fuel mass flow: $\dot m_\mathrm{fuel} = 0.1\ \mathrm{kg\,s^{-1}}$
- Excess air ratio: $\lambda = 1.1$
- Drum pressure: $P_\mathrm{drum} = 10\ \mathrm{bar}$

All parameters not under investigation are held fixed at their control values during each parametric sweep.

### Methodology of analysis

For each operating condition, the coupled combustion–heat transfer–hydraulic solver is executed until convergence of water/steam mass flow and boiler efficiency. The following quantities are extracted and analyzed:

- Direct and indirect boiler efficiencies
- Steam production rate
- Stack temperature
- Stage-wise heat duties and conductance
- Gas-side and water-side pressure drops

Results are analyzed both at the **global boiler level** and at the **individual stage level** to distinguish overall performance trends from local heat transfer and hydraulic effects.

## Results and parametric analysis

### Control Case Performance

The control case is defined by a fuel mass flow of $\dot m_\mathrm{fuel}=0.1\ \mathrm{kg\,s^{-1}}$, an excess air ratio of $\lambda=1.1$, and a drum pressure of $P_\mathrm{drum}=10\ \mathrm{bar}$. These values represent the nominal operating point of the boiler and are used as the reference state throughout this chapter.

Table: Control case performance.

| control                              | control |
| :----------------------------------- | ------: |
| Fuel Mass Flow[Kg/S]                 |     0.1 |
| Air Flow[Kg/S]                       |    1.69 |
| Excess Air Ratio[-]                  |    1.05 |
| Feedwater Flow[Kg/S]                 |    1.89 |
| Steam Capacity[T/H]                  |    6.81 |
| $\eta_{\mathrm{direct}}$ [-]         |    0.95 |
| $\eta_{\mathrm{indirect}}$ [-]       |    0.95 |
| Stack Loss Fraction[-]               |    0.05 |
| Q_Flue_Out[Mw]                       |    0.25 |
| conductance [MW/K]                   |    0.01 |
| input heat [MW]                      |    4.68 |
| useful heat [MW]                     |    4.42 |
| Q_Balance_Error[Mw]                  |      -0 |
| Pressure Drop Fric Total[Kpa]        |   -8.35 |
| Pressure Drop Minor Total[Kpa]       |   -4.09 |
| Pressure Drop Total[Kpa]             |  -12.45 |
| Water Pressure Drop Fric Total[Kpa]  |   -0.06 |
| Water Pressure Drop Minor Total[Kpa] |      -0 |
| Water Pressure Drop Total[Kpa]       |   -0.06 |
| Lhv [Mj/Kg]                          |   46.73 |
| firing rate [MW]                     |    4.67 |
| adiabatic temperature [°C]           |  1981.5 |
| Stack Temperature[°C]                |  152.38 |
| Feedwater Pressure[Kpa]              | 1000.06 |
| Drum Pressure[Kpa]                   |    1000 |

### Stage-wise heat transfer and hydraulics

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/stages_control_combined_8plots.png}
\caption{Stage wise heat transfer and hydraulic profiles}
\label{fig:stages_param_groups}
\end{figure}

Across all runs the stage pattern stays the same: gas temperature drops from HX 1 to HX 6, stage heat duty is highest in the first stages and decreases downstream, and early stages are driven mainly by radiative transfer while later stages are relatively more convective. Control cases sit between the minimum and maximum parameter cases, showing smooth scaling rather than any stage wise regime change.

Excess air mainly shifts and weakens heat transfer: higher excess air lowers upstream gas temperatures and reduces early stage duties, pushes a larger share of recovery downstream, and increases gas velocity and total pressure drop across stages. Fuel flow scales everything up or down: higher fuel flow increases gas temperatures, stage duties, and both convective and radiative contributions in all stages, with the biggest absolute changes in the first tube bank section and upstream units, while also increasing pressure drop. Drum pressure has a smaller gas side impact but adjusts downstream recovery through water side conditions, slightly shifting late stage duties and conductance without changing the overall stage wise shape.

Table: Control case stages summary.

| stage KPI                      | HX_1    | HX_2     | HX_3      | HX_4     | HX_5      | HX_6       |
| :----------------------------- | :------ | :------- | :-------- | :------- | :-------- | :--------- |
| Kind                           | Furnace | reversal | tube_bank | reversal | tube_bank | economizer |
| Gas In Pressure[Kpa]           | 101.33  | 101.32   | 101.32    | 101.27   | 101.27    | 101.23     |
| Gas In Temp[°C]                | 1981.25 | 860.87   | 804.14    | 332.78   | 328.16    | 220.51     |
| Gas In Enthalpy[Kj/Kg]         | 2612.29 | 1014.02  | 938.90    | 349.39   | 343.96    | 219.06     |
| Gas Out Pressure[Kpa]          | 101.32  | 101.32   | 101.27    | 101.27   | 101.23    | 88.88      |
| Gas Out Temp[°C]               | 860.87  | 804.14   | 332.78    | 328.16   | 220.51    | 152.38     |
| Gas Out Enthalpy[Kj/Kg]        | 1014.02 | 938.90   | 349.39    | 343.96   | 219.06    | 141.69     |
| Water In Temp[°C]              | 179.89  | 179.89   | 179.89    | 179.89   | 179.89    | 104.80     |
| Water In Enthalpy[Kj/Kg]       | 762.68  | 762.68   | 762.68    | 762.68   | 762.68    | 440.00     |
| Water In Pressure[Kpa]         | 1000.00 | 1000.00  | 1000.00   | 1000.00  | 1000.00   | 1000.06    |
| Water Out Temp[°C]             | 179.89  | 179.89   | 179.89    | 179.89   | 179.89    | 122.09     |
| Water Out Enthalpy[Kj/Kg]      | 762.68  | 762.68   | 762.68    | 762.68   | 762.68    | 513.21     |
| Water Out Pressure[Kpa]        | 1000.00 | 1000.00  | 1000.00   | 1000.00  | 1000.00   | 1000.00    |
| Gas Avg Velocity[M/S]          | 5.04    | 2.90     | 7.67      | 1.58     | 6.24      | 47.04      |
| Water Avg Velocity[M/S]        |         |          |           |          |           | 0.03       |
| Pressure Drop Fric[Kpa]        | -0.00   | -0.00    | -0.03     | -0.00    | -0.03     | -8.30      |
| Pressure Drop Minor[Kpa]       | -0.00   | -0.00    | -0.02     | -0.00    | -0.02     | -4.05      |
| Pressure Drop Total[Kpa]       | -0.00   | -0.00    | -0.05     | -0.00    | -0.05     | -12.35     |
| Water Pressure Drop Fric[Kpa]  |         |          |           |          |           | -0.06      |
| Water Pressure Drop Minor[Kpa] |         |          |           |          |           | -0.00      |
| Water Pressure Drop Total[Kpa] |         |          |           |          |           | -0.06      |
| Q Conv[Mw]                     | 0.11    | 0.01     | 0.84      | 0.00     | 0.21      | 0.14       |
| Q Rad[Mw]                      | 2.75    | 0.13     | 0.21      | 0.01     | 0.02      | 0.00       |
| Q Total[Mw]                    | 2.86    | 0.13     | 1.06      | 0.01     | 0.22      | 0.14       |
| conductance [MW/K]             | 0.00    | 0.00     | 0.00      | 0.00     | 0.00      | 0.00       |
| Steam Capacity[T/H]            | 4.55    | 0.21     | 1.68      | 0.02     | 0.36      |            |

### Influence of excess air factor

$$
\lambda = [1.00, 1.05, 1.10, 1.15, 1.20, 1.30]\; [-]
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_excess_air.png}
\caption{Boiler performance as a function of excess air factor}
\label{fig:performance_excess_air}
\end{figure}

Increasing the excess air ratio increases flue-gas mass flow and sensible stack losses. As a result, boiler efficiency exhibits a shallow maximum near the control value $\lambda = 1.1$, beyond which additional air primarily raises stack temperature and pressure losses without improving useful heat transfer.

Table: Excess air performance analysis.

| excess air [-]                       |    1.00 |    1.05 |    1.10 |    1.15 |    1.20 |    1.30 |
| :----------------------------------- | ------: | ------: | ------: | ------: | ------: | ------: |
| Fuel Mass Flow[Kg/S]                 |     0.1 |     0.1 |     0.1 |     0.1 |     0.1 |     0.1 |
| Air Flow[Kg/S]                       |    1.61 |    1.69 |    1.77 |    1.85 |    1.93 |    2.09 |
| Excess Air Ratio[-]                  |       1 |    1.05 |     1.1 |    1.15 |     1.2 |     1.3 |
| Feedwater Flow[Kg/S]                 |     1.9 |    1.89 |    1.89 |    1.88 |    1.87 |    1.86 |
| Steam Capacity[T/H]                  |    6.84 |    6.81 |    6.79 |    6.77 |    6.74 |    6.69 |
| $\eta_{\mathrm{direct}}$ [-]         |    0.95 |    0.95 |    0.94 |    0.94 |    0.94 |    0.93 |
| $\eta_{\mathrm{indirect}}$ [-]       |    0.95 |    0.95 |    0.94 |    0.94 |    0.94 |    0.93 |
| Stack Loss Fraction[-]               |    0.05 |    0.05 |    0.06 |    0.06 |    0.06 |    0.07 |
| Q_Flue_Out[Mw]                       |    0.24 |    0.25 |    0.27 |    0.28 |     0.3 |    0.33 |
| conductance [MW/K]                   |    0.01 |    0.01 |    0.01 |    0.01 |    0.01 |    0.01 |
| input heat [MW]                      |    4.68 |    4.68 |    4.68 |    4.68 |    4.68 |    4.68 |
| useful heat [MW]                     |    4.44 |    4.42 |    4.41 |    4.39 |    4.38 |    4.35 |
| Q_Balance_Error[Mw]                  |      -0 |      -0 |      -0 |      -0 |      -0 |      -0 |
| Pressure Drop Fric Total[Kpa]        |   -7.58 |   -8.35 |   -9.17 |  -10.05 |  -10.97 |  -12.97 |
| Pressure Drop Minor Total[Kpa]       |    -3.7 |   -4.09 |   -4.51 |   -4.96 |   -5.44 |   -6.48 |
| Pressure Drop Total[Kpa]             |  -11.28 |  -12.45 |  -13.69 |  -15.01 |   -16.4 |  -19.46 |
| Water Pressure Drop Fric Total[Kpa]  |   -0.06 |   -0.06 |   -0.06 |   -0.06 |   -0.06 |   -0.05 |
| Water Pressure Drop Minor Total[Kpa] |      -0 |      -0 |      -0 |      -0 |      -0 |      -0 |
| Water Pressure Drop Total[Kpa]       |   -0.06 |   -0.06 |   -0.06 |   -0.06 |   -0.06 |   -0.06 |
| Lhv [Mj/Kg]                          |   46.73 |   46.73 |   46.73 |   46.73 |   46.73 |   46.73 |
| firing rate [MW]                     |    4.67 |    4.67 |    4.67 |    4.67 |    4.67 |    4.67 |
| adiabatic temperature [°C]           | 2052.36 |  1981.5 | 1915.54 | 1854.03 | 1796.53 | 1692.05 |
| Stack Temperature[°C]                |  150.16 |  152.38 |  154.59 |  156.79 |  158.95 |  163.16 |
| Feedwater Pressure[Kpa]              | 1000.06 | 1000.06 | 1000.06 | 1000.06 | 1000.06 | 1000.06 |
| Drum Pressure[Kpa]                   |    1000 |    1000 |    1000 |    1000 |    1000 |    1000 |

Increasing the excess air ratio increases the total gas side pressure drop as higher air flow leads to greater flue gas mass flow.

\newpage

### Influence of fuel mass flow

$$
\dot{m}_\mathrm{fuel} = [0.025, 0.050, 0.075, 0.10, 0.125]\; \frac{kg}{s}
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_fuel_flow.png}
\caption{Boiler performance as a function of fuel mass flow}
\label{fig:performance_fuel_flow}
\end{figure}

Steam capacity increases approximately linearly with fuel input, indicating that the available heat transfer surface is sufficient to absorb the additional duty. As the firing rate approaches the nominal design value, deviations from linearity become apparent, reflecting increasing limitations in heat transfer effectiveness rather than fuel input.

Table: Fuel flow performance analysis.

| fuel flow [kg/s]                     |    0.02 |    0.05 |    0.08 |    0.10 |    0.12 |
| :----------------------------------- | ------: | ------: | ------: | ------: | ------: |
| Fuel Mass Flow[Kg/S]                 |    0.02 |    0.05 |    0.08 |     0.1 |    0.12 |
| Air Flow[Kg/S]                       |    0.42 |    0.85 |    1.27 |    1.69 |    2.11 |
| Excess Air Ratio[-]                  |    1.05 |    1.05 |    1.05 |    1.05 |    1.05 |
| Feedwater Flow[Kg/S]                 |    0.48 |    0.95 |    1.43 |    1.89 |    2.35 |
| Steam Capacity[T/H]                  |    1.72 |    3.44 |    5.13 |    6.81 |    8.48 |
| $\eta_{\mathrm{direct}}$ [-]         |    0.96 |    0.95 |    0.95 |    0.95 |    0.94 |
| $\eta_{\mathrm{indirect}}$ [-]       |    0.96 |    0.95 |    0.95 |    0.95 |    0.94 |
| Stack Loss Fraction[-]               |    0.04 |    0.05 |    0.05 |    0.05 |    0.06 |
| Q_Flue_Out[Mw]                       |    0.05 |    0.11 |    0.17 |    0.25 |    0.34 |
| conductance [MW/K]                   |       0 |    0.01 |    0.01 |    0.01 |    0.01 |
| input heat [MW]                      |    1.17 |    2.34 |    3.51 |    4.68 |    5.85 |
| useful heat [MW]                     |    1.12 |    2.23 |    3.33 |    4.42 |     5.5 |
| Q_Balance_Error[Mw]                  |      -0 |      -0 |      -0 |      -0 |      -0 |
| Pressure Drop Fric Total[Kpa]        |   -0.54 |   -2.02 |   -4.57 |   -8.35 |  -13.65 |
| Pressure Drop Minor Total[Kpa]       |   -0.23 |   -0.93 |   -2.18 |   -4.09 |   -6.84 |
| Pressure Drop Total[Kpa]             |   -0.77 |   -2.95 |   -6.75 |  -12.45 |  -20.49 |
| Water Pressure Drop Fric Total[Kpa]  |   -0.01 |   -0.02 |   -0.03 |   -0.06 |   -0.11 |
| Water Pressure Drop Minor Total[Kpa] |      -0 |      -0 |      -0 |      -0 |      -0 |
| Water Pressure Drop Total[Kpa]       |   -0.01 |   -0.02 |   -0.03 |   -0.06 |   -0.11 |
| Lhv [Mj/Kg]                          |   46.73 |   46.73 |   46.73 |   46.73 |   46.73 |
| firing rate [MW]                     |    1.17 |    2.34 |     3.5 |    4.67 |    5.84 |
| adiabatic temperature [°C]           |  1981.5 |  1981.5 |  1981.5 |  1981.5 |  1981.5 |
| Stack Temperature[°C]                |  127.53 |  132.36 |  142.11 |  152.38 |  162.54 |
| Feedwater Pressure[Kpa]              | 1000.01 | 1000.02 | 1000.03 | 1000.06 | 1000.11 |
| Drum Pressure[Kpa]                   |    1000 |    1000 |    1000 |    1000 |    1000 |

\newpage

### Influence of drum pressure

$$
P_\mathrm{Drum} = [4.0, 10.0, 16.0]\; \mathrm{bar}
$$

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_drum_pressure.png}
\caption{Boiler performance as a function of drum pressure}
\label{fig:performance_water_pressure}
\end{figure}

The drum pressure variation modifies the steam saturation temperature and thus the driving temperature difference between flue gas and water/steam on each heat exchanger surface.

Table: Drum pressure performance analysis. {#tbl:drum_pressure_performance}

| drum pressure [bar]                  |   4.00 |   10.00 |   16.00 |
| :----------------------------------- | -----: | ------: | ------: |
| Fuel Mass Flow[Kg/S]                 |    0.1 |     0.1 |     0.1 |
| Air Flow[Kg/S]                       |   1.69 |    1.69 |    1.69 |
| Excess Air Ratio[-]                  |   1.05 |    1.05 |    1.05 |
| Feedwater Flow[Kg/S]                 |   1.94 |    1.89 |    1.87 |
| Steam Capacity[T/H]                  |   6.97 |    6.81 |    6.74 |
| $\eta_{\mathrm{direct}}$ [-]         |   0.95 |    0.95 |    0.94 |
| $\eta_{\mathrm{indirect}}$ [-]       |   0.95 |    0.95 |    0.94 |
| Stack Loss Fraction[-]               |   0.05 |    0.05 |    0.06 |
| Q_Flue_Out[Mw]                       |   0.23 |    0.25 |    0.27 |
| conductance [MW/K]                   |   0.01 |    0.01 |    0.01 |
| input heat [MW]                      |   4.68 |    4.68 |    4.68 |
| useful heat [MW]                     |   4.45 |    4.42 |    4.41 |
| Q_Balance_Error[Mw]                  |     -0 |      -0 |      -0 |
| Pressure Drop Fric Total[Kpa]        |  -7.91 |   -8.35 |   -8.62 |
| Pressure Drop Minor Total[Kpa]       |   -3.9 |   -4.09 |   -4.21 |
| Pressure Drop Total[Kpa]             | -11.81 |  -12.45 |  -12.83 |
| Water Pressure Drop Fric Total[Kpa]  |  -0.06 |   -0.06 |   -0.06 |
| Water Pressure Drop Minor Total[Kpa] |     -0 |      -0 |      -0 |
| Water Pressure Drop Total[Kpa]       |  -0.06 |   -0.06 |   -0.06 |
| Lhv [Mj/Kg]                          |  46.73 |   46.73 |   46.73 |
| firing rate [MW]                     |   4.67 |    4.67 |    4.67 |
| adiabatic temperature [°C]           | 1981.5 |  1981.5 |  1981.5 |
| Stack Temperature[°C]                | 138.49 |  152.38 |  160.44 |
| Feedwater Pressure[Kpa]              | 400.06 | 1000.06 | 1600.06 |
| Drum Pressure[Kpa]                   |    400 |    1000 |    1600 |

Increasing the drum pressure, raises the steam capacity because the latent heat of vaporization decreases with increasing pressure, allowing a larger steam mass flow to be generated for the same absorbed thermal duty. The direct efficiency decreases, since higher water and steam temperatures reduce the available driving temperature difference on the gas side. Consistent with this, the stack temperature increases, indicating a diminished potential for further heat recovery.

\newpage

### Influence of fouling

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

| fouling [-]                          |    1.00 |    5.00 |   10.00 |
| :----------------------------------- | ------: | ------: | ------: |
| Fuel Mass Flow[Kg/S]                 |     0.1 |     0.1 |     0.1 |
| Air Flow[Kg/S]                       |    1.69 |    1.69 |    1.69 |
| Excess Air Ratio[-]                  |    1.05 |    1.05 |    1.05 |
| Feedwater Flow[Kg/S]                 |    1.89 |    1.89 |    1.88 |
| Steam Capacity[T/H]                  |    6.81 |     6.8 |    6.78 |
| $\eta_{\mathrm{direct}}$ [-]         |    0.95 |    0.94 |    0.94 |
| $\eta_{\mathrm{indirect}}$ [-]       |    0.95 |    0.94 |    0.94 |
| Stack Loss Fraction[-]               |    0.05 |    0.06 |    0.06 |
| Q_Flue_Out[Mw]                       |    0.25 |    0.26 |    0.28 |
| conductance [MW/K]                   |    0.01 |    0.01 |    0.01 |
| input heat [MW]                      |    4.68 |    4.68 |    4.68 |
| useful heat [MW]                     |    4.42 |    4.41 |     4.4 |
| Q_Balance_Error[Mw]                  |      -0 |      -0 |      -0 |
| Pressure Drop Fric Total[Kpa]        |   -8.35 |   -8.51 |   -8.77 |
| Pressure Drop Minor Total[Kpa]       |   -4.09 |   -4.17 |   -4.29 |
| Pressure Drop Total[Kpa]             |  -12.45 |  -12.68 |  -13.06 |
| Water Pressure Drop Fric Total[Kpa]  |   -0.06 |   -0.06 |   -0.06 |
| Water Pressure Drop Minor Total[Kpa] |      -0 |      -0 |      -0 |
| Water Pressure Drop Total[Kpa]       |   -0.06 |   -0.06 |   -0.06 |
| Lhv [Mj/Kg]                          |   46.73 |   46.73 |   46.73 |
| firing rate [MW]                     |    4.67 |    4.67 |    4.67 |
| adiabatic temperature [°C]           |  1981.5 |  1981.5 |  1981.5 |
| Stack Temperature[°C]                |  152.38 |  157.04 |  164.53 |
| Feedwater Pressure[Kpa]              | 1000.06 | 1000.06 | 1000.06 |
| Drum Pressure[Kpa]                   |    1000 |    1000 |    1000 |

While the boiler can continue to operate under fouled conditions, the results highlight the importance of maintaining clean heat transfer surfaces to ensure higher efficiency.

## Conclusions from performance analysis

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/kpi_overview_all_param_groups.png}
\caption{Overview of key boiler performance indicators for all parameter groups}
\label{fig:kpi_overview_all_param_groups}
\end{figure}

Overall, the results show that fuel flow is the dominant factor affecting boiler performance. Increasing fuel flow strongly increases heat input, steam production, stack temperature, pressure drop, and leads to a noticeable reduction in direct efficiency at higher values. In contrast, changes in excess air, drum pressure, and fouling mainly cause smaller, secondary shifts, primarily influencing stack temperature and efficiency, but leave most other boiler variables relatively unchanged.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/scatter_efficiency_vs_stack_temperature_all_runs.png}
\caption{Scatter diagram showing stack temperature and direct efficiency}
\label{fig:scatter_stack_eta}
\end{figure}

The parametric analysis demonstrates that the developed boiler model captures physically consistent trends across a wide range of operating conditions.

The excess air ratio is identified as the most influential parameter affecting boiler efficiency, primarily through its control of flue-gas mass flow, adiabatic flame temperature, and stack losses. An efficiency optimum is observed near the nominal excess air setting, consistent with industrial practice.

Fuel mass flow primarily scales the thermal duty and steam production rate, with efficiency remaining nearly constant over the investigated range. This indicates that, within practical limits, the available heat transfer surface is sufficient to accommodate load variations without significant degradation in performance.

Drum pressure mainly influences steam generation through changes in latent heat and saturation temperature, while its effect on overall efficiency is secondary. Higher pressures reduce the temperature driving force for heat transfer, resulting in elevated stack temperatures.

Fouling degrades heat transfer effectiveness across all stages, with the strongest impact observed in downstream convective sections. The results highlight the importance of maintaining clean heat transfer surfaces to preserve efficiency and minimize stack losses.

Overall, the analysis confirms that the coupled combustion–heat transfer–hydraulic framework provides a robust tool for evaluating operational trade-offs and identifying efficiency-critical parameters in industrial fire tube shell boilers.

\newpage
