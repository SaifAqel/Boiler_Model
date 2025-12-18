# Summary

This thesis presented a physics based modelling framework for a three pass fire tube industrial shell boiler, integrating combustion, heat transfer, and hydraulic behavior within a single tool. The model was implemented in Python and structured around a one dimensional marching solver that resolves gas side and water/steam side processes consistently along the boiler flow path.

The developed framework couples three main sub models:

- A detailed fuel air combustion model.

- Heat transfer is resolved across six sequential gas side stages.

- Gas side pressure losses are computed concurrently with heat transfer, Water side pressure losses are evaluated for the economizer circuit.

The performance analysis demonstrates that boiler efficiency is most sensitive to the excess air ratio, which directly controls flue gas mass flow, adiabatic flame temperature, and stack losses.

The firing rate primarily governs the absolute thermal duty and steam production, with steam capacity scaling approximately linearly over the investigated operating range, indicating that the available heat transfer surface is sufficient up to near-design load. At higher firing rates, increasing gas velocities and pressure losses highlight the growing hydraulic cost of additional capacity.

Drum pressure mainly influences steam quantity through its effect on latent heat and saturation temperature, while having only a secondary impact on overall thermal efficiency; higher pressures reduce the available temperature driving force, resulting in elevated stack temperatures without proportionate gains in useful heat recovery.

Across all cases, the coupled model captures the interplay between combustion conditions, heat transfer effectiveness, and hydraulic constraints, providing a physically consistent basis for assessing operational trade offs and identifying efficiency critical control parameters in industrial fire tube boilers.

\newpage

\appendix
