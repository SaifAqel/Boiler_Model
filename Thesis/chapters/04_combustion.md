# Combustion Model

Determine combustion conditions inside the furnace (1st pass), resulting in a fully burnt flue gas stream, entering the heat transfer model at adiabatic temperature.

\begin{figure}[H]
\centering
\includegraphics[height=0.5\textheight, keepaspectratio]{Thesis/figures/combustion_flow.pdf}
\caption{Combustion flow}
\label{fig:combustion-flow}
\end{figure}

## Fuel and Air

### Fuel Stream

The boiler is fired with a natural-gas–type fuel defined in the simulation input (`config/fuel.yaml`).  
The fuel is supplied at $300 K$ and $1.013×10⁵ Pa$ with a mass flow rate of $0.1 kg/s$.  
Its composition is specified by user on a mass fraction.

Table: Fuel composition in mass fractions. [@ISO6976_2016]

| Component        | Formula              | Mass fraction $\mathrm{w_i}$ [-] |
| ---------------- | -------------------- | -------------------------------- |
| Methane          | $\mathrm{CH_4}$      | 0.8548                           |
| Ethane           | $\mathrm{C_2H_6}$    | 0.0622                           |
| Propane          | $\mathrm{C_3H_8}$    | 0.0207                           |
| n-Butane         | $\mathrm{C_4H_{10}}$ | 0.00518                          |
| Hydrogen sulfide | $\mathrm{H_2S}$      | 0.000104                         |
| Nitrogen         | $\mathrm{N_2}$       | 0.0414                           |
| Carbon dioxide   | $\mathrm{CO_2}$      | 0.0155                           |
| Water vapour     | $\mathrm{H_2O}$      | 0.00                             |
| Argon            | $\mathrm{Ar}$        | 0.00                             |

The mass fractions sum to 1.0 by definition. The mole fractions $\mathrm{x_i}$ are obtained from

$$
x_i = \frac{\dfrac{w_i}{M_i}}{\sum_j \dfrac{w_j}{M_j}}
$$

which is provided by the function `to_mol` in `combustion/mass_mole.py`, where $\mathrm{M_i}$ is the molar mass of species $i$ from `molar_masses` in `common/constants.py`.

### Air Stream

Combustion air is represented as a separate `GasStream` object, analogous to the fuel stream, with:

- temperature $T_\mathrm{air} = 300\ \mathrm{K}$,
- pressure $P_\mathrm{air} = 1.013\times 10^{5}\ \mathrm{Pa}$,
- mass flow rate determined internally from the specified excess air ratio $\lambda$,
- composition:

  Table: Air composition in mass fractions. [@NASA_Glenn_Air]

  | Component      | Formula         | Mass fraction $w_i$ [-] |
  | -------------- | --------------- | ----------------------- |
  | Oxygen         | $\mathrm{O_2}$  | 0.233                   |
  | Nitrogen       | $\mathrm{N_2}$  | 0.755                   |
  | Argon          | $\mathrm{Ar}$   | 0.013                   |
  | Carbon dioxide | $\mathrm{CO_2}$ | 0.00006                 |

The mass fractions satisfy $\sum_i w_i = 1$ and are converted internally to mole fractions whenever stoichiometric or thermophysical properties are required.

### Stoichiometric Oxygen requirement

Evaluated the stoichiometric oxygen requirement via `stoich_O2_required_per_mol_fuel`
in `combustion/flue.py`. The algorithm is:

