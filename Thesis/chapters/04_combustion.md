# Combustion Model

The combustion module forms the first stage of the design workflow. It reads all run-specific configurations and parameters from YAML files and simulates the combustion process for the specified fuel and air streams at the given excess air ratio. Its outputs are the adiabatic flame temperature, used as the inlet temperature for the flue gas entering the first pass, and the fully combusted flue gas composition. Together, these results define the flue-gas stream supplied to the heat-transfer model.

## Fuel Stream

The boiler is fired with a natural-gas–type fuel defined in the simulation input (`config/fuel.yaml`).  
The fuel is supplied at $300 K$ and $1.013×10⁵ Pa$ with a mass flow rate of $0.1 kg/s$.  
Its composition is specified on a mass-fraction basis and converted internally to mole fractions for all stoichiometric and thermodynamic calculations.

Table 4-1 summarizes the fuel composition in both mass and mole fraction form.

| Component        | Formula                         | Mass fraction $\mathrm{w_i}$ [-] | Mole fraction $\mathrm{x_i}$ [-] | Comment                                                             |
| ---------------- | ------------------------------- | -------------------------------- | -------------------------------- | ------------------------------------------------------------------- |
| Methane          | $\mathrm{CH_4}$                 | 0.80                             | 0.8895                           | Main combustible, dominant contributor to LHV                       |
| Ethane           | $\mathrm{C_2}$$\mathrm{H_6}$    | 0.10                             | 0.0593                           | Heavier hydrocarbon, increases LHV and required $\mathrm{O_2}$      |
| Propane          | $\mathrm{C_3}$$\mathrm{H_8}$    | 0.04                             | 0.0162                           | Heavier hydrocarbon, raises flame temperature                       |
| n-Butane         | $\mathrm{C_4}$$\mathrm{H_{10}}$ | 0.01                             | 0.00307                          | Minor heavy hydrocarbon fraction                                    |
| Hydrogen sulfide | $\mathrm{H_2}$$\mathrm{S}$      | 0.01                             | 0.00523                          | Sulfur-bearing contaminant → $\mathrm{S}$$\mathrm{O_2}$ in flue gas |
| Nitrogen         | $\mathrm{N_2}$                  | 0.02                             | 0.0127                           | Inert ballast in the fuel stream                                    |
| Carbon dioxide   | $\mathrm{C}$$\mathrm{O_2}$      | 0.01                             | 0.00405                          | Inert (already fully oxidized)                                      |
| Water vapour     | $\mathrm{H_2}$$\mathrm{O}$      | 0.01                             | 0.00990                          | Moisture carried with the fuel                                      |

The mass fractions sum to 1.0 by definition. The mole fractions $\mathrm{x_i}$ are obtained from

$$
x_i \;=\; \frac{\dfrac{w_i}{M_i}}{\sum_j \dfrac{w_j}{M_j}}
$$

which is provided by the function `to_mol` in `combustion/mass_mole.py`, where $\mathrm{M_i}$ is the molar mass of species $i$ from `molar_masses` in `common/constants.py`.

## Air Stream

## Model flow

The purpose of the combustion model is to determine combustion conditions inside the furnace (1st pass), resulting in a fully burnt flue gas stream entering the heat transfer model at adiabatic temperature.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{Thesis/figures/combustion_flow.pdf}
\caption{Combustion flow}
\label{fig:combustion-flow}
\end{figure}

## Stoichiometric $\mathrm{O_2}$ requirement

Evaluated the stoichiometric oxygen requirement via `stoich_O2_required_per_mol_fuel`
in `combustion/flue.py`. The algorithm is:

