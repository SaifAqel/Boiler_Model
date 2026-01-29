---
title: "Heat Transfer and Fluid Flow Calculations of Industrial Shell Boilers and Evaluation of Operation Conditions"
author: "Saif-Aldain Aqel"
---

## Agenda

- Problem & objectives
- Boiler configuration (HX1–HX6)
- Modeling framework (combustion, heat transfer, hydraulics)
- Sanity checks / validation posture
- Key results: control case + parametric trends
- Conclusions, limitations

::: notes
Today I’ll present a physics-based model of a three-pass fire-tube shell boiler implemented in Python.
I’ll start with why this is a coupled problem and what the thesis tries to achieve, then introduce the six-stage boiler representation.
After that, I’ll walk through the modeling architecture—combustion, the 1D heat-transfer solver, and hydraulics—and how they couple.
Because there is no dedicated experimental campaign in the thesis, I’ll frame validation as consistency checks and comparisons to expected industrial ranges.
Then I’ll summarize the control case with the key performance numbers and finish with the main parametric trends for excess air, pressure, firing rate, and fouling.
Finally I’ll close with conclusions and limitations, and then questions.
Transition: first, what problem are we solving and why do we need this structure?
:::

---

## Motivation & problem statement

- Industrial shell boilers are common (6–25 bar, ~0.5–20 t/h typical)
- Performance is set by **coupled physics**:
  - combustion → flue-gas properties & heat input
  - multi-stage convection + radiation
  - geometry-driven pressure losses
- Need a **fast, physics-based tool** for:
  - efficiency/stack temperature prediction
  - steam capacity under varying operation
  - sensitivity to key parameters ($\lambda$, pressure, firing rate, fouling)

::: notes
Shell boilers look simple, but their behavior depends on several tightly coupled processes.
Combustion sets the available heat input, the flue-gas composition, and the temperature level entering the furnace.
Heat transfer is distributed across multiple regions—radiation-dominated upstream and more convection-dominated downstream—so a single lumped UA is not very explanatory.
At the same time, hydraulics matters because pressure losses and velocities change local heat transfer and impact operability, especially in the economizer crossflow.
So the thesis goal is a practical, physics-based model that is detailed enough to capture these couplings, but still computationally efficient for parametric sweeps and engineering use.
Transition: with that in mind, here is the specific boiler layout I model.
:::

---

## Boiler configuration: three-pass + economizer (HX1–HX6)

- Gas-side stages (sequential):
  - **HX1** furnace → **HX2** reversal → **HX3** tube bank
  - **HX4** reversal → **HX5** tube bank → **HX6** economizer → stack
- Water/steam side:
  - HX1–HX5: **pool boiling at drum saturation**
  - HX6: **single-phase feedwater heating**
- What to look at: **stage boundaries** and where the economizer sits downstream

## Shell boiler labeled stages

![Shell boiler labeled stages](Thesis/figures/boiler_stages.jpg){ width=92% }

::: notes
This model represents the boiler as six sequential gas-side stages.
HX1 is the furnace tube where the hottest gas enters; HX2 and HX4 are the reversal chambers; HX3 and HX5 are the convective tube banks inside the shell.
HX6 is the economizer located downstream, recovering remaining sensible heat to preheat feedwater.
On the water side, the pressure-part surfaces are treated as pool-boiling surfaces at the drum saturation temperature, while the economizer is treated as a single-phase internal flow.
The key point is that each stage has distinct geometry, heat-transfer regime, and hydraulics—so stage resolution is important for explaining trends.
Transition: next I’ll briefly show the physical geometry context used for these stages.
:::

---

## Boiler geometry context (cross-section)

- Drum: ~4.5 m ID, ~5 m length (modeled as saturated reservoir)
- Stages use geometry from `config/stages.yaml` (diameters, lengths, tube counts)
- Includes wall conduction + fouling layers in the thermal resistance network
- What to look at: **furnace tube + tube banks + reversal chambers** locations

## Boiler cross section

![Boiler cross section](Thesis/figures/boiler_cross_section.jpg){ width=90% }