1. Use per mole of species stoichiometric $\mathrm{O_2}$ factors $\nu_{\mathrm{O_{2,i}}}$ from `O2_per_mol` in `common/constants.py`:

   Table: Combustion reactions and stoichiometric factors

   | Species                                                                | Global reaction (complete combustion)                                                                     | $\nu_{\mathrm{O_2},i}$ [mol $\mathrm{O_2}$ / mol species] |
   | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
   | $\mathrm{C}$$\mathrm{H_4}$                                             | $\mathrm{C}$$\mathrm{H_4}$ + 2 $\mathrm{O_2}$ → $\mathrm{C}$$\mathrm{O_2}$ + 2 $\mathrm{H_2}$$\mathrm{O}$ | 2.0                                                       |
   | $\mathrm{C_2}$$\mathrm{H_6}$                                           | $\mathrm{C_2}$$\mathrm{H_6}$ + 3.5 $\mathrm{O_2}$ → 2 $C$$\mathrm{O_2}$ + 3 $\mathrm{H_2}$$\mathrm{O}$    | 3.5                                                       |
   | $\mathrm{C_3}$$\mathrm{H_8}$                                           | $C₃H₈$ + 5 $\mathrm{O_2}$ → 3 $\mathrm{C}$$\mathrm{O_2}$ + 4 $\mathrm{H_2}$$\mathrm{O}$                   | 5.0                                                       |
   | $\mathrm{C_4}$$\mathrm{H_{10}}$                                        | $C₄H₁₀$ + 6.5 $\mathrm{O_2}$ → 4 $\mathrm{C}$$\mathrm{O_2}$ + 5 $\mathrm{H_2}$$\mathrm{O}$                | 6.5                                                       |
   | $\mathrm{H_2}$$\mathrm{S}$                                             | $\mathrm{H_2}$$\mathrm{S}$ + 1 $\mathrm{O_2}$ → $S$$\mathrm{O_2}$ + $\mathrm{H_2}$$\mathrm{O}$            | 1.0                                                       |
   | $\mathrm{N_2}$, $\mathrm{C}$$\mathrm{O_2}$, $\mathrm{H_2}$$\mathrm{O}$ | Inert/fully oxidized → no additional $\mathrm{O_2}$                                                       | 0.0                                                       |

2. Compute the stoichiometric $\mathrm{O_2}$ requirement per mole of fuel mixture as

   $$
   \nu_{\mathrm{O_2,stoich}} = \sum_i x_i \,\nu_{\mathrm{O_2},i}
   $$

   Using the mole fractions from Section 4.1 for the present fuel:

3. For later hydraulic and performance interpretation, it is also useful to express this on a mass basis.

   For 1 kg of fuel, the total fuel moles are

   $$
   \mathrm{n_{fuel,total}} = \sum_i \frac{w_i}{M_i}
   $$

   Thus the stoichiometric $\mathrm{O_2}$ requirement per unit fuel mass is

   $$
   n_{\mathrm{O_2,stoich}}^{(m)}
   = \nu_{\mathrm{O_2,stoich}} \, n_{\text{fuel,total}}
   $$

   Converting to mass of $\mathrm{O_2}$ per kg of fuel:

   $$
   \dot{m}_{\mathrm{O_2,stoich}}
   = n_{\mathrm{O_2,stoich}}^{(m)} M_{\mathrm{O_2}}
   $$

### Air-fuel ratio and excess air $\lambda$

The simulation specifies an excess air ratio $\lambda = 1.05$ in `config/operation.yaml`. This value enters the calculation through `air_flow_rates(air, fuel, excess)` in `combustion/flue.py`.

#### Actual $\mathrm{O_2}$ supplied {- .unlisted}

Using:

$$
\dot{n}_{\mathrm{O_2,actual}}
= \lambda \,\dot{n}_{\mathrm{O_2,stoich}}
= \lambda \,\nu_{\mathrm{O_2,stoich}} \,\dot{n}_{\mathrm{fuel}}
$$

#### Air required {- .unlisted}

Air $\mathrm{O_2}$ mole fraction (from `air.yaml`): $x_{\mathrm{O_2,air}}$

Air moral flow, given by `air_flow_rates()`:

$$
\dot{n}_{\text{air}}
= \frac{\dot{n}_{\mathrm{O_2,actual}}}{x_{\mathrm{O_2,air}}}
$$

The air molar mass (mixture weighted) is:

$$
M_{\text{air}} = \sum_i x_i\, M_i
$$

Therefore the air mass flow rate:

$$
\dot{m}_{\text{air}}
= \dot{n}_{\text{air}} M_{\text{air}}
$$

#### Air–fuel ratio {- .unlisted}

Mass based air fuel ratio:

$$
\text{AFR} = \frac{\dot{m}_{\text{air}}}{\dot{m}_f}
$$

## Heating values and firing rate

The fuel lower and higher heating values, and the corresponding firing rate, are evaluated in `combustion/heat.py` by the function `compute_LHV_HHV(fuel, air)` and then used by `total_input_heat()`.

### HHV and LHV

For each fuel species, complete combustion is considered:

- $C$$\mathrm{H_4}$ + 2 $\mathrm{O_2}$ → $C$$\mathrm{O_2}$ + 2 $\mathrm{H_2}$$O$
- $\mathrm{C_2}$$\mathrm{H_6}$ + 3.5 $\mathrm{O_2}$ → 2 $C$$\mathrm{O_2}$ + 3 $\mathrm{H_2}$$O$

