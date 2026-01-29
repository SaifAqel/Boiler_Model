---
title: "Heat Transfer and Fluid Flow Calculations of Industrial Shell Boilers and Evaluation of Operation Conditions"
author: "Saif-Aldain Aqel"
theme: default
aspectratio: 169
header-includes:
  - \usepackage{beamerthemeBME}
  - \usepackage{booktabs}
  - \usepackage{siunitx}
  - \usepackage{microtype}
  - \usepackage{graphicx}
  - \setkeys{Gin}{width=\linewidth,height=0.85\textheight,keepaspectratio}
---

## Agenda

- Problem & objectives
- Boiler configuration (HX1–HX6)
- Modeling framework (combustion, heat transfer, hydraulics)
- Sanity checks / validation posture
- Key results: control case + parametric trends
- Conclusions, limitations

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

## Boiler configuration: three-pass + economizer (HX1–HX6)

- Gas-side stages (sequential):
  - **HX1** furnace → **HX2** reversal → **HX3** tube-bank → **HX4** reversal → **HX5** tube-bank → **HX6** economizer → stack
- Water/steam side:
  - HX1–HX5: **pool boiling at drum saturation**
  - HX6: **single-phase feedwater heating**

## Shell boiler labeled stages

\begin{center}
\includegraphics{Thesis/figures/boiler_stages.jpg}
\end{center}

## Boiler geometry context (cross-section)

- Drum: ~4.5 m ID, ~5 m length (modeled as saturated reservoir)
- Stages use geometry from `config/stages.yaml` (diameters, lengths, tube counts)
- Includes wall conduction + fouling layers in the thermal resistance network

## Boiler cross section

\begin{center}
\includegraphics{Thesis/figures/boiler_cross_section.jpg}
\end{center}

## Model architecture (Python framework)

- Inputs (YAML):
  - fuel composition + $\dot m_\mathrm{fuel}$, excess air $\lambda$, drum pressure
  - stage geometries + loss coefficients + fouling factor
- Main modules:
  - **Combustion** (Cantera): $T_\mathrm{ad}$, flue-gas $c_p,\mu,k$, composition, $Q_\mathrm{in}$
  - **HX solver**: 1D marching, resistance network, radiation+convection
  - **Hydraulics**: stage-wise $\Delta P$ with correlations + minor losses
  - **Postproc**: boiler KPIs + stage summaries

## Combustion flow

\begin{center}
\includegraphics{Thesis/figures/combustion_flow.pdf}
\end{center}

## Heat-transfer model: 1D marching + resistance network

- Counter-current, stage-wise 1D marching in $x$:
  - $q'(x)=UA'(x)\,[T_g(x)-T_w(x)]$
  - update $h_g,h_w$ via $\Delta h_g=-Q/\dot m_g$, $\Delta h_w=+Q/\dot m_w$
- Overall conductance per length from series resistances:
  - gas convection + **gas radiation** + fouling + wall + water-side HTC
- Regimes:
  - gas: internal convection (HX1–HX5), crossflow bank (HX6)
  - water: pool boiling (HX1–HX5), single-phase internal flow (HX6)

## Heat transfer resistance network

\begin{center}
\includegraphics{Thesis/figures/heat_step.png}
\end{center}

## Gas/water properties + radiation handling

- Gas properties: **Cantera** mixture at local $T,P$ ( $c_p,\mu,k,\rho$ )
- Water/steam properties: **IAPWS-IF97** (saturation $T_\mathrm{sat}(P)$, $h_f,h_g$, single-phase liquid props)
- Radiation model (gray-gas bands):
  - participating media $CO_2/H_2O$, banded emissivity $\varepsilon_g(T,p_i,L_b)$
  - linearized: $h*{g,\mathrm{rad}}=4\sigma F \varepsilon_g T*\mathrm{film}^3$

## Gas path through stages

\begin{center}
\includegraphics{Thesis/figures/gas_path.png}
\end{center}

## Hydraulics: pressure-drop model and coupling

- Per-step decomposition:
  - friction: $\Delta P\_\mathrm{fric}=-f\frac{\Delta x}{D_h}\left(\rho V^2/2\right)$
  - minor losses: $\Delta P\_\mathrm{minor}=-K(\rho V^2/2)$
- Friction factor:
  - laminar $64/\mathrm{Re}$, turbulent **Colebrook–White** (seeded by Swamee–Jain)
- Economizer gas side: **tube-bank bundle loss** (drag-based), distributed along $L$
- Coupled update: $P_{i+1}=P_i+\Delta P_\mathrm{total}$ → affects $\rho,\mu$, $V$, Re, HTCs

## Sanity checks / validation posture (no dedicated experiment)

- Numerical consistency:
  - converged outer loop on $\eta$ and $\dot m_w$ (fixed-point iteration)
  - global energy balance error ~ 0 (control case table)
- Physical plausibility:
  - stack temperature and efficiency in expected industrial ranges for gas-fired fire-tube + economizer
  - monotonic gas temperature drop HX1 → HX6; duties highest upstream
- Stage-wise trends:
  - radiation fraction highest in HX1; convection more important downstream

## Stage-wise heat transfer and hydraulics (control)

\begin{center}
\includegraphics{results/plots/per_run/stages_control_combined_8plots.png}
\end{center}

## Control case: key performance numbers (reference point)

- Operating point:
  - $\dot m_\mathrm{fuel}=0.1$ kg/s, $\lambda=1.05$, $P_\mathrm{drum}=10$ bar, fouling factor $f=1$
- Control-case KPI label:
  - **$\eta \approx 0.95$ (LHV)**, $Q_\mathrm{useful}\approx 4.42$ MW, $Q_\mathrm{in}\approx 4.68$ MW
  - **Steam $\approx$ 6.81 t/h**, $T_\mathrm{stack}\approx 152^\circ$C
  - **$\Delta P_\mathrm{gas}\approx 12.45$ kPa** (economizer dominates)
- Heat-transfer distribution (stage totals, MW):
  - HX1: **2.86** (mostly radiative), HX3: **1.06**, HX6: **0.14**

## Parametric trends (main findings)

- Excess air $\lambda$:
  - **shallow efficiency optimum near $\lambda \approx 1.05$**
  - higher $\lambda$ → higher flue mass flow → higher stack losses and $\Delta P$
- Drum pressure:
  - pressure changes shift **steam quantity more than efficiency**
  - higher $P$ → higher $T_\mathrm{sat}$ → reduced driving $\Delta T$ → higher $T_\mathrm{stack}$
- Firing rate ($\dot m_\mathrm{fuel}$):
  - duties and steam rate scale **approximately linearly** over practical load range
- Fouling:
  - reduces downstream convective recovery → **raises $T_\mathrm{stack}$** and slightly lowers $\eta$

## KPI overview across parameter groups

\begin{center}
\includegraphics{results/plots/per_run/kpi_overview_all_param_groups.png}
\end{center}

## Conclusions & limitations

- Built a coupled framework:
  - 3-pass shell boiler as **6 sequential gas-side stages**
  - combustion + heat-transfer + hydraulics
- Model reproduces physically consistent behavior:
  - realistic control case: $\eta\sim 0.95$ (LHV), $T_\mathrm{stack}\sim 152^\circ$C, $\Delta P_g\sim 12.5$ kPa
  - correct directional sensitivities for $\lambda$, $P$, firing rate, fouling
- Main limitations (scope choices):
  - steady-state 1D
  - pool-boiling treated via correlation at saturation; no detailed circulation/separation

## Questions

- Thank you.