::: notes
This cross-section provides the physical context for the stage model.
The drum is modeled as a single saturated reservoir at the operating pressure, supplying saturation temperature for pool boiling on the pressure parts.
Each stage’s geometry—diameter, length, tube count, pitches for tube banks, and the economizer shell diameter—comes from the configuration file.
Thermally, the model includes convection on both sides, wall conduction, and fouling resistances, which becomes important for the fouling study later.
Transition: with the hardware defined, I’ll show how the code is structured to model combustion, heat transfer, and hydraulics together.
:::

---

## Model architecture (Python framework)

- Inputs (YAML):
  - fuel composition + $\dot m\_\mathrm{fuel}$, excess air $\lambda$, drum pressure
  - stage geometries + loss coefficients + fouling factor
- Main modules:
  - **Combustion** (Cantera): $T*\mathrm{ad}$, flue-gas $c_p,\mu,k$, composition, $Q*\mathrm{in}$
  - **HX solver**: 1D marching, resistance network, radiation+convection
  - **Hydraulics**: stage-wise $\Delta P$ with correlations + minor losses
  - **Postproc**: boiler KPIs + stage summaries

## Combustion flow

![Combustion flow](Thesis/figures/combustion_flow.pdf){ width=78% }

::: notes
At a high level, the user specifies operation and geometry in YAML: fuel, air, excess air ratio, pressure, and stage parameters.
The combustion module uses Cantera to compute the adiabatic flame temperature and an associated burnt flue-gas stream used for properties throughout the boiler model.
Then the heat-exchanger solver marches along the gas path through HX1 to HX6, computing local heat transfer using a full resistance network, and updating temperatures and properties step-by-step.
In parallel, the hydraulics model computes pressure losses from friction and minor losses—plus a dedicated bundle-loss formulation for economizer crossflow.
Finally, postprocessing exports boiler-level KPIs and stage summaries used for the results figures and tables.
Transition: next I’ll zoom into the core of the method—the 1D marching solver and the resistance network.
:::

---

## Heat-transfer model: 1D marching + resistance network

- Counter-current, stage-wise 1D marching in $x$:
  - $q'(x)=UA'(x)\,[T_g(x)-T_w(x)]$
  - update $h_g,h_w$ via $\Delta h_g=-Q/\dot m_g$, $\Delta h_w=+Q/\dot m_w$
- Overall conductance per length from series resistances:
  - gas convection + **gas radiation** + fouling + wall + water-side HTC
- Regimes:
  - gas: internal convection (HX1–HX5), crossflow bank (HX6)
  - water: pool boiling (HX1–HX5), single-phase internal flow (HX6)
- What to look at: the **series resistance path** gas → wall → water

## Heat transfer resistance network

![Heat transfer resistance network](Thesis/figures/heat_step.png){ width=92% }

::: notes
The heat-transfer backbone is a one-dimensional marching solver applied stage by stage along the gas flow direction.
At each step, the model computes the local overall conductance per unit length from a series resistance network: gas-side convection and radiation contributions, gas-side fouling, wall conduction, water-side fouling, and water-side convection or boiling HTC.
Given UA’ and the local temperature difference, it computes the local heat flux and then updates gas and water enthalpies over the step.
On the gas side, HX1–HX5 are treated as internal flow; the economizer is crossflow over a tube bank.
On the water side, the pressure parts are treated as pool boiling at saturation, and the economizer is treated as single-phase internal flow.
Transition: now I’ll highlight how radiation and property models are handled, since they are key upstream.
:::

---

## Gas/water properties + radiation handling

- Gas properties: **Cantera** mixture at local $T,P$ ( $c_p,\mu,k,\rho$ )
- Water/steam properties: **IAPWS-IF97** (saturation $T\_\mathrm{sat}(P)$, $h_f,h_g$, single-phase liquid props)
- Radiation model (gray-gas bands):
  - participating media $CO_2/H_2O$, banded emissivity $\varepsilon_g(T,p_i,L_b)$
  - linearized: $h*{g,\mathrm{rad}}=4\sigma F \varepsilon_g T*\mathrm{film}^3$
- What to look at: upstream stages are **radiation-dominated**, downstream mostly convection

## Gas path through stages

![Gas path through stages](Thesis/figures/gas_path.png){ width=88% }