The implementation also supports heavier hydrocarbons ($\mathrm{C_3}\mathrm{H_8}, \mathrm{C_4}\mathrm{H_{10}}$) and sulphur species ($\mathrm{H_2}S$), which are handled using stoichiometric oxygen requirements.

Builds complete-combustion products assuming all water remains in the vapour phase. The lower heating value (LHV) is obtained directly from the gas-phase products.

The higher heating value (HHV) is obtained by adding the latent heat of condensation of the water formed.

### Latent heat of water {- .unlisted}

Obtain the latent heat of vaporization of water at the reference pressure
$P_\mathrm{ref} = 101{,}325\ \mathrm{Pa}$ from the IAPWS-97 correlation:

```python
latent_H2O = WaterProps.h_g(P_ref) - WaterProps.h_f(P_ref)
```

where:

- $\mathrm{h_g}$ is the saturated vapour enthalpy,
- $\mathrm{h_f}$ is the saturated liquid enthalpy.

### Reference thermodynamic data {- .unlisted}

All reactant and product enthalpies are obtained from the Cantera thermodynamic database via the mechanism file `config/flue_cantera.yaml`.

Mixture molar enthalpies are evaluated at the reference state $T_\mathrm{ref}=298.15\ \mathrm{K}$ and $P_\mathrm{ref}=101{,}325\ \mathrm{Pa}$ using Cantera's species NASA polynomial fits.

### Methodology {- .unlisted}

The mixture molar heating values are computed directly from the molar enthalpy
difference between reactants and products at the reference state:

$$
\mathrm{LHV}_\mathrm{mol}
=
h_\mathrm{react}(T_\mathrm{ref},P_\mathrm{ref})
-
h_\mathrm{prod}(T_\mathrm{ref},P_\mathrm{ref})
$$

The higher heating value is then obtained as

$$
\mathrm{HHV}_\mathrm{mol}
=
\mathrm{LHV}_\mathrm{mol}
+
n_{\mathrm{H_2O}}
\,
\left(
h_g - h_f
\right)
M_{\mathrm{H_2O}}
$$

After obtaining the mixture molar heating values, conversion to mass basis uses

$$
\text{HHV}_\mathrm{mix}
=
\frac{\text{HHV}_\mathrm{mol}}{M_\mathrm{mix}}, \qquad
\text{LHV}_\mathrm{mix}
=
\frac{\text{LHV}_\mathrm{mol}}{M_\mathrm{mix}},
$$

The firing rate corresponding to a fuel mass flow $\dot m_f$ then follows directly:

$$
P_\mathrm{HHV}
=
\dot m_f \, \text{HHV}_\mathrm{mix},
\qquad
P_\mathrm{LHV}
=
\dot m_f \, \text{LHV}_\mathrm{mix}.
$$

### Total heat input

The function `total_input_heat()` combines chemical and sensible contributions:

where `sensible_heat()` uses:

$$
Q_\text{sens}
=
\dot{m}
\left[
h(T,P,Y) - h(T_\text{ref},P,Y)
\right]
$$

Both fuel and air enter at 300 K, while the reference is 298.15 K; the resulting sensible
contributions are very small compared with the chemical term $P_\mathrm{LHV}$ (on the order of
tens of kW versus tens of MW). Therefore:

$$
Q_\text{in} = P_\mathrm{LHV} + Q_{\text{sens,fuel}} + Q_{\text{sens,air}} \approx P_\mathrm{LHV}
$$

## Flame and flue gas

The combustion model must provide two closely related but conceptually distinct outputs:

1. The adiabatic flame temperature $T_\mathrm{ad}$ and equilibrium combustion state, which define the thermodynamic upper limit of the combustion process.
2. A practical flue-gas stream to be used as the hot-side working fluid in the boiler heat-transfer and pressure-drop calculations.

These two objectives place conflicting requirements on the combustion model.  
Accurate prediction of $T_\mathrm{ad}$ requires a full chemical-equilibrium treatment including high-temperature dissociation. In contrast, boiler heat-transfer and hydraulics require a chemically frozen reduced product set with stable thermophysical properties.

For this reason, the model deliberately computes two distinct flue-gas representations from the same reactant energy balance:

- an equilibrium flue gas used solely to determine $T_\mathrm{ad}$ and equilibrium composition, and
- a fully burnt boiler flue gas used as the working fluid throughout the boiler model.

Both streams are derived from the same inlet conditions and satisfy the same adiabatic, constant-pressure energy balance, but they differ in their chemical treatment and intended use.

### Methodology

Fuel and air are assumed to mix perfectly and react adiabatically at constant pressure $P$, equal to the inlet pressure. Heat losses and shaft work are neglected.

The total inlet enthalpy rate of the unmixed reactants is

$$
\dot{H}_\mathrm{react}
= \dot{m}_\mathrm{air} \, h_\mathrm{air}(T_\mathrm{air}, P, \mathbf{X}_\mathrm{air})
+ \dot{m}_\mathrm{fuel} \, h_\mathrm{fuel}(T_\mathrm{fuel}, P, \mathbf{X}_\mathrm{fuel})
$$

with total mass flow

$$
\dot{m}_\mathrm{tot} = \dot{m}_\mathrm{air} + \dot{m}_\mathrm{fuel}.
$$

The target specific enthalpy of the reacting mixture is therefore

$$
h_\mathrm{target} = \frac{\dot{H}_\mathrm{react}}{\dot{m}_\mathrm{tot}}.
$$

The overall reactant composition is constructed from the molar flow rates of each species in the fuel and air streams.  
Reactant species molar flow rates are obtained by converting inlet mass fractions to mole fractions and scaling by the corresponding total molar flow rates:

$$
\dot n_i^{(\mathrm{air})}, \qquad \dot n_i^{(\mathrm{fuel})}.
$$

The total molar flow rate of species $i$ is

$$
\dot n_i = \dot n_i^{(\mathrm{air})} + \dot n_i^{(\mathrm{fuel})},
$$

and the overall reactant mole fractions are

$$
X_{i,\mathrm{react}} = \frac{\dot n_i}{\sum_j \dot n_j}.
$$

This reactant mixture, together with $h_\mathrm{target}$ and pressure $P$, defines the common thermodynamic basis for both flue-gas representations described below.

### Equilibrium flame state and adiabatic flame temperature

The equilibrium flame state is computed using Cantera by enforcing chemical equilibrium at constant enthalpy and pressure:

$$
\begin{aligned}
h_\mathrm{products}(T_\mathrm{ad}, P, \mathbf{X}_\mathrm{eq}) &= h_\mathrm{target}, \\
P_\mathrm{out} &= P,
\end{aligned}
$$

where $\mathbf{X}_\mathrm{eq}$ satisfies chemical equilibrium at $(T_\mathrm{ad}, P)$.

The reacting mixture is initialized at $T = 300\,\mathrm{K}$, pressure $P$, and composition $\mathbf{X}_\mathrm{react}$, and Cantera’s `HP` equilibrium solver is used to determine the equilibrium temperature and species composition.

The resulting equilibrium flue gas:

- includes all species permitted by the chemical mechanism, including dissociation products,
- defines the adiabatic flame temperature $T_\mathrm{ad}$,
- is used exclusively for combustion diagnostics and performance assessment.

This stream is not used in downstream boiler calculations.

### Boiler flue gas

For boiler heat-transfer and pressure-drop calculations, a second flue-gas stream is constructed assuming complete combustion without dissociation.

Complete oxidation is implemented explicitly for a fixed fuel species set (CH$_4$, C$_2$H$_6$, C$_3$H$_8$, C$_4$H$_{10}$, H$_2$S), accounting for any CO$_2$, H$_2$O, N$_2$, and Ar present in the inlet streams, and assuming excess-air operation ($\lambda \ge 1$). The resulting product set is limited to stable species such as CO$_2$, H$_2$O, N$_2$, O$_2$, Ar, and SO$_2$.

The boiler flue-gas temperature $T_\mathrm{flue}$ is obtained from an adiabatic, constant-pressure energy balance:

$$
h_\mathrm{products}(T_\mathrm{flue}, P, \mathbf{Y}_\mathrm{burnt}) = h_\mathrm{target}.
$$

This fully burnt, chemically frozen flue gas:

- satisfies the same overall energy balance as the equilibrium flame state,
- has a reduced, stable species set suitable for property evaluation,
- is used as the hot-side working fluid in all boiler heat-transfer and pressure-drop calculations.

\newpage
