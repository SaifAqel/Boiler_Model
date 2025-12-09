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
Its composition is specified on a mass fraction basis and converted internally to mole fractions for all stoichiometric and thermodynamic calculations.

Table: Fuel composition in both mass and mole fractions.

| Component        | Formula              | Mass fraction $\mathrm{w_i}$ [-] | Mole fraction $\mathrm{x_i}$ [-] |
| ---------------- | -------------------- | -------------------------------- | -------------------------------- |
| Methane          | $\mathrm{CH_4}$      | 0.80                             | 0.8895                           |
| Ethane           | $\mathrm{C_2H_6}$    | 0.10                             | 0.0593                           |
| Propane          | $\mathrm{C_3H_8}$    | 0.04                             | 0.0162                           |
| n-Butane         | $\mathrm{C_4H_{10}}$ | 0.01                             | 0.00307                          |
| Hydrogen sulfide | $\mathrm{H_2S}$      | 0.01                             | 0.00523                          |
| Nitrogen         | $\mathrm{N_2}$       | 0.02                             | 0.0127                           |
| Carbon dioxide   | $\mathrm{CO_2}$      | 0.01                             | 0.00405                          |
| Water vapour     | $\mathrm{H_2O}$      | 0.01                             | 0.00990                          |

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
- composition specified on a mass fraction basis.

  | Component      | Formula         | Mass fraction $w_i$ [-] |
  | -------------- | --------------- | ----------------------- |
  | Oxygen         | $\mathrm{O_2}$  | 0.232                   |
  | Nitrogen       | $\mathrm{N_2}$  | 0.755                   |
  | Argon          | $Ar$            | 0.0128                  |
  | Carbon dioxide | $\mathrm{CO_2}$ | $6.1\times 10^{-4}$     |

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
contributions are small compared with the chemical term $P_\mathrm{LHV}$ (on the order of
tens of kW versus tens of MW). Therefore, numerically:

- Total heat input including sensible:
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

In the combustion model two different flue gas streams are distinguished:

1. An equilibrium flue gas at adiabatic flame conditions (`flue_ad`), obtained from high temperature HP equilibrium in Cantera.
2. A fully burnt boiler flue gas (`flue`), obtained from pure stoichiometry with excess air and no dissociation, used throughout the heat-exchanger network.

Both are represented as `GasStream` objects and stored in the `CombustionResult`, but they serve different purposes in the boiler calculation.

### Definitions and distinction

- **Equilibrium flue gas (`flue_ad`)**

  - Thermodynamic state: high temperature HP equilibrium at the adiabatic flame temperature.
  - Contains all equilibrium species allowed by the mechanism (major products + dissociation products + radicals).
  - Used only to:
    - determine the adiabatic flame temperature $T_\mathrm{ad}$,
    - report equilibrium composition in diagnostics/CSV.

- **Fully burnt flue gas (`flue`)**
  - Thermodynamic state: chemically frozen, fully burnt mixture at the same temperature and pressure as the equilibrium gas at burner exit.
  - Contains only “engineering” products ($C$$\mathrm{O_2}$, $\mathrm{H_2}$$O$, $S$$\mathrm{O_2}$, $\mathrm{O_2}$, $\mathrm{N_2}$, $Ar$) with no $CO$, $\mathrm{H_2}$, $N$$\mathrm{O_x}$ or radicals.
  - Used as the hot-side gas in all boiler heat-transfer and pressure-drop calculations.

Hence, equilibrium chemistry is confined to the flame-temperature calculation, while the boiler itself is solved with a simplified, fully burnt flue gas consistent with complete combustion and 10 % excess air.

### Equilibrium flue gas at adiabatic conditions

The adiabatic flame calculation is performed in `combustion/adiabatic_flame_temperature.py` via the function `adiabatic_flame_T(air, fuel)`:

- The inlet air and fuel streams are:

  - represented as `GasStream` objects (mass flow, $T$, $P$, mass fractions),
  - converted to mole fractions (`to_mole`) and set into separate Cantera `Solution` objects (`gas_air`, `gas_fuel`) based on `config/flue_cantera.yaml`.

- A mixed-reactant state is constructed at constant pressure:

  - Total enthalpy flow of reactants:
    $$
      \dot H_\text{react} = \dot m_\text{air}\, h_\text{air} + \dot m_\text{fuel}\, h_\text{fuel}
    $$
  - Target specific enthalpy:
    $$
      h_\text{target} = \dot H_\text{react} / \dot m_\text{tot}
    $$
  - Overall reactant mole fractions are built from molar flow rates of air and fuel.

- The mixture is then set in Cantera (`gas_mix`) with:

  - composition $X_\text{react}$,
  - pressure $P = P_\text{air}$,
  - specific enthalpy $h = h_\text{target}$,
  - and equilibrated under HP constraints:

    ```python
    gas_mix.TPX = 300.0, P_Pa, X_react   # T placeholder
    gas_mix.HP  = h_target, P_Pa
    gas_mix.equilibrate("HP")
    ```

- After equilibrium:

  - The **adiabatic flame temperature** is `gas_mix.T`.
  - The **equilibrium mass fractions** are read from `gas_mix.Y`:

    ```python
    Y_eq = gas_mix.Y
    comp_eq = {
        sp: Q_(float(Y_eq[i]), "")
        for i, sp in enumerate(gas_mix.species_names)
        if Y_eq[i] > 1e-15
    }
    ```

- These are stored in the equilibrium flue-gas stream:

  ```python
  flue_ad = GasStream(
      mass_flow = Q_(m_tot, "kg/s"),
      T         = Q_(gas_mix.T, "K"),
      P         = air.P,
      comp      = comp_eq,
  )
  ```

Typical equilibrium composition (λ = 1.1, natural gas, $T_\mathrm{ad} = 2050\ \text{K}$) is:

- Major species:
  - $C$$\mathrm{O_2}$ ≈ 0.085–0.095
  - $\mathrm{H_2}$$O$ ≈ 0.075–0.085
  - $\mathrm{O_2}$ ≈ 0.020–0.030 (excess air)
  - $\mathrm{N_2}$ ≈ 0.78–0.80
- Dissociation / minor species:
  - $CO$ ≈ $10^{-3}$
  - $\mathrm{H_2}$ ≈ $10^{-4}$
  - $NO$ ≈ $10^{-4}–10^{-5}$
  - $OH$, $O$, radicals < $10^{-6}$
  - $S$$\mathrm{O_2}$ = $10^{-4}$ (from fuel $\mathrm{H_2}$$S$)

This composition is physically consistent with high-temperature equilibrium at $~2000 K$ and slight dissociation.

The object `flue_ad` is stored in `CombustionResult` and is only used to:

- provide $T_\mathrm{ad}$ and equilibrium composition to the boiler summary CSV,
- support diagnostic post processing.

It is **not** used in the heat exchanger network.

### Fully burnt boiler flue gas

The boiler thermal model requires a chemically simple flue-gas mixture to compute heat transfer and pressure drop. For that purpose a **fully burnt** flue gas is constructed in `combustion/flue.py` and `combustion/combustor.py`:

1. In `Combustor.run()` the air mass flow is first set from stoichiometry plus excess air:

   ```python
   air.mass_flow = air_flow_rates(air, fuel, self.excess_air_ratio)
   ```

2. The fully burnt flue-gas composition is then computed from pure stoichiometry:

   ```python
   mass_comp_burnt, m_dot_flue = from_fuel_and_air(fuel, air)
   ```

   - `from_fuel_and_air` assumes complete oxidation of:
     - C-containing species → $C$$\mathrm{O_2}$,
     - $H$ → $\mathrm{H_2}$$O$,
     - $S$ → $S$$\mathrm{O_2}$,
   - including $C$$\mathrm{O_2}$ and $\mathrm{H_2}$$O$ already present in the inlet fuel and air.
   - The allowed product set is:
     - $C$$\mathrm{O_2}$, $\mathrm{H_2}$$O$, $S$$\mathrm{O_2}$, $\mathrm{O_2}$, $\mathrm{N_2}$, $Ar$.
   - Residual $\mathrm{O_2}$ is determined by the imposed excess air ratio $λ$; there is no $CO$, $\mathrm{H_2}$, $N$$\mathrm{O_x}$, or radicals in this stream.

   Internally, `from_fuel_and_air` works with molar balances:

   - determines stoichiometric $\mathrm{O_2}$ demand per mole of fuel (`stoich_O2_required_per_mol_fuel`),
   - combines fuel and air mole fractions to get:
     $$
     \dot n_{\mathrm{CO_2}},\
     \dot n_{\mathrm{H_2O}},\
     \dot n_{\mathrm{SO_2}},\
     \dot n_{\mathrm{O_2}},\
     \dot n_{\mathrm{N_2}},\
     \dot n_{\mathrm{Ar}}
     $$
   - normalizes by total moles to obtain mole fractions, converts to mass fractions (`to_mass`), and returns both:
     - `mass_comp` (mass fractions),
     - `m_dot` (total mass flow of flue gas).

3. The fully burnt flue-gas stream is then created as:

   ```python
   flue_boiler = GasStream(
       mass_flow = Q_(m_dot_flue, "kg/s"),
       T         = T_ad,     # assume recombination to near Tad at burner exit
       P         = air.P,
       comp      = {sp: Q_(y, "") for sp, y in mass_comp_burnt.items()},
   )
   ```

4. `CombustionResult` is populated with both flue streams:

   ```python
   return CombustionResult(
       LHV        = power_LHV,
       Q_in       = Q_in,
       T_ad       = T_ad,
       flue       = flue_boiler,  # fully burnt flue used in boiler model
       flue_ad    = flue_ad,      # equilibrium flue at Tad (diagnostics)
       fuel_LHV_mass = LHV_mass,
       fuel_P_LHV    = P_LHV,
   )
   ```

The **boiler solver** (`run_hx`) always receives `combustion.flue` (i.e. `flue_boiler`) as its gas inlet, and this fully burnt composition is used for:

- gas properties (`cp`, ρ, μ, k),
- heat-transfer coefficients,
- radiative heat transfer (emissivity based on $C$$\mathrm{O_2}$/$\mathrm{H_2}$$O$/$S$$\mathrm{O_2}$),
- pressure-drop estimates and stack temperature.

Thus, the equilibrium flue gas provides a physically consistent high-temperature reference, while the fully burnt flue gas represents the practical working fluid in the convective–radiative sections of the boiler.

### Output fields

The flue-gas information exposed to the rest of the model and to the post-processing is encapsulated in `CombustionResult`:

```python
@dataclass(frozen=True)
class CombustionResult:
    LHV: Q_
    Q_in: Q_
    T_ad: Q_
    flue: GasStream               # fully-burnt flue used in boiler
    flue_ad: GasStream | None = None   # equilibrium flue at T_ad (optional)
    fuel_LHV_mass: Q_ | None = None
    fuel_P_LHV: Q_ | None = None
```

The relevant report/CSV entries are:

| Field     | Meaning                                                                  |
| --------- | ------------------------------------------------------------------------ |
| `T_ad`    | Adiabatic flame temperature from HP equilibrium                          |
| `flue_ad` | `GasStream` of equilibrium flue gas (adiabatic composition, diagnostics) |
| `flue`    | `GasStream` of fully burnt flue gas used in all boiler HX calculations   |

This completes the description of how flue-gas composition is defined, distinguished, and used in the boiler model.