1. Use per mole of species stoichiometric $\mathrm{O_2}$ factors $\nu_{\mathrm{O_{2,i}}}$ from `O2_per_mol` in `common/constants.py`:

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
   \nu_{\mathrm{O_2,stoich}}
   \;=\; \sum_i x_i \,\nu_{\mathrm{O_2},i}
   $$

   Using the mole fractions from Section 4.1 for the present fuel:

   - $x_{\mathrm{CH_4}} = 0.8895$
   - $x_{\mathrm{C_2H_6}} = 0.0593$
   - $x_{\mathrm{C_3H_8}} = 0.0162$
   - $x_{\mathrm{C_4H_{10}}} = 0.00307$
   - $x_{\mathrm{H_2S}} = 0.00523$
   - remaining species: $\mathrm{x_{\mathrm{N_2}}}, \mathrm{x_{\mathrm{CO_2}}}, \mathrm{x_{\mathrm{H_2O}}}$ are inert in the stoichiometric balance.

   Hence

   $$
   \nu_{\mathrm{O_2,stoich}}
   = 2.09 \;\;\text{mol $\mathrm{O_2}$ per mol fuel mixture}
   $$

   This is exactly what `stoich_O2_required_per_mol_fuel` returns:

   ```python
   def stoich_O2_required_per_mol_fuel(fuel: GasStream) -> Q_:
       fuel_x = to_mole(fuel.comp)
       total = sum(fuel_x[k] * O2_per_mol.get(k, 0.0) for k in fuel_x)
       return Q_(total, "dimensionless")
   ```

3. For later hydraulic and performance interpretation, it is also useful to express this on a mass basis.

   For 1 kg of fuel, the total fuel moles are

   $$
   \mathrm{n_{fuel,total}} = \sum_i \frac{w_i}{M_i} = 56.1 \;\text{mol fuel/kg}
   $$

   Thus the stoichiometric $\mathrm{O_2}$ requirement per unit fuel mass is

   $$
   n_{\mathrm{O_2,stoich}}^{(m)}
   = \nu_{\mathrm{O_2,stoich}} \, n_{\text{fuel,total}}
   = 1.17\times 10^2\;\text{mol $\mathrm{O_2}$/kg fuel}
   $$

   Converting to mass of $\mathrm{O_2}$ per kg of fuel:

   $$
   \dot{m}_{\mathrm{O_2,stoich}}
   = n_{\mathrm{O_2,stoich}}^{(m)} M_{\mathrm{O_2}}
   = 3.75 \,\text{kg $\mathrm{O_2}$/kg fuel}
   $$

So, for this fuel:

- Stoichiometric oxygen requirement:  
  $\boxed{\nu_{\mathrm{O_2,stoich}} = 2.09 \text{ mol $\mathrm{O_2}$ per mol fuel mixture}}$
- Equivalent mass requirement:  
  $\boxed{\dot{m}_{\mathrm{O_2,stoich}} = 3.75 \text{ kg $\mathrm{O_2}$ per kg fuel}}$

## Air–fuel ratio and excess air $λ$

The simulation specifies an excess air ratio

$$
\lambda = 1.1
$$

in `config/operation.yaml`. This value enters the calculation through  
`air_flow_rates(air, fuel, excess)` in `combustion/flue.py`.

### Actual $\mathrm{O_2}$ supplied

Using:

$$
\dot{n}_{\mathrm{O_2,actual}}
= \lambda \,\dot{n}_{\mathrm{O_2,stoich}}
$$

Thus:

$$
\dot{n}_{\mathrm{O_2,actual}}
= 1.1 \,\nu_{\mathrm{O_2,stoich}} \,\dot{n}_{\mathrm{fuel}}
$$

The molar fuel flow is determined from the mass-flow rate:

- Fuel mass flow:

  $$
  \dot{m}_f = 0.5 \;\text{kg/s}
  $$

- Total moles per unit mass of fuel mixture (from the mixture molar mass calculation):

  $$
  n_{\text{fuel,total}} = 56.1\;\text{mol/kg}
  $$

- Therefore the total molar fuel flow:
  $$
  \dot{n}_f = 56.1 \times 0.5 = 28.05\;\text{mol/s}
  $$

Hence the stoichiometric and actual $\mathrm{O_2}$ flows are:

$$
\dot{n}_{\mathrm{O_2,stoich}} = 2.09 \times 28.05 = 58.7\;\text{mol/s}
$$

$$
\dot{n}_{\mathrm{O_2,actual}} = 1.1 \times 58.7 = 64.6\;\text{mol/s}
$$

### Air required

Air $\mathrm{O_2}$ mole fraction (from `air.yaml`):

$$
x_{\mathrm{O_2,air}} = 0.2095
$$

Thus:

$$
\dot{n}_{\text{air}}
= \frac{\dot{n}_{\mathrm{O_2,actual}}}{x_{\mathrm{O_2,air}}}
= \frac{64.6}{0.2095}
= 308\;\text{mol/s}
$$

The air molar mass (mixture weighted) is:

$$
M_{\text{air}} = 0.02897\;\text{kg/mol}
$$

Therefore the mass-based air flow rate:

$$
\dot{m}_{\text{air}}
= \dot{n}_{\text{air}} M_{\text{air}}
= 308 \times 0.02897
= 8.93\;\text{kg/s}
$$

### Air–fuel ratio

Mass-based air–fuel ratio:

$$
\text{AFR} = \frac{\dot{m}_{\text{air}}}{\dot{m}_f}
= \frac{8.93}{0.5}
= 17.9
$$

## Lower heating value (LHV) and heat release

The fuel lower and higher heating values, and the corresponding firing rate, are evaluated in
`combustion/heat.py` by the function `compute_LHV_HHV(fuel)` and then used by
`total_input_heat(fuel, air)`.

### Method

#### Latent heat of water

Obtain the latent heat of vaporization of water at the reference pressure
$P_\mathrm{ref} = 101{,}325\ \mathrm{Pa}$ from the IAPWS-97 correlation:

```python
latent_H2O = WaterProps.h_g(P_ref) - WaterProps.h_f(P_ref)
```

where:

- $\mathrm{h_g}$ is the saturated vapour enthalpy,
- $\mathrm{h_f}$ is the saturated liquid enthalpy.

#### Reference formation enthalpies

Standard formation enthalpies $\Delta h^\circ_\mathrm{f}$ (at 298.15 K, 1 bar) are taken from
`common/constants.py` in kJ/mol:

| Species              | $\Delta h^\circ_{\mathrm{f}} \; (\mathrm{kJ}\,\mathrm{mol}^{-1})$ |
| -------------------- | ----------------------------------------------------------------- |
| $\mathrm{CH_4}$      | –74.8                                                             |
| $\mathrm{C_2H_6}$    | –84.7                                                             |
| $\mathrm{C_3H_8}$    | –103.8                                                            |
| $\mathrm{C_4H_{10}}$ | –126.1                                                            |
| $\mathrm{SO_2}$      | –296.8                                                            |
| $\mathrm{CO_2}$      | –393.5                                                            |
| $\mathrm{H_2O(l)}$   | –285.5                                                            |

Table: Standard enthalpy of formation of selected species [@nist]

#### Products for HHV and LHV

For each fuel species, complete combustion is considered:

- $C$$\mathrm{H_4}$ + 2 $\mathrm{O_2}$ → $C$$\mathrm{O_2}$ + 2 $\mathrm{H_2}$$O$
- $\mathrm{C_2}$$\mathrm{H_6}$ + 3.5 $\mathrm{O_2}$ → 2 $C$$\mathrm{O_2}$ + 3 $\mathrm{H_2}$$O$

Builds product formation enthalpies for:

- HHV assumption: water as liquid (condensed)
- LHV assumption: water as vapour (no condensation heat recovered)

```python
H2O_liq = _dHf["H2O"]                       # kJ/mol
H2O_vap = _dHf["H2O"] + latent_H2O * M_H2O  # (kJ/kg)*(kg/mol) = kJ/mol
```

Then, looping over the _molar_ fuel composition `mol_comp = to_mole(fuel.comp)`:

```python
react = 0
HHV_p = 0
LHV_p = 0

for comp, x in mol_comp.items():
    dh = _dHf.get(comp, 0)
    react += x * dh

    C, H = parse_CH(comp)
    if C is not None:
        HHV_p += x * (C * _dHf["CO2"] + (H/2) * H2O_liq)
        LHV_p += x * (C * _dHf["CO2"] + (H/2) * H2O_vap)
    elif comp == "H2S":
        HHV_p += x * (_dHf["SO2"] + H2O_liq)
        LHV_p += x * (_dHf["SO2"] + H2O_vap)
    else:
        HHV_p += x * dh
        LHV_p += x * dh
```

Here:

- `react` represents the mixture-averaged formation enthalpy of the fuel (kJ/mol),
- `HHV_p`, `LHV_p` represent the mixture-averaged formation enthalpy of the ideal products
  for HHV and LHV definitions.

#### Mixture HHV and LHV (molar, then mass-based)

The mixture molar higher and lower heating values are:

$$
\text{HHV}_\mathrm{mol} = h_\mathrm{react} - h_{\mathrm{prod,HHV}}, \quad
\text{LHV}_\mathrm{mol} = h_\mathrm{react} - h_{\mathrm{prod,LHV}}
$$