::: notes
Two property libraries drive the “physics-based” part of the model.
On the gas side, Cantera provides temperature- and composition-dependent properties, which matter because the gas cools from very high furnace temperatures down to the stack.
On the water side, IAPWS-IF97 provides saturation properties and enthalpies needed for steam generation and for the economizer liquid heating.
For radiation, the furnace and high-temperature regions include a gray-gas band model for CO2 and H2O, producing an effective emissivity and then a linearized radiative HTC.
The key qualitative outcome is that early stages—especially HX1—have a large radiative share, while later stages are more convection-limited.
Transition: next I’ll describe the hydraulics model and how pressure drop is computed alongside the energy balance.
:::

---

## Hydraulics: pressure-drop model and coupling

- Per-step decomposition:
  - friction: $\Delta P\_\mathrm{fric}=-f\frac{\Delta x}{D_h}\left(\rho V^2/2\right)$
  - minor losses: $\Delta P\_\mathrm{minor}=-K(\rho V^2/2)$
- Friction factor:
  - laminar $64/\mathrm{Re}$, turbulent **Colebrook–White** (seeded by Swamee–Jain)
- Economizer gas side: **tube-bank bundle loss** (drag-based), distributed along $L$
- Coupled update: $P*{i+1}=P_i+\Delta P*\mathrm{total}$ → affects $\rho,\mu$, $V$, Re, HTCs

::: notes
Hydraulics is solved concurrently with heat transfer using standard one-dimensional pressure-drop relationships.
For internal-flow stages, pressure losses are modeled as frictional Darcy–Weisbach plus minor losses from area changes and bends, using stage-specific K values.
The friction factor is computed based on Reynolds number and roughness, with Colebrook–White for turbulent flow.
The economizer is different: gas flows across a tube bank, so the model uses a bundle-loss coefficient formulation rather than a wall-friction model.
Importantly, pressure is marched stepwise in the same loop, so changes in pressure affect density and viscosity, which then affects velocities, Reynolds number, and both heat transfer and pressure loss.
Transition: since there is no experimental campaign, I’ll summarize how I check the model for physical consistency.
:::

---

## Sanity checks / validation posture (no dedicated experiment)

- Numerical consistency:
  - converged outer loop on $\eta$ and $\dot m_w$ (fixed-point iteration)
  - global energy balance error ~ 0 (control case table)
- Physical plausibility:
  - stack temperature and efficiency in expected industrial ranges for gas-fired fire-tube + economizer
  - monotonic gas temperature drop HX1 → HX6; duties highest upstream
- Stage-wise trends:
  - radiation fraction highest in HX1; convection more important downstream
- What to look at: stage-wise profiles are smooth and ordered across stages

## Stage-wise heat transfer and hydraulics (control)

![Stage-wise heat transfer and hydraulics (control)](results/plots/per_run/stages_control_combined_8plots.png){ width=92% }

::: notes
Because the thesis does not include a matched experimental dataset for this exact boiler, validation is framed as consistency and plausibility checks.
First, the solver has an outer iteration that converges efficiency and water mass flow so that combustion input and absorbed duty are consistent; convergence is based on water mass-flow change.
Second, the energy balance closes: in the control case, the reported balance error is essentially zero, indicating the marching and integration are consistent.
Third, results are compared qualitatively to expected ranges for gas-fired fire-tube boilers with economizers—efficiencies in the mid-90% on an LHV basis and stack temperatures on the order of ~150°C are plausible.
Finally, stage-wise results show physically consistent ordering: temperatures fall monotonically, and upstream stages dominate duty with radiation playing a large role early.
Transition: with those checks established, I’ll present the headline control-case numbers.
:::

---

## Control case: key performance numbers (reference point)

- Operating point:
  - $\dot m*\mathrm{fuel}=0.1$ kg/s, $\lambda=1.05$, $P*\mathrm{drum}=10$ bar, fouling factor $f=1$
- Control-case KPI label:
  - **$\eta \approx 0.95$ (LHV)**, $Q*\mathrm{useful}\approx 4.42$ MW, $Q*\mathrm{in}\approx 4.68$ MW
  - **Steam $\approx$ 6.81 t/h**, $T\_\mathrm{stack}\approx 152^\circ$C
  - **$\Delta P\_\mathrm{gas}\approx 12.45$ kPa** (economizer dominates)
- Heat-transfer distribution (stage totals, MW):
  - HX1: **2.86** (mostly radiative), HX3: **1.06**, HX6: **0.14**

