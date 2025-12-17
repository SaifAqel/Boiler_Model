# Conclusion and summary

This thesis presented a physics based modelling framework for a three pass fire tube industrial shell boiler, integrating combustion, heat transfer, and hydraulic behavior within a single tool. The model was implemented in Python and structured around a one dimensional marching solver that resolves gas side and water/steam side processes consistently along the boiler flow path.

The developed framework couples three main sub models:

**Combustion model**
A detailed fuel air combustion model computes the stoichiometric requirements, excess air effects, lower and higher heating values, and the total heat release from natural gas firing. Chemical equilibrium calculations provide the adiabatic flame temperature, while a chemically frozen, fully burnt flue gas composition is used for subsequent heat transfer and hydraulic calculations.

**Heat transfer model**
Heat transfer is resolved across six sequential gas side stages, representing the furnace, reversal chambers, convective tube banks, and economizer. The model combines:

- gas side convection and radiation, wall conduction with fouling layers,
- water side pool boiling, flow boiling, and single phase convection.

A full thermal resistance network is solved locally at each marching step, updating wall temperatures, heat transfer coefficients, and linear heat flux $q'(x)$.

**Hydraulic model**
Gas side pressure losses are computed concurrently with heat transfer, using Darcy Weisbach friction for internal flow sections and a drag based bundle loss formulation for economizer crossflow. Minor losses from expansions, contractions, and bends are included. Water side pressure losses are evaluated for the economizer circuit.

The steady state simulations and sensitivity studies presented in the previous chapter lead to the following main conclusions:

**Excess air ratio**
Boiler efficiency exhibits a shallow optimum near the design excess air setting ($\lambda \approx 1.1$). At low excess air, efficiency is limited by combustion margins, while higher excess air increases flue gas mass flow and stack losses, raising the stack temperature and total gas side pressure drop. This confirms that excess air control is primarily an efficiency and hydraulics trade off rather than a strong heat transfer limitation.

**Fuel firing rate**
Steam generation scales approximately linearly with fuel mass flow over the investigated load range, indicating that the available heat transfer surface is sufficient at part load. At higher firing rates, stack temperature increases and efficiency decreases slightly, reflecting reduced effectiveness of downstream heat recovery.

**Drum pressure**
Drum pressure has a relatively minor effect on overall boiler efficiency but strongly influences steam capacity. Increasing pressure reduces the latent heat of vaporization, allowing higher steam mass flow for the same absorbed duty. Higher saturation temperatures reduce the gas water temperature driving force, leading to higher stack temperatures and marginally lower efficiencies.

Efficiency is most sensitive to excess air and stack losses, firing rate governs absolute duty and steam capacity, pressure mainly affects steam quantity rather than thermal efficiency.

The modelling framework successfully captures the coupled thermal and hydraulic behavior of an industrial shell boiler using physically interpretable sub models and standard correlations. The results are consistent with known operational trends of fire tube boilers and demonstrate that:

The developed tool provides a flexible basis for performance evaluation, operational optimization, and design exploration of shell boilers.

\newpage

\appendix
