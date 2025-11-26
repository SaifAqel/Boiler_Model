# Boiler Geometry and Configuration

The simulated unit is a three-pass fire-tube shell boiler with six distinct gas-side heat-transfer stages and a single common steam drum on the water/steam side. Hot flue gas from the burner traverses a radiative furnace, two reversal chambers, two convective tube banks, and a final economiser before leaving to the stack. The water/steam side is treated as a single circulating system coupled to all pressure parts.

## Overall layout

The gas path is represented as:

$$
\mathrm{Burner} \rightarrow \mathrm{HX_1} \rightarrow \mathrm{HX_2} \rightarrow \mathrm{HX_3}
\rightarrow \mathrm{HX_4} \rightarrow \mathrm{HX_5} \rightarrow \mathrm{HX_6} \rightarrow \mathrm{stack}
$$

with the following interpretation:

- $\mathrm{HX_1}$ – Furnace (first pass, `single_tube`)  
  Large, single furnace tube where combustion products enter directly from the burner and transfer heat mainly by radiation and high-temperature convection to the surrounding water/steam.

- $\mathrm{HX_2}$ – First reversal chamber (`reversal_chamber`)  
  Short cylindrical wet back chamber that turns the flow from the furnace outlet into the first convective tube bank (gas direction change = 180°).

- $\mathrm{HX_3}$ – First convective tube bank (second pass, `tube_bank`)  
  Bank of small diameter fire tubes arranged in a staggered pattern inside the shell; flue gas flows inside of the tubes, water/steam outside.

- $\mathrm{HX_4}$ – Second reversal chamber (`reversal_chamber`)  
  Second turning chamber redirecting gas from the first to the second tube bank.

- $\mathrm{HX_5}$ – Second convective tube bank (third pass, `tube_bank`)  
  Second fire-tube bundle, again in cross-flow, representing the last in-boiler convective pass.

- $\mathrm{HX_6}$ – Economiser (`economiser`)  
  Separate, downstream tube bank used to preheat feedwater in single-phase operation before entering the drum/boiler circuit.

Pool boiling is enabled for $\mathrm{HX_1}$–$\mathrm{HX_5}$ (pressure parts); $\mathrm{HX_6}$ is explicitly single-phase on the water side.

---

## Drum configuration

The boiler has a single horizontal steam drum described by the `Drum` object. Its inner diameter is $$D_{i,\text{drum}} = 4.5\ \text{m}$$ and its length $$L_{\text{drum}} = 5.0\ \text{m}$$.

The drum is not modelled with internal separators or circulation hardware. It simply supplies the saturated water/steam state at boiler pressure, while all circulation effects are represented by the single 1-D water/steam stream used in the heat-transfer stages.

## Consolidated geometry and surface specification

Table 3-1 summarises the principal geometric inputs used in the simulation for the drum and all six heat-transfer stages. Values are taken directly from the YAML configuration files (`drum.yaml` and `stages.yaml`).

|     Element     | Kind         | Di [m] | L [m] | N_tubes [-] | Wall t [mm] | Roughness [µm] | Pool boiling [-] |
| :-------------: | ------------ | :----: | :---: | :---------: | :---------: | :------------: | :--------------: |
| $\mathrm{DRUM}$ | drum         |  4.50  | 5.00  |      –      |      –      |      0.5       |        –         |
| $\mathrm{HX_1}$ | single_tube  |  1.40  | 5.276 |      1      |     2.9     |      0.5       |       true       |
| $\mathrm{HX_2}$ | reversal_ch. |  1.60  | 0.80  |      1      |     2.9     |      0.5       |       true       |
| $\mathrm{HX_3}$ | tube_bank    | 0.076  | 4.975 |     118     |     2.9     |      0.5       |       true       |
| $\mathrm{HX_4}$ | reversal_ch. |  1.60  | 0.80  |      1      |     2.9     |      0.5       |       true       |
| $\mathrm{HX_5}$ | tube_bank    | 0.076  | 5.620 |     100     |     2.9     |      0.5       |       true       |
| $\mathrm{HX_6}$ | economiser   | 0.076  | 7.50  |     160     |     2.5     |      0.5       |      false       |

All pressure-part stages ($\mathrm{HX_1}$–$\mathrm{HX_5}$) share the same steel wall thermal conductivity of $\mathrm{k_{wall}} = 16$ $\text{W/m/K}$. The economiser ($\mathrm{HX_6}$) is modelled with a higher wall conductivity $\mathrm{k_{wall}} = 30$ $\text{W/m/K}$ and a clean surface (zero fouling thickness) to represent a best-case heat-recovery configuration.

\newpage
