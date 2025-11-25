# Combustion Model

## Fuel composition

The boiler is fired with a natural-gas–type fuel defined in the simulation input (`config/fuel.yaml`).  
The fuel is supplied at 300 K and 1.013×10⁵ Pa with a mass flow rate of $0.5 kg·s⁻¹$.  
Its composition is specified on a mass-fraction basis and converted internally to mole fractions for all stoichiometric and thermodynamic calculations.

Table 4-1 summarises the fuel composition in both mass and mole fraction form.

| Component        | Formula         | Mass fraction $\mathrm{w_i}$ [-] | Mole fraction $\mathrm{x_i}$ [-] | Comment                                              |
| ---------------- | --------------- | -------------------------------- | -------------------------------- | ---------------------------------------------------- |
| Methane          | $\mathrm{CH_4}$ | 0.80                             | 0.8895                           | Main combustible, dominant contributor to LHV        |
| Ethane           | $C₂H₆$          | 0.10                             | 0.0593                           | Heavier hydrocarbon, increases LHV and required $O₂$ |
| Propane          | $C₃H₈$          | 0.04                             | 0.0162                           | Heavier hydrocarbon, raises flame temperature        |
| n-Butane         | $C₄H₁₀$         | 0.01                             | 0.00307                          | Minor heavy hydrocarbon fraction                     |
| Hydrogen sulfide | $H₂S$           | 0.01                             | 0.00523                          | Sulfur-bearing contaminant → $SO₂$ in flue gas       |
| Nitrogen         | $N₂$            | 0.02                             | 0.0127                           | Inert ballast in the fuel stream                     |
| Carbon dioxide   | $CO₂$           | 0.01                             | 0.00405                          | Inert (already fully oxidised)                       |
| Water vapour     | $H₂O$           | 0.01                             | 0.00990                          | Moisture carried with the fuel                       |

The mass fractions sum to 1.0 by definition. The mole fractions $\mathrm{x_i}$ are obtained from

$$
x_i \;=\; \frac{\dfrac{w_i}{M_i}}{\sum_j \dfrac{w_j}{M_j}}
$$

where $\mathrm{M_i}$ is the molar mass of species $i$ from `molar_masses` in `common/constants.py`. The resulting fuel mixture is therefore predominantly methane with small amounts of heavier hydrocarbons and trace inert/contaminant species, representative of a typical processed natural gas for boiler firing.

## Stoichiometric $\mathrm{O_2}$ requirement

Evaluate the stoichiometric oxygen requirement via the function `stoich_O2_required_per_mol_fuel(fuel)` in `combustion/flue.py`. The algorithm is:

1. Use per–mole-of-species stoichiometric $\mathrm{O_2}$ factors $\nu_{\mathrm{O_2},i}$ from `O2_per_mol` in `common/constants.py`:

   | Species            | Global reaction (complete combustion)     | $\nu_{\mathrm{O_2},i}$ [mol $O₂$ / mol species] |
   | ------------------ | ----------------------------------------- | ----------------------------------------------- |
   | $CH₄$              | $CH₄$ + 2 $O₂$ → $CO₂$ + 2 $H₂O$          | 2.0                                             |
   | $C₂H₆$             | $C₂H₆$ + 3.5 $O₂$ → 2 $CO₂$ + 3 $H₂O$     | 3.5                                             |
   | $C₃H₈$             | $C₃H₈$ + 5 $O₂$ → 3 $CO₂$ + 4 $H₂O$       | 5.0                                             |
   | $C₄H₁₀$            | $C₄H₁₀$ + 6.5 $O₂$ → 4 $CO₂$ + 5 $H₂O$    | 6.5                                             |
   | $H₂S$              | $H₂S$ + 1 $O₂$ → $SO₂$ + $H₂O$            | 1.0                                             |
   | $N₂$, $CO₂$, $H₂O$ | Inert/fully oxidised → no additional $O₂$ | 0.0                                             |

2. Compute the stoichiometric $O₂$ requirement per mole of fuel mixture as
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
- remaining species: $x_{\mathrm{N_2}}, x_{\mathrm{CO_2}}, x_{\mathrm{H_2O}}$ are inert in the stoichiometric balance.

Hence

