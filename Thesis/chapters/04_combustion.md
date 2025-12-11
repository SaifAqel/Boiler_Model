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

For the current working fuel:

- Stoichiometric oxygen requirement:
  $\nu_{\mathrm{O_2,stoich}} = 2.09 \text{ mol $\mathrm{O_2}$ per mol fuel mixture}$
- Equivalent mass requirement:
  $\dot{m}_{\mathrm{O_2,stoich}} = 3.75 \text{ kg $\mathrm{O_2}$ per kg fuel}$

### Air–fuel ratio and excess air $\lambda$

The simulation specifies an excess air ratio $\lambda = 1.1$

in `config/operation.yaml`. This value enters the calculation through  
`air_flow_rates(air, fuel, excess)` in `combustion/flue.py`.

#### Actual $\mathrm{O_2}$ supplied {- .unlisted}

Using:

$$
\dot{n}_{\mathrm{O_2,actual}}
= \lambda \,\dot{n}_{\mathrm{O_2,stoich}}
= \lambda \,\nu_{\mathrm{O_2,stoich}} \,\dot{n}_{\mathrm{fuel}}
$$

#### Air required {- .unlisted}

Air $\mathrm{O_2}$ mole fraction (from `air.yaml`): $x_{\mathrm{O_2,air}} = 0.2095$

Air moral flow, given by `air_flow_rates()`:

$$
\dot{n}_{\text{air}}
= \frac{\dot{n}_{\mathrm{O_2,actual}}}{x_{\mathrm{O_2,air}}}
$$

The air molar mass (mixture weighted) is: $M_{\text{air}} = 0.02897\;\text{kg/mol}$

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

The fuel lower and higher heating values, and the corresponding firing rate, are evaluated in `combustion/heat.py` by the function `compute_LHV_HHV(fuel)` and then used by `total_input_heat()`.

### HHV and LHV

For each fuel species, complete combustion is considered:

- $C$$\mathrm{H_4}$ + 2 $\mathrm{O_2}$ → $C$$\mathrm{O_2}$ + 2 $\mathrm{H_2}$$O$
- $\mathrm{C_2}$$\mathrm{H_6}$ + 3.5 $\mathrm{O_2}$ → 2 $C$$\mathrm{O_2}$ + 3 $\mathrm{H_2}$$O$

Builds product formation enthalpies for:

- HHV assumption: water as liquid (condensed)
- LHV assumption: water as vapour (no condensation heat recovered)

### Latent heat of water {- .unlisted}

Obtain the latent heat of vaporization of water at the reference pressure
$P_\mathrm{ref} = 101{,}325\ \mathrm{Pa}$ from the IAPWS-97 correlation:

```python
latent_H2O = WaterProps.h_g(P_ref) - WaterProps.h_f(P_ref)
```

where:

- $\mathrm{h_g}$ is the saturated vapour enthalpy,
- $\mathrm{h_f}$ is the saturated liquid enthalpy.

### Reference formation enthalpies {- .unlisted}

Standard formation enthalpies $\Delta h^\circ_\mathrm{f}$ (at 298.15 K, 1 bar) are taken from
`common/constants.py` in kJ/mol:

Table: Standard enthalpy of formation of selected species [@nist]

| Species              | $\Delta h^\circ_{\mathrm{f}} \; (\mathrm{kJ}\,\mathrm{mol}^{-1})$ |
| -------------------- | ----------------------------------------------------------------- |
| $\mathrm{CH_4}$      | –74.8                                                             |
| $\mathrm{C_2H_6}$    | –84.7                                                             |
| $\mathrm{C_3H_8}$    | –103.8                                                            |
| $\mathrm{C_4H_{10}}$ | –126.1                                                            |
| $\mathrm{SO_2}$      | –296.8                                                            |
| $\mathrm{CO_2}$      | –393.5                                                            |
| $\mathrm{H_2O(l)}$   | –285.5                                                            |

### Methodology {- .unlisted}

The mixture molar higher and lower heating values are:

$$
\text{HHV}_\mathrm{mol} = h_\mathrm{react} - h_{\mathrm{prod,HHV}}, \quad
\text{LHV}_\mathrm{mol} = h_\mathrm{react} - h_{\mathrm{prod,LHV}}
$$

These are converted to mass based heating values.

For each species $i$ in the fuel, the reaction enthalpy contribution is

