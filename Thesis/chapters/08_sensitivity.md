# Boiler performance analysis

The present chapter evaluates the thermal and hydraulic performance of the water tube boiler model based on steady state simulations of a reference control case and systematic parameter variations. The analysis is structured to introduce the control case first and then to discuss the influence of excess air factor, fuel mass flow, and drum pressure, followed by a stage wise interpretation of heat transfer and gas side hydraulics. Throughout the chapter, boiler efficiency is considered both in terms of direct efficiency

$$
\eta_{\mathrm{direct}} = \frac{Q_{\mathrm{useful}}}{\dot{m}_{\mathrm{fuel}} \, \mathrm{LHV}}
$$

and indirect efficiency based on loss terms.

## Control case performance

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/hx/default_case_hx_approach.png}
\caption{Thermal and hydraulic performance indicators for the control case operating point}
\label{fig:performance_control_case}
\end{figure}

The control case corresponds to operation near$\lambda \approx 1.1$,$\dot{m}_{\mathrm{fuel}} \approx 0.1 \ \mathrm{kg \ s^{-1}}$, and$p_{\mathrm{drum}} \approx 10 \ \mathrm{bar}$. At this point the boiler delivers the nominal steam flow and serves as the reference state for all relative comparisons in this chapter. The figure summarises the principal key performance indicators$Q_{\mathrm{in}}$,$Q_{\mathrm{useful}}$,$\eta_{\mathrm{direct}}$,$T_{\mathrm{ad}}$, and$T_{\mathrm{stack}}$, as well as the distribution of$Q_{\mathrm{stage}}$and$UA$across heat exchangers HX1 to HX6. Subsequent sections refer back to these values when quantifying the impact of parameter variations.

## Global boiler performance across parameter groups

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/kpi_overview_all_param_groups.png}
\caption{Overview of key boiler performance indicators for all parameter groups}
\label{fig:kpi_overview_all_param_groups}
\end{figure}

The overview plot consolidates the direct and indirect efficiencies, total heat input$Q_{\mathrm{in}}$, useful heat$Q_{\mathrm{useful}}$, and stack temperature for all simulated operating points. The data are grouped by excess air factor variation, fuel mass flow variation, and drum pressure variation. This figure provides a compact summary of how the different parameter groups shift the global performance relative to the control case introduced above. In the remainder of the chapter, each parameter group is analysed separately, but the trends are always interpreted in the context of the global behavior shown here.

## Influence of excess air factor

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_excess_air.png}
\caption{Boiler performance as a function of excess air factor}
\label{fig:performance_excess_air}
\end{figure}

The variation of excess air factor$\lambda$at fixed fuel mass flow and drum pressure modifies the adiabatic flame temperature$T_{\mathrm{ad}}$, the radiative heat transfer in HX1, and the convective heat transfer in the subsequent tube banks. The figure shows the resulting trends in$\eta_{\mathrm{direct}}$,$Q_{\mathrm{useful}}$,$T_{\mathrm{stack}}$, and the main loss terms over the simulated range of$\lambda$. Decreasing$\lambda$towards stoichiometric conditions increases$T_{\mathrm{ad}}$and the fraction of duty absorbed in the radiant section, while increasing$\lambda$leads to higher stack losses due to additional sensible heat in the flue gas. The numerical values extracted from this plot are used later to identify the recommended band of$\lambda$for efficient and robust operation.

## Influence of fuel mass flow

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_fuel_flow.png}
\caption{Boiler performance as a function of fuel mass flow}
\label{fig:performance_fuel_flow}
\end{figure}

The fuel mass flow sweep at fixed$\lambda$and$p_{\mathrm{drum}}$explores part load and overload operation between approximately$25\%$and$100\%$of nominal firing rate. The figure presents the corresponding change in$Q_{\mathrm{in}}$,$Q_{\mathrm{useful}}$, and boiler efficiencies along with the evolution of$T_{\mathrm{stack}}$and steam production$\dot{m}_{\mathrm{steam}}$. As the load increases, the higher gas mass flow and gas side Reynolds numbers enhance convective heat transfer, particularly in HX3 and HX5, while also increasing gas side pressure drops and velocities. The quantitative trends in this figure support the later discussion of how duty is redistributed between the radiant section, convective tube banks, and economiser when the boiler is operated away from the control case firing rate.

## Influence of drum pressure

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/performance_water_pressure.png}
\caption{Boiler performance as a function of drum pressure}
\label{fig:performance_water_pressure}
\end{figure}

The drum pressure variation modifies the steam saturation temperature and thus the driving temperature difference between flue gas and water or steam on each heat exchanger surface. The figure illustrates how increasing$p_{\mathrm{drum}}$raises the saturation temperature and the corresponding mean water side temperature, which reduces the logarithmic mean temperature difference and shifts the distribution of$Q_{\mathrm{stage}}$. The net effect on$\eta_{\mathrm{direct}}$and$T_{\mathrm{stack}}$depends on the balance between reduced driving temperature difference and the improved thermodynamic quality of the steam. These trends are quantified in the numerical analysis and are used to identify suitable operating pressures given constraints on efficiency and required steam conditions.

## Stage wise heat transfer behaviour

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/stages_param_groups.png}
\caption{Stage wise heat exchanger duty, conductance, outlet temperature, and pressure drop for all parameter groups}
\label{fig:stages_param_groups}
\end{figure}

The stage wise plot presents$Q_{\mathrm{stage}}$,$UA$, gas outlet temperature, and stage pressure drop$\Delta p$for HX1 to HX6 across all parameter groups. This figure links global performance changes to local heat transfer behaviour. Variations in$\lambda$primarily affect$Q_{\mathrm{stage}}$and$UA$in the radiant section and the first convective bank, while load changes affect both the magnitude and the distribution of duty along the gas path. The drum pressure variation, by modifying water side temperatures, alters the effective$UA$utilisation in each stage. The numerical values extracted from this plot are used to identify which heat exchangers limit boiler performance under different operating conditions.

## Gas side hydraulics and heat transfer decomposition

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{results/plots/per_run/stages_velocity_pressure_Qsum_UA.png}
\caption{Stage wise gas velocity, gas pressure, heat transfer decomposition, and conductance}
\label{fig:stages_velocity_pressure_Qsum_UA}
\end{figure}

The final figure resolves gas side velocity, absolute gas pressure, and the decomposition of$Q_{\mathrm{stage}}$into radiative and convective contributions, along with the corresponding stage conductance values. The figure clarifies how changes in fuel mass flow and excess air factor translate into different velocity and pressure profiles and how this in turn influences heat transfer modes in each heat exchanger. The presented data enable a consistent interpretation of how hydraulic margins evolve with operating point and how close individual stages approach practical constraints such as allowable gas velocity or pressure drop. In combination with the previous plots, this information supports the identification of an operating window that balances efficiency, steam conditions, and hydraulic safety.