$$
\begin{aligned}
\nu_{\mathrm{O_2,stoich}}
&= 0.8895 \cdot 2.0
 + 0.0593 \cdot 3.5
 + 0.0162 \cdot 5.0
 + 0.00307 \cdot 6.5
 + 0.00523 \cdot 1.0 \\[3pt]
&\approx 2.09 \;\;\text{mol $O₂$ per mol fuel mixture}
\end{aligned}
$$

This is exactly what `stoich_O2_required_per_mol_fuel` returns:

```python
def stoich_O2_required_per_mol_fuel(fuel: GasStream) -> Q_:
    fuel_x = to_mole(fuel.comp)
    total = sum(fuel_x[k] * O2_per_mol.get(k, 0.0) for k in fuel_x)
    return Q_(total, "dimensionless")
```

For later hydraulic and performance interpretation, it is also useful to express this on a mass basis.  
For 1 kg of fuel, the total fuel moles are

$$
n_{\text{fuel,total}} = \sum_i \frac{w_i}{M_i} \approx 56.1 \;\text{mol fuel/kg}
$$

Thus the stoichiometric $O₂$ requirement per unit fuel mass is

$$
n_{\mathrm{O_2,stoich}}^{(m)}
= \nu_{\mathrm{O_2,stoich}} \, n_{\text{fuel,total}}
\approx 2.09 \times 56.1 \approx 1.17\times 10^2\;\text{mol $O₂$/kg fuel}
$$

Converting to mass of $O₂$ per kg of fuel:

$$
\dot{m}_{\mathrm{O_2,stoich}}
= n_{\mathrm{O_2,stoich}}^{(m)} M_{\mathrm{O_2}}
\approx 117.3 \,\text{mol/kg} \times 0.031998 \,\text{kg/mol}
\approx 3.75 \,\text{kg $O₂$/kg fuel}
$$

So, for this fuel:

- Stoichiometric oxygen requirement:  
  $\boxed{\nu_{\mathrm{O_2,stoich}} \approx 2.09 \text{ mol $O₂$ per mol fuel mixture}}$
- Equivalent mass requirement:  
  $\boxed{\dot{m}_{\mathrm{O_2,stoich}} \approx 3.75 \text{ kg $O₂$ per kg fuel}}$

## Air–fuel ratio and excess air $λ$

The simulation specifies an excess‐air ratio

$$
\lambda = 1.1
$$

in `config/operation.yaml`. This value enters the calculation through  
`air_flow_rates(air, fuel, excess)` in `combustion/flue.py`.

---

### Stoichiometric $\mathrm{O_2}$ requirement (per mole of fuel mixture)

From Section 4.2:

$$
\nu_{\mathrm{O_2,stoich}} = 2.09 \;\text{mol $O₂$/mol fuel}
$$

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
  n_{\text{fuel,total}} \approx 56.1\;\text{mol/kg}
  $$

- Therefore the total molar fuel flow:
  $$
  \dot{n}_f = 56.1 \times 0.5 \approx 28.05\;\text{mol/s}
  $$

Hence the stoichiometric and actual $O₂$ flows are:

$$
\dot{n}_{\mathrm{O_2,stoich}} = 2.09 \times 28.05 = 58.7\;\text{mol/s}
$$

$$
\dot{n}_{\mathrm{O_2,actual}} = 1.1 \times 58.7 = 64.6\;\text{mol/s}
$$

---

### Air required

Air $O₂$ mole fraction (from `air.yaml`):

$$
x_{\mathrm{O_2,air}} = 0.2095
$$

Thus:

$$
\dot{n}_{\text{air}}
= \frac{\dot{n}_{\mathrm{O_2,actual}}}{x_{\mathrm{O_2,air}}}
= \frac{64.6}{0.2095}
\approx 308\;\text{mol/s}
$$

The air molar mass (mixture weighted) is:

$$
M_{\text{air}} \approx 0.02897\;\text{kg/mol}
$$

Therefore the mass-based air flow rate:

$$
\dot{m}_{\text{air}}
= \dot{n}_{\text{air}} M_{\text{air}}
\approx 308 \times 0.02897
\approx 8.93\;\text{kg/s}
$$

---

### Air–fuel ratio

Mass-based air–fuel ratio:

$$
\text{AFR} = \frac{\dot{m}_{\text{air}}}{\dot{m}_f}
= \frac{8.93}{0.5}
\approx 17.9
$$

---

## Lower heating value (LHV) and heat release