$$
\Delta h_i
=
x_i \left[
\Delta h^\circ_{\mathrm{f,products}}
-
\Delta h^\circ_{\mathrm{f,reactants}}
\right],
$$

and mixture HHV and LHV are obtained by summing these contributions over all fuel
components, enforcing the appropriate water phase:

- HHV: water in products is liquid
- LHV: water in products is vapour

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

For the fuel specified above, the mixture heating values are:

Table: Heating values and firing rates, returned by `compute_LHV_HHV()`

| Variable                    | Value              |
| --------------------------- | ------------------ |
| $\mathrm{HHV}_\mathrm{mix}$ | $52\ \text{MJ/kg}$ |
| $\mathrm{LHV}_\mathrm{mix}$ | $47\ \text{MJ/kg}$ |
| $P_\mathrm{HHV}$            | $26\ \text{MW}$    |
| $P_\mathrm{LHV}$            | $23.6\ \text{MW}$  |

### Total heat input

The function `total_input_heat()` combines chemical and sensible contributions:

where `sensible_heat()` uses:

$$
Q_\text{sens} = \dot{m}\, c_p \,(T - T_\text{ref})
$$

Both fuel and air enter at 300 K, while the reference is 298.15 K; the resulting sensible
contributions are very small compared with the chemical term $P_\mathrm{LHV}$ (on the order of
tens of kW versus tens of MW). Therefore:

$$
Q_\text{in} = P_\mathrm{LHV} + Q_{\text{sens,fuel}} + Q_{\text{sens,air}}
$$

## Adiabatic flame temperature

The adiabatic flame temperature $T_\mathrm{ad}$ is evaluated in the model by the function `adiabatic_flame_T()` in `combustion/adiabatic_flame_temperature.py`. This routine uses Cantera and an enthalpy–pressure equilibrium (`HP`) function to determine the equilibrium temperature and composition of the flue gas, assuming:

- complete mixing of fuel and air,
- no heat losses to the surroundings (adiabatic),
- constant system pressure (equal to the air/fuel inlet pressure),
- chemical equilibrium among all gas species.

The total inlet enthalpy rate of the unmixed reactants is

$$
\dot{H}_\mathrm{react}
= \dot{m}_\mathrm{air} \, h_\mathrm{air}(T_\mathrm{air}, P, X_\mathrm{air})
+ \dot{m}_\mathrm{fuel} \, h_\mathrm{fuel}(T_\mathrm{fuel}, P, X_\mathrm{fuel})
$$

The total mass flow is

$$
\dot{m}_\mathrm{tot} = \dot{m}_\mathrm{air} + \dot{m}_\mathrm{fuel}
$$

so the mixture-averaged specific enthalpy of the reactants is

$$
h_\mathrm{target} = \frac{\dot{H}_\mathrm{react}}{\dot{m}_\mathrm{tot}}
$$

The adiabatic, constant-pressure equilibrium state is then defined by the constraints:

$$
\begin{aligned}
h_\mathrm{products}(T_\mathrm{ad}, P, \mathbf{X}_\mathrm{eq}) &= h_\mathrm{target} \\
P_\mathrm{out} &= P \\
\mathbf{X}_\mathrm{eq} &\text{ satisfies chemical equilibrium at }(T_\mathrm{ad}, P)
\end{aligned}
$$

Cantera is used to enforce this condition via its `HP` equilibrium mode.

Build the overall reactant composition $\mathbf{X}_\mathrm{react}$ from the
molar flow rates of each component in each stream:

Determine molar flow rates of all species in the air and fuel streams,  
$$\dot n_i^{(\mathrm{air})},\quad \dot n_i^{(\mathrm{fuel})}.$$

Form the total species molar flow rate,  
$$\dot n_i = \dot n_i^{(\mathrm{air})} + \dot n_i^{(\mathrm{fuel})}.$$

Compute the overall reactant mole fractions,  
$$X_{i,\mathrm{react}} = \frac{\dot n_i}{\sum_j \dot n_j}$$

Initialize the mixture and perform HP equilibrium:

Initialize the reacting mixture at  
temperature $T = 300\,\mathrm{K}$, pressure $P$, and composition $X_{\mathrm{react}}$.

Impose the constraint of fixed enthalpy and pressure,  
$$h = h_{\mathrm{target}},\qquad P = P,$$