::: notes
This slide is the main numerical summary of the control case, which is the baseline for all parametric studies.
At the nominal operating point—fuel flow 0.1 kg/s, excess air 1.05, drum pressure 10 bar—the model predicts about 4.68 MW of heat input on an LHV basis and about 4.42 MW useful heat transfer.
That corresponds to roughly 95% direct and indirect efficiency on an LHV basis.
Steam capacity is about 6.81 tons per hour, and the stack temperature is about 152 degrees C.
On hydraulics, the total gas-side pressure drop is about 12.45 kPa, and the stage table shows this is dominated by the economizer section.
Stage-wise duties show that HX1 contributes the largest share and is radiation-heavy, while the economizer recovers a smaller but important amount downstream.
Transition: next I’ll summarize the parameter trends—the main “so what” outcomes from the sweeps.
:::

---

## Parametric trends (main findings)

- Excess air $\lambda$:
  - **shallow efficiency optimum near $\lambda \approx 1.05$**
  - higher $\lambda$ → higher flue mass flow → higher stack losses and $\Delta P$
- Drum pressure:
  - pressure changes shift **steam quantity more than efficiency**
  - higher $P$ → higher $T*\mathrm{sat}$ → reduced driving $\Delta T$ → higher $T*\mathrm{stack}$
- Firing rate ($\dot m\_\mathrm{fuel}$):
  - duties and steam rate scale **approximately linearly** over practical load range
- Fouling:
  - reduces downstream convective recovery → **raises $T\_\mathrm{stack}$** and slightly lowers $\eta$

## KPI overview across parameter groups

![KPI overview across parameter groups](results/plots/per_run/kpi_overview_all_param_groups.png){ width=92% }

::: notes
This slide summarizes the most important trends across all parametric runs.
First, efficiency versus excess air shows a shallow maximum near the design value of about lambda 1.05.
As lambda increases beyond that, additional air increases flue-gas mass flow and sensible losses, so stack temperature and pressure drop rise without improving useful recovery.
Second, drum pressure mainly affects steam generation characteristics through latent heat and saturation temperature—so the effect is stronger on steam quantity and stack temperature than on overall efficiency.
Third, varying fuel flow primarily scales the entire system: heat duties and steam rate increase approximately linearly across the investigated range, indicating available surface is sufficient in that operating window.
Finally, fouling degrades heat transfer, especially in downstream convective sections where temperature driving forces are already smaller, which raises stack temperature and reduces efficiency modestly.
Transition: I’ll close with the key conclusions and limitations of the framework.
:::

---

## Conclusions & limitations

- Built a coupled framework:
  - 3-pass shell boiler as **6 sequential gas-side stages**
  - combustion (Cantera) + HT (resistance network + gray-gas radiation) + hydraulics
- Model reproduces physically consistent behavior:
  - realistic control case: $\eta\sim 0.95$ (LHV), $T\_\mathrm{stack}\sim 152^\circ$C, $\Delta P_g\sim 12.5$ kPa
  - correct directional sensitivities for $\lambda$, $P$, firing rate, fouling
- Main limitations (scope choices):
  - steady-state 1D; simplified radiation (gray bands, no soot)
  - pool-boiling treated via correlation at saturation; no detailed circulation/separation
  - validation is consistency/range-based (no matched experiment)

::: notes
To conclude, the thesis delivers a physics-based boiler model that couples combustion, multi-stage heat transfer, and hydraulics in one computational tool.
The boiler is represented as six sequential gas-side stages, solved with a one-dimensional marching approach using a full resistance network and a gray-gas radiation model for CO2 and H2O.
The control case lands in a plausible industrial range, and the parametric sweeps show physically consistent sensitivities: a shallow efficiency optimum near design excess air, pressure affecting steam generation more than efficiency, firing rate scaling duties roughly linearly, and fouling degrading downstream recovery and raising stack temperature.
The main limitations are the steady-state 1D nature, simplified radiation assumptions, simplified treatment of boiling and internal drum phenomena, and the fact that validation is based on checks and expected ranges rather than a dedicated experimental dataset.
Transition: that’s the end of the prepared material—happy to take questions.
:::

---

## Questions

- Thank you.

::: notes
I’ll stop here. I’m happy to answer questions about assumptions, correlations, the solver coupling, or the results trends.
:::
