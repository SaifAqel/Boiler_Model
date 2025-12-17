# Summary

This thesis presented a physics based modelling framework for a three pass fire tube industrial shell boiler, integrating combustion, heat transfer, and hydraulic behavior within a single tool. The model was implemented in Python and structured around a one dimensional marching solver that resolves gas side and water/steam side processes consistently along the boiler flow path.

The developed framework couples three main sub models:

- A detailed fuel air combustion model.

- Heat transfer is resolved across six sequential gas side stages, representing the furnace, reversal chambers, convective tube banks, and economizer.

- Gas side pressure losses are computed concurrently with heat transfer, Water side pressure losses are evaluated for the economizer circuit.

The performance analysis shows boiler efficiency most sensitive to excess air, firing rate governs absolute duty and steam capacity, pressure mainly affects steam quantity rather than thermal efficiency.

\newpage

\appendix