and compute the chemical equilibrium state under $(H,P)$ conditions.

Obtain the equilibrium mass fractions  
$$Y_{i,\mathrm{eq}}$$

The HP-equilibrium calculation yields an adiabatic flame temperature on the order of:

$$
T_\mathrm{ad} \;=\; 2{,}050\ \mathrm{K}
\quad (= 1{,}780^\circ\mathrm{C})
$$

This value is consistent with typical adiabatic flame temperatures for natural gas with around 10 % excess air and confirms that the combustion zone (furnace) operates at very high gas temperatures [@turns2012], driving strong radiative and convective heat transfer to the shell-side water/steam.

## Flue gas composition

In the combustion model two different flue gas streams are distinguished, represented as `GasStream` objects and stored in the `CombustionResult`, but they serve different purposes in the boiler calculation:

1. Equilibrium flue gas (`flue_ad`)

   - Defined as the flue gas mixture at adiabatic flame conditions, obtained from a high-temperature HP equilibrium calculation in Cantera.
   - Contains all equilibrium species permitted by the reaction mechanism.
   - Its purposes are:
     - determining the adiabatic flame temperature $T_\mathrm{ad}$,
     - providing the equilibrium composition for diagnostics.

2. Fully burnt flue gas (`flue`)

   - Defined as a chemically frozen, fully burnt mixture at the same temperature and pressure as the equilibrium (`flue_ad`).
   - Contains only standard engineering combustion products.
   - Used as the hot side working gas for all boiler heat transfer and pressure drop calculations throughout the heat-exchanger network.

The equilibrium flue gas provides a physically consistent high temperature reference, while the fully burnt flue gas represents the practical working fluid in the convective radiative sections of the boiler.

### Fully burnt boiler flue gas {- .unlisted}

Starting from the fuel and air known `GasStream` objects, compute molar formation rates and flow rate as:

Using the fuel and air molar flow rates, $\dot n_{\mathrm{fuel}}$ and $\dot n_{\mathrm{air}}$, and their mole fractions $x_i^{(\mathrm{fuel})}$ and $x_i^{(\mathrm{air})}$, for any product species $k$, the molar flow rate is written generically as

$$
\dot n_k
= \dot n_{\mathrm{fuel}}\,\Phi_k^{(\mathrm{fuel})}
+ \dot n_{\mathrm{air}}\,\Phi_k^{(\mathrm{air})},
$$

where

- $\Phi_k^{(\mathrm{fuel})}$ is the amount of species $k$ that comes from the fuel:
  species already present in the fuel plus any of $k$ formed by complete oxidation of the fuel components.

- $\Phi_k^{(\mathrm{air})}$ is the amount of species $k$ that comes from the air:
  species originally present in the air plus any portion that remains unreacted.

Oxygen additionally satisfies

$$
\dot n_{O_2}
= \dot n_{\mathrm{air}}\,x^{(\mathrm{air})}_{O_2}
- \dot n_{\mathrm{fuel}}\,\nu_{O_{2},\mathrm{stoich}},
$$

where $\nu_{O_{2},\mathrm{stoich}}$ is the stoichiometric oxygen demand of the fuel.

The total molar flow rate of the fully burnt flue gas is

$$
\dot n_\mathrm{tot}
=
\sum_k \dot n_k.
$$

The molar fractions of the products are then

$$
x_k^\mathrm{(flue)}
=
\frac{\dot n_k}{\dot n_\mathrm{tot}}.
$$

These molar fractions are converted to product mass fractions by `to_mass()`:

$$
w_k^\mathrm{(flue)}
=
\frac{x_k^\mathrm{(flue)} M_k}{\sum_j x_j^\mathrm{(flue)} M_j}.
$$

Finally, the flue gas total mass flow rate is obtained from the molar composition and total molar flow via `mass_flow()`:

$$
\dot m_\mathrm{flue}
=
\sum_k x_k^\mathrm{(flue)} \,\dot n_\mathrm{tot} M_k.
$$

The function `from_fuel_and_air()` returns the fully burnt flue gas composition $w_k^\mathrm{(flue)}$ and the total flue mass flow $\dot m_\mathrm{flue}$.

This separation allows the model to retain a realistic high temperature reference from chemical equilibrium while employing a reduced, engineering flue gas composition for subsequent heat transfer and hydraulic calculations.

\newpage