The fuel lower and higher heating values, and the corresponding firing rate, are evaluated in
`combustion/heat.py` by the function `compute_LHV_HHV(fuel)` and then used by
`total_input_heat(fuel, air)`.

---

### Method

#### Latent heat of water

Obtain the latent heat of vaporisation of water at the reference pressure
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

| Species  | $\Delta h^\circ_\mathrm{f}$ [kJ/mol] |
| -------- | ------------------------------------ |
| $CH₄$    | −74.8                                |
| $C₂H₆$   | −84.7                                |
| $C₃H₈$   | −103.8                               |
| $C₄H₁₀$  | −126.1                               |
| $SO₂$    | −296.8                               |
| $CO₂$    | −393.5                               |
| $H₂O(l)$ | −285.5                               |

#### Products for HHV and LHV

For each fuel species, complete combustion is considered:

- $CH₄$ + 2 $O₂$ → $CO₂$ + 2 $H₂O$
- $C₂H₆$ + 3.5 $O₂$ → 2 $CO₂$ + 3 $H₂O$

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

---

### Numerical results for the present fuel

For the fuel specified above, the mixture heating values are:

- Higher heating value (HHV, mass-based):
  $$
  \mathrm{HHV}_\mathrm{mix} \approx 52\,\text{MJ/kg}
  $$
- Lower heating value (LHV, mass-based):
  $$
  \mathrm{LHV}_\mathrm{mix} \approx 47\,\text{MJ/kg}
  $$

For the specified fuel mass flow rate:

$$
\dot{m}_f = 0.5\ \text{kg/s}
$$

the resulting firing rates are:

- On an HHV basis:

  $$
  P_\mathrm{HHV} = \dot{m}_f \,\mathrm{HHV}_\mathrm{mix}
  \approx 0.5 \times 52\ \text{MJ/s}
  \approx 26\ \text{MW}
  $$

- On an LHV basis (used consistently in the simulation):
  $$
  P_\mathrm{LHV} = \dot{m}_f \,\mathrm{LHV}_\mathrm{mix}
  \approx 0.5 \times 47\ \text{MJ/s}
  \approx 23.6\ \text{MW}
  $$

These correspond directly to `P_HHV` and `P_LHV` returned by `compute_LHV_HHV`.

---

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
  P_\mathrm{LHV} \approx 23.6\ \text{MW}
  $$

- Total heat input including sensible:
  $$
  Q_\text{in} \approx P_\mathrm{LHV} + Q_{\text{sens,fuel}} + Q_{\text{sens,air}}
  \approx 23.6\ \text{MW} \quad (\text{increase } < 0.1\%)
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

---

### Thermodynamic formulation

Let the fuel and air streams be characterised by:

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

---

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

6. Initialise the mixture and perform HP equilibrium:

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

---

### Numerical result for the present case

For the given conditions:

- Fuel: natural-gas–type mixture from Section 4.1,  
  $\dot{m}_\mathrm{fuel} = 0.5\ \mathrm{kg/s}$, $T_\mathrm{fuel} = 300\ \mathrm{K}$, 1.013×10⁵ Pa.
- Air: dry air at 300 K and 1.013×10⁵ Pa, composition from `config/air.yaml`.
- Excess air: $\lambda = 1.1$ (10 % excess air).

the HP-equilibrium calculation yields an adiabatic flame temperature on the order of:

$$
T_\mathrm{ad} \;\approx\; 2{,}050\ \mathrm{K}
\quad (\approx 1{,}780^\circ\mathrm{C})
$$

This value is consistent with typical adiabatic flame temperatures for natural gas with
around 10 % excess air and confirms that the combustion zone (furnace) operates at very high gas temperatures, driving strong radiative and convective heat transfer to the
shell-side water/steam.

The scalar `T_ad` is passed forward and written into the boiler summary CSV
(`*_boiler_summary.csv`) for reference and later comparison with non-adiabatic stack
temperatures obtained from the full boiler simulation.

## Flue-gas composition at adiabatic conditions

After equilibrium is solved in `adiabatic_flame_T`, the model constructs the full equilibrium flue-gas composition. This composition is used only for reporting (via `CombustionResult`)
and is not the same composition used in the heat-exchanger network (the boiler heat-transfer
model uses _non-equilibrium, fully burnt_ flue gas based on pure stoichiometry and excess air).

---

### Species included