```python
HHV_mol = react - HHV_p     # kJ/mol
LHV_mol = react - LHV_p     # kJ/mol
```

These are converted to mass-based heating values using the mixture molar mass
$M_\mathrm{mix}$ from `mix_molar_mass(mol_comp)`:

```python
HHV_kg  = HHV_mol / M_mix   # kJ/kg
LHV_kg  = LHV_mol / M_mix   # kJ/kg
```

The function returns these, together with the corresponding firing powers:

```python
P_HHV = (HHV_kg * fuel.mass_flow).to("kW")
P_LHV = (LHV_kg * fuel.mass_flow).to("kW")
```

### Numerical results for the present fuel

For the fuel specified above, the mixture heating values are:

- Higher heating value (HHV, mass-based):
  $$
  \mathrm{HHV}_\mathrm{mix} = 52\,\text{MJ/kg}
  $$
- Lower heating value (LHV, mass-based):
  $$
  \mathrm{LHV}_\mathrm{mix} = 47\,\text{MJ/kg}
  $$

For the specified fuel mass flow rate:

$$
\dot{m}_f = 0.5\ \text{kg/s}
$$

the resulting firing rates are:

- On an HHV basis:

  $$
  P_\mathrm{HHV} = \dot{m}_f \,\mathrm{HHV}_\mathrm{mix}
  = 0.5 \times 52\ \text{MJ/s}
  = 26\ \text{MW}
  $$

- On an LHV basis (used consistently in the simulation):
  $$
  P_\mathrm{LHV} = \dot{m}_f \,\mathrm{LHV}_\mathrm{mix}
  = 0.5 \times 47\ \text{MJ/s}
  = 23.6\ \text{MW}
  $$

These correspond directly to `P_HHV` and `P_LHV` returned by `compute_LHV_HHV`.

### Total heat input to the boiler $\mathrm{Q_{in}}$

The function `total_input_heat(fuel, air)` combines chemical and sensible contributions:

```python
def total_input_heat(fuel, air):
    _, _, _, power_LHV = compute_LHV_HHV(fuel)
    fuel_sens = sensible_heat(fuel)
    air_sens  = sensible_heat(air)
    Q_in = (power_LHV + fuel_sens + air_sens).to("kW")
    return power_LHV, Q_in
```

where `sensible_heat(stream)` uses:

$$
Q_\text{sens} = \dot{m}\, c_p \,(T - T_\text{ref})
$$

Both fuel and air enter at 300 K, while the reference is 298.15 K; the resulting sensible
contributions are small compared with the chemical term $P_\mathrm{LHV}$ (on the order of
tens of kW versus tens of MW). Therefore, numerically:

- LHV-based chemical heat input:

  $$
  P_\mathrm{LHV} = 23.6\ \text{MW}
  $$

- Total heat input including sensible:
  $$
  Q_\text{in} = P_\mathrm{LHV} + Q_{\text{sens,fuel}} + Q_{\text{sens,air}}
  = 23.6\ \text{MW} \quad (\text{increase } < 0.1\%)
  $$

The quantity `Q_in` in the `CombustionResult` object is thus interpreted in the rest of the
boiler model as the total LHV-based heat release available to be transferred to the
water/steam side.

## Adiabatic flame temperature

The adiabatic flame temperature $T_\mathrm{ad}$ is evaluated in the model by the function `adiabatic_flame_T(air, fuel)` in `combustion/adiabatic_flame_temperature.py`. This routine uses Cantera and an enthalpy–pressure equilibrium (`HP`) calculation to determine the final
equilibrium temperature and composition of the flue gas, assuming:

- complete mixing of fuel and air,
- no heat losses to the surroundings (adiabatic),
- constant system pressure (equal to the air/fuel inlet pressure),
- chemical equilibrium among all gas species in `config/flue_cantera.yaml`.

### Thermodynamic formulation

Let the fuel and air streams be characterized by:

- mass flows $\dot{m}_\mathrm{fuel}, \dot{m}_\mathrm{air}$,
- inlet temperatures $T_\mathrm{fuel}, T_\mathrm{air}$,
- pressure $P$,
- compositions (mole fractions) $X_\mathrm{fuel}, X_\mathrm{air}$.

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

### Implementation

Key steps from `adiabatic_flame_T`:

1. Convert the mass-based composition of fuel and air to mole fractions using
   `to_mole(...)` (from `combustion/mass_mole.py`).

2. Create three Cantera `Solution` objects using the mechanism `config/flue_cantera.yaml`:

   ```python
   gas_air  = ct.Solution("config/flue_cantera.yaml", "gas_mix")
   gas_fuel = ct.Solution("config/flue_cantera.yaml", "gas_mix")
   gas_mix  = ct.Solution("config/flue_cantera.yaml", "gas_mix")
   ```

3. Set the inlet states of the separate streams:

   ```python
   gas_air.TPX  = T_air,  P_Pa, X_air
   gas_fuel.TPX = T_fuel, P_Pa, X_fuel
   ```

4. Compute reactant enthalpy rate and target specific enthalpy:

   ```python
   Hdot_react = m_air * gas_air.enthalpy_mass + m_fuel * gas_fuel.enthalpy_mass
   h_target   = Hdot_react / m_tot          # J/kg of mixture
   ```

5. Build the overall reactant composition $\mathbf{X}_\mathrm{react}$ from the
   molar flow rates of each component in each stream:

   ```python
   n_air  = molar_flow(air.comp,  air.mass_flow)
   n_fuel = molar_flow(fuel.comp, fuel.mass_flow)

   # Accumulate species molar flow rates
   n_dot_sp = {...}
   X_react = {k: v / n_sum for k, v in n_dot_sp.items()}
   ```

6. Initialize the mixture and perform HP equilibrium:

   ```python
   gas_mix.TPX = 300.0, P_Pa, X_react   # initial guess for T
   gas_mix.HP  = h_target, P_Pa         # enforce (H,P)
   gas_mix.equilibrate("HP")            # chemical equilibrium
   ```

7. Construct the resulting flue-gas stream:

   ```python
   Y_eq = gas_mix.Y  # equilibrium mass fractions
   comp_eq = {sp: Q_(float(Y_eq[i]), "") for i, sp in enumerate(gas_mix.species_names)
              if Y_eq[i] > 1e-15}

   flue = GasStream(
       mass_flow = Q_(m_tot, "kg/s"),
       T         = Q_(gas_mix.T, "K"),
       P         = air.P,
       comp      = comp_eq,
   )
   ```

The adiabatic flame temperature is then available as `flue.T` and is also stored in
`CombustionResult.T_ad`.

### Numerical result for the present case

For the given conditions:

- Fuel: natural-gas–type mixture from Section 4.1,  
  $\dot{m}_\mathrm{fuel} = 0.5\ \mathrm{kg/s}$, $T_\mathrm{fuel} = 300\ \mathrm{K}$, 1.013×10⁵ Pa.
- Air: dry air at 300 K and 1.013×10⁵ Pa, composition from `config/air.yaml`.
- Excess air: $\lambda = 1.1$ (10 % excess air).

the HP-equilibrium calculation yields an adiabatic flame temperature on the order of:

$$
T_\mathrm{ad} \;=\; 2{,}050\ \mathrm{K}
\quad (= 1{,}780^\circ\mathrm{C})
$$

This value is consistent with typical adiabatic flame temperatures for natural gas with
around 10 % excess air and confirms that the combustion zone (furnace) operates at very high gas temperatures, driving strong radiative and convective heat transfer to the
shell-side water/steam.

The scalar `T_ad` is passed forward and written into the boiler summary CSV
(`*_boiler_summary.csv`) for reference and later comparison with non-adiabatic stack
temperatures obtained from the full boiler simulation.

## Flue-gas composition

In the combustion model two different flue-gas streams are distinguished:

1. An **equilibrium flue gas at adiabatic flame conditions** (`flue_ad`), obtained from high-temperature HP equilibrium in Cantera.
2. A **fully burnt boiler flue gas** (`flue`), obtained from pure stoichiometry with excess air and no dissociation, used throughout the heat-exchanger network.

Both are represented as `GasStream` objects and stored in the `CombustionResult`, but they serve different purposes in the boiler calculation.

### Definitions and distinction

- **Equilibrium flue gas (`flue_ad`)**

  - Thermodynamic state: high-temperature HP equilibrium at the adiabatic flame temperature.
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

- The inlet **air** and **fuel** streams are:

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
- support diagnostic post-processing.

It is **not** used directly in the heat-exchanger network.

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
