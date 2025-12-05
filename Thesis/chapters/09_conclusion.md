# Conclusion

This thesis developed and validated a coupled combustion–heat-transfer–hydraulics model for a three-pass fire-tube industrial shell boiler. The framework integrates detailed fuel–air combustion using Cantera, multi-stage radiative and convective heat-transfer modelling across six sequential heat-exchange sections, and a resistance-based hydraulic model for gas-side pressure losses. The approach captures the dominant physical mechanisms governing boiler performance while remaining computationally tractable for iterative operating-point calculations and sensitivity studies.

The modelling framework successfully reproduces the expected qualitative behaviour of industrial shell boilers:

- The adiabatic flame temperature $T_\mathrm{ad}$ is predicted from full HP-equilibrium chemistry, providing a physically consistent upper-bound reference state for the flue gas.
- Radiative transfer in the furnace (HX$_1$) dominates high-temperature heat exchange, while the downstream tube banks (HX$_3$ and HX$_5$) provide the bulk of convective duty.
- The economiser (HX$_6$) is correctly characterised as a single-phase internal flow exchanger, with performance governed largely by gas-side convection.

At the boiler scale, the simulation produces converged operating conditions by solving a fixed-point iteration linking efficiency, combustion heat input, and steam mass flow. This procedure captures the inherent coupling between water/steam generation and flue-gas cooling, ensuring global energy consistency.

The sensitivity studies demonstrate three principal findings:

1. **Excess air ratio $\lambda$.**  
   Efficiency exhibits a shallow optimum close to the design value. Increasing $\lambda$ beyond this point lowers furnace temperatures, reduces radiative heat transfer, increases stack losses, and raises overall gas-side pressure drop. The model quantifies these effects and highlights the operational importance of controlling excess air.

2. **Drum/feedwater pressure.**  
   Pressure mainly influences _steam quantity_ rather than _efficiency_. Higher pressures increase saturation temperature and reduce latent heat, leading to lower steam mass flow for the same heat input. The indirect efficiency varies only mildly across the investigated pressure range.

3. **Firing rate (fuel mass flow).**  
   Useful duty and steam flow scale nearly linearly with firing rate over a broad operating window. Efficiency remains relatively stable at mid-loads, with penalties at both low and high firing rates due to deteriorated heat-transfer coefficients and increased stack temperatures. Gas-side pressure drop increases strongly with load, reflecting the quadratic dependence on velocity.

Overall, the model provides a physics-based, modular, and extensible framework suitable for performance assessment, operational optimisation, and early-stage design exploration of industrial shell boilers. It enables quantitative evaluation of how geometry, combustion conditions, and operating parameters influence heat-transfer distribution, steam capacity, efficiency, and hydraulic behaviour.

Future work could extend the present model by incorporating:

- transient operation and burner cycling,
- advanced radiation models (spectral or WSGG-based),
- two-phase water/steam circulation modelling within the pressure parts,
- fouling, slagging, and degradation effects over time,
- NO$_x$ formation and emissions modelling coupled to flame-temperature predictions.

Such extensions would further enhance the model’s fidelity and applicability across a wider range of industrial boiler configurations and operating regimes.

\newpage