The mechanism `config/flue_cantera.yaml` defines the set of gaseous species for equilibrium.
Typical species present after equilibrium include:

- Major products:

  - CO₂
  - H₂O
  - N₂
  - O₂ (from excess air)

- Minor equilibrium species:
  - CO
  - H₂
  - OH
  - O
  - NO
  - NO₂
  - SO₂ (from fuel H₂S)

Because chemical equilibrium is enforced, small fractions of dissociation products appear at
high temperature (CO, H₂, radicals, NOₓ). These are automatically included in `gas_mix.Y`.

---

### Procedure

Once the HP equilibrium is complete:

```python
Y_eq = gas_mix.Y
species = gas_mix.species_names

comp_eq = {
    sp: Q_(float(Y_eq[i]), "")
    for i, sp in enumerate(species)
    if Y_eq[i] > 1e-15
}
```

This produces a dictionary of mass fractions for all species above a cut-off. These form:

```python
flue = GasStream(
    mass_flow = Q_(m_tot, "kg/s"),
    T         = Q_(gas_mix.T, "K"),
    P         = air.P,
    comp      = comp_eq,
)
```

This `flue` object is stored inside the `CombustionResult`.

---

### Representative equilibrium composition for the present case

For the fuel and air conditions of Sections 4.1–4.3 and λ = 1.1, an HP-equilibrium calculation
at $T_\mathrm{ad} \approx 2050\ \mathrm{K}$ typically yields approximate mass fractions:

- CO₂: 0.085–0.095
- H₂O: 0.075–0.085
- O₂: 0.020–0.030 (excess)
- N₂: 0.78–0.80
- CO: ~10⁻³
- H₂: ~10⁻⁴
- NO: ~10⁻⁴–10⁻⁵
- OH, O, radicals: < 10⁻⁶ each
- SO₂: ~10⁻⁴ (proportional to fuel H₂S)

The exact values depend on the mechanism and equilibrium temperature. The values above are
consistent with:

- natural-gas combustion,
- slight dissociation at ~2000 K,
- 10 % excess air,
- trace sulfur combustion.

---

### Distinction between equilibrium flue gas and boiler flue gas

The equilibrium flue gas calculated here is not used for heat-exchanger calculations.

Instead:

- Equilibrium flue gas is used only to compute the adiabatic flame temperature and for
  diagnostic output in the summary CSV.
- The boiler thermal model assumes complete combustion with no dissociation at the actual
  furnace and convection-pass temperatures. For all heat-transfer and pressure-drop
  calculations:
  - product species CO₂, H₂O, SO₂,
  - unreacted O₂ (from λ),
  - N₂ from air and fuel,
    with no radicals or dissociation species.

Thus, equilibrium chemistry is isolated to the flame-temperature calculation.

---

### Output fields

The following entries in `CombustionResult` originate from this section:

| Field     | Meaning                                                 |
| --------- | ------------------------------------------------------- |
| `flue_ad` | `GasStream` of equilibrium flue gas (T, P, composition) |
| `T_ad`    | Adiabatic flame temperature                             |
| `comp_ad` | Equilibrium mass fractions written to the CSV           |

This completes all combustion chemistry inputs passed to the boiler model.

## Combustion summary

In the implementation, all values are derived from the configuration files in `config/` and from the combustion routines in `combustion/*.py` (`compute_LHV_HHV`, `total_input_heat`, `air_flow_rates`, `adiabatic_flame_T`), these quantities are wrapped in a `CombustionResult` dataclass (`common/results.py`):

```python
@dataclass(frozen=True)
class CombustionResult:
    LHV: Q_          # LHV-based firing power [kW]
    Q_in: Q_         # total heat input (LHV + sensible) [kW]
    T_ad: Q_         # adiabatic flame temperature [K]
    flue: GasStream  # flue-gas stream at adiabatic conditions
    fuel_LHV_mass: Q_ | None = None  # LHV_mix [kJ/kg]
    fuel_P_LHV:   Q_ | None = None   # P_LHV [kW]
```

This object is created in `Combustor.run()` and passed to the boiler solver:

- to define the total available heat $Q_\mathrm{in}$,
- to initialise the flue-gas stream entering the first heat-transfer stage (HX_1),
- and to provide diagnostic quantities (LHV, $T_\mathrm{ad}$) for the boiler performance
  summary.
