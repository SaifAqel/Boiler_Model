# Hydraulic Model

Hydraulic behavior is extracted directly from the solver through the per step pressure drop decomposition implemented in `heat/solver.py` (`_gas_dp_components`, `pressure_drop_gas`) and accumulated at the stage level in `heat/solver.py::solve_stage`.

The model divides gas side pressure losses into:

- Frictional losses
- Minor losses (inlet, outlet, bends, etc.)
- Total pressure drop (sum of the above)

Water side pressure losses are intentionally not included in this model (water is taken at constant drum pressure).

## Frictional losses

The per step frictional pressure drop follows a standard 1D formulation:

$$
\Delta P_{\mathrm{fric}} = - f \, \frac{\Delta x}{D_h} \left( \frac{\rho V^2}{2} \right)
$$

[@white_fluid_mechanics]

Here:

- $f$ is the Darcy friction factor,
- $D_h$ is the gas side hydraulic diameter (`hot_Dh`),
- $\rho$ and $V$ are local gas density and velocity,
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

- Turbulent ($\mathrm{Re} \ge 4000$):  
  Colebrook–White is solved iteratively, seeded by the Swamee–Jain explicit approximation.

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

## Minor losses

Minor losses are applied using per–stage catalogue $K$ values. For each stage, a total loss coefficient $K_{\mathrm{sum}}$ is assembled from geometry and user inputs:

- `economiser`  
  Minor losses are neglected:

  $$
  K_{\mathrm{sum}} = 0
  $$

- `reversal_chamber`  
  Includes nozzle and bend losses:

  - Inlet/outlet: `nozzle_k_in` + `nozzle_k_out` (if provided),
  - Bend loss $K_{\mathrm{bend}}$ based on curvature ratio:

    $$
    K_{\mathrm{bend}} = R_c / D_o
    $$

    with a fallback $K_{\mathrm{bend}} = 0.5$ if geometry is missing.

- `single_tube`  
  Defaults are used if not overridden in the spec:

  $$
  K_{\mathrm{contraction}} = 0.5,\quad
  K_{\mathrm{expansion}}  = 1.0,\quad
  K_{\mathrm{exit}}       = 1.0
  $$

  so that

  $$
  K_{\mathrm{sum}} = K_{\mathrm{contraction}} + K_{\mathrm{expansion}} + K_{\mathrm{exit}}
  $$

- `tube_bank`  
  Defaults to zero for all minor loss coefficients unless explicitly provided:

  $$
  K_{\mathrm{contraction}},\; K_{\mathrm{expansion}},\; K_{\mathrm{exit}} \to 0
  $$

Once $K_{\mathrm{sum}}$ is known, it is uniformly distributed over the $N$ marching steps of that stage:

Minor-loss pressure drop is given by:

$$
\Delta P_{\text{minor}} = K \left( \frac{\rho V^{2}}{2} \right)
$$

[@crane_tp410]

$$
K_{\mathrm{per\,step}} = \frac{K_{\mathrm{sum}}}{N}
$$

The per–step minor loss is then

$$
\Delta P_{\mathrm{minor}} = - K_{\mathrm{per\,step}} \left( \frac{\rho V^2}{2} \right)
$$

## Total gas side pressure drop

For each step, the total gas–side pressure change is the sum of frictional and minor components:

$$
\Delta P_{\mathrm{total}} = \Delta P_{\mathrm{fric}} + \Delta P_{\mathrm{minor}}
$$

[@white_fluid_mechanics]

This is what `pressure_drop_gas` returns and what is applied to the gas stream in `update_gas_after_step`.

## Coupling of ΔP into the energy solver

Gas pressure is updated step–wise using the same ΔP model:

$$
P_{i+1} = P_i + \Delta P_{\mathrm{total}}(P_i, T_i, \dots)
$$

After each step:

1. The local gas state $(T_i, P_i, \text{composition})$ is used to evaluate
   $\rho$, $\mu$, $k$, and $c_p$.
2. The friction factor and dynamic pressure are computed from these properties.
3. $\Delta P_{\mathrm{fric}}$ and $\Delta P_{\mathrm{minor}}$ are formed.
4. The updated pressure $P_{i+1}$ is used for the next step, so density, viscosity, Reynolds number, and gas side HTC $h_g$ are all evaluated at the updated pressure.

In this way, compressibility enters through the pressure dependence of $\rho(T,P)$ and $\mu(T,P)$ and their effect on $V$, $\mathrm{Re}$, and $f$.
