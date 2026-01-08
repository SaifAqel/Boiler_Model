# Hydraulic Model

Hydraulic behavior is extracted directly from the solver through the per step pressure drop decomposition implemented in `heat/solver.py` (`_gas_dp_components`, `pressure_drop_gas`) and accumulated at the stage level in `heat/solver.py::solve_stage`.

The model divides pressure losses into:

- Frictional losses
- Minor losses (inlet, outlet, bends, etc.)
- Total pressure drop (sum of the above)

## Frictional losses

### Gas and water sides {- .unlisted}

The per step frictional pressure drop follows a standard 1D Darcy formulation:

$$
\Delta P_{\mathrm{fric}} = - f \, \frac{\Delta x}{D_h} \left( \frac{\rho V^2}{2} \right)
$$

[@white_fluid_mechanics]

Here:

- $f$ is the Darcy friction factor,
- $D_h$ is the relevant side hydraulic diameter ($D_h=\texttt{hot\_Dh}$ for gas, $D_h=\texttt{cold\_Dh}$ for water),
- $\rho$ and $V$ are local density and velocity on the relevant side,
- $\Delta x$ is the current marching step length.

The friction factor is computed from Reynolds number and relative roughness via `_friction_factor`:

- Laminar ($\mathrm{Re} < 2300$):

  $$
  f = \frac{64}{\mathrm{Re}}
  $$

  [@white_fluid_mechanics]

- Transitional ($2300 \le \mathrm{Re} < 4000$): linear blend between laminar and turbulent values:

  $$
  f = (1 - w) f_{\mathrm{lam}} + w f_{\mathrm{turb}}, \quad
  w = \frac{\mathrm{Re} - 2300}{4000 - 2300}
  $$

  [@crane_tp410]

- Turbulent ($\mathrm{Re} \ge 4000$): Colebrook–White is solved iteratively, seeded by the Swamee–Jain explicit approximation.

  Swamee–Jain seed (used as the initial guess):

  $$
  f_{\text{SJ}} =
  \frac{0.25}{
    \left[
      \log_{10}\!\left(
        \frac{\varepsilon/D_h}{3.7} +
        \frac{5.74}{\mathrm{Re}^{0.9}}
      \right)
    \right]^2
  }
  $$

  [@swamee_jain_1976]

  Colebrook–White equation solved iteratively in the code:

  $$
  \frac{1}{\sqrt{f}} =
  -2 \,\log_{10}
  \left(
    \frac{\varepsilon/D_h}{3.7}
    + \frac{2.51}{\mathrm{Re}\sqrt{f}}
  \right)
  $$

  [@white_fluid_mechanics]

  The iteration is performed on $1/\sqrt{f}$ until convergence.

Local velocity and Reynolds number are evaluated using the side flow area $A$ and properties:

$$
V = \frac{\dot m}{\rho A}, \qquad
\mathrm{Re} = \frac{\rho V D_h}{\mu}
$$

Frictional losses are only applied for the `economizer` water side branch in `_water_dp_components`; for other stage kinds the current model sets $\Delta P_{\mathrm{fric}} = 0$.

## Gas side pressure drop in the economizer

The economizer gas side hydraulics differ fundamentally from all other modeled stages.  
While other stages assume internal flow and apply a Darcy–Weisbach formulation, the economizer models external crossflow over a tube bank, and gas side pressure losses are therefore computed using a bundle loss (drag-based) formulation rather than a wall-friction model.

### Crossflow bundle formulation {- .unlisted}

The gas flows across a bank of tubes arranged either inline or staggered.  
A characteristic velocity is defined using a bulk velocity corrected by a geometry-dependent maximum-velocity factor:

$$
V_{\mathrm{bulk}} = \frac{\dot m}{\rho A_{\mathrm{hot}}}, \qquad
V_{\mathrm{char}} = u_{\max}\, V_{\mathrm{bulk}}
$$

where:

- $A_{\mathrm{hot}} = \texttt{hot\_flow\_A}$ is the free crossflow area,
- $u_{\max} = \texttt{umax\_factor}$ accounts for flow acceleration between tubes.

The Reynolds number is formed using the tube outer diameter:

$$
\mathrm{Re}_D = \frac{\rho V_{\mathrm{char}} D_o}{\mu}
$$

### Bundle loss coefficient {- .unlisted}

The pressure loss per tube row is expressed via a dimensionless bundle loss coefficient:

$$
\zeta_{\text{row}} = C_0 \, \mathrm{Re}_D^{\,m} \, \Phi_{\mathrm{geom}}
$$

where:

- $C_0$ and $m$ depend on tube arrangement (inline or staggered),
- $\Phi_{\mathrm{geom}}$ accounts for pitch ratios:

$$
\Phi_{\mathrm{geom}} =
\left(\frac{S_T/D_o}{1.5}\right)^{-0.2}
\left(\frac{S_L/D_o}{1.5}\right)^{-0.2}
$$

with transverse pitch $S_T$ and longitudinal pitch $S_L$.

The total bundle loss coefficient is then:

$$
\zeta_{\text{bundle}} = N_{\mathrm{rows}} \, \zeta_{\text{row}}
$$

where $N_{\mathrm{rows}}$ is the number of tube rows in the flow direction.

### Distributed pressure loss {- .unlisted}

The dynamic pressure is evaluated using the characteristic velocity:

$$
q = \frac{\rho V_{\mathrm{char}}^2}{2}
$$

The total bundle pressure drop is:

$$
\Delta P_{\text{bundle}} = -\zeta_{\text{bundle}} \, q
$$

This loss is distributed uniformly along the economizer length $L$ across the marching steps:

$$
\Delta P_{\mathrm{fric,step}} =
\Delta P_{\text{bundle}} \, \frac{\Delta x}{L}
$$

where $\Delta x$ is the local marching step length.

## Minor losses

Minor losses are applied using per-stage catalogue $K$ values and the standard dynamic-pressure formulation:

$$
\Delta P_{\text{minor}} = -K_{\mathrm{minor}} \left( \frac{\rho V^{2}}{2} \right)
$$

[@crane_tp410]

The total minor-loss coefficient $K_{\mathrm{minor}}$ is assembled differently for gas and water sides, but applied through the same formulation.

### Coefficient assembly {- .unlisted}

Gas side.  
For each stage, the total loss coefficient is assembled from geometry and user inputs:

$$
K_{\mathrm{minor}} =
K_{\mathrm{contraction}}
+ K_{\mathrm{expansion}}
+ K_{\mathrm{bend}}
$$

Where:

- $K_{\mathrm{contraction}}$:
  accounts for sudden expansion of flow area (e.g. $\mathrm{HX_2} \rightarrow \mathrm{HX_3}$), default $= 0.5$.
- $K_{\mathrm{expansion}}$ (Borda–Carnot):
  losses caused by sudden expansion of flow area (e.g. $\mathrm{HX_1} \rightarrow \mathrm{HX_2}$), default $= 1$.
- $K_{\mathrm{bend}}$:
  losses due to gas flow rotation in reversal chambers, default $= 0$.

The bend loss is distributed uniformly across the $n$ marching steps:

$$
K_{\text{bend,per-step}} = \frac{K_{\text{cold,bend}}}{n}
$$

The per-step assembled coefficient is:

$$
K_{\mathrm{minor}} =
K_{\text{bend,per-step}}
+ \mathbb{1}_{i=0}\,K_{\text{cold,inlet}}
+ \mathbb{1}_{i=n-1}\,K_{\text{cold,outlet}}
$$

### Application {- .unlisted}

For both gas and water sides, the minor-loss pressure drop is computed using the local dynamic pressure:

$$
V = \frac{\dot m}{\rho A}, \qquad
q = \frac{\rho V^2}{2}, \qquad
\Delta P_{\text{minor}} = -K_{\mathrm{minor}}\,q
$$

where $A$ is the relevant side flow area ($A=\texttt{cold\_flow\_A}$ for water, gas side area otherwise).

## Total pressure drop

For each step, the total side pressure change is the sum of frictional and minor components:

$$
\Delta P_{\mathrm{total}} = \Delta P_{\mathrm{fric}} + \Delta P_{\mathrm{minor}}
$$

[@white_fluid_mechanics]

This is what `pressure_drop_gas/water` return and what is applied to the streams in `update_gas/water_after_step`.

## Coupling of ΔP into the energy solver

Gas/water pressure is updated step–wise using the same ΔP model:

$$
P_{i+1} = P_i + \Delta P_{\mathrm{total}}(P_i, T_i, \dots)
$$

After each step:

1. The local gas/water state $(T_i, P_i, \text{composition})$ is used to evaluate $\rho$, $\mu$, $k$, and $c_p$.
2. The friction factor and dynamic pressure are computed from these properties.
3. $\Delta P_{\mathrm{fric}}$ and $\Delta P_{\mathrm{minor}}$ are formed.
4. The updated pressure $P_{i+1}$ is used for the next step.

In this way, compressibility enters through the pressure dependence of $\rho(T,P)$ and $\mu(T,P)$ and their effect on $V$, $\mathrm{Re}$, and $f$.

\newpage
