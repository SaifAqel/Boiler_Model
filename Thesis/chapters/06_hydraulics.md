# Hydraulic Calculations

Hydraulic behaviour is extracted directly from the solver through the per-step pressure-drop decomposition implemented in `heat/solver.py` (`_gas_dp_components`, `pressure_drop_gas`) and accumulated at the stage level in `heat/solver.py::solve_stage` and in the boiler summary computed by `heat/postproc.py::summary_from_profile`.

The model divides gas-side pressure losses into:

- Frictional losses:  
  Computed by Colebrook–White (turbulent), laminar 64/Re, and a linear transitional blend for 2300 < $\mathrm{Re} < 4000$.  
  The per-step drop is $$\Delta P_{\mathrm{fric}} = - f \frac{\Delta x}{D_h}\left(\frac{\rho V^2}{2}\right)$$ where $f$ is obtained from `_friction_factor()` and hydraulic diameter, velocity, and density come from the local gas state.

- Minor losses:  
  Applied using per-stage catalogue $K$-values.  
  For reversal chambers, inlet/outlet nozzle $K$ plus bend-equivalent loss are included; tube-banks default to zero unless specified.  
  In `solve_stage`, the total per-stage loss coefficient $K_{\mathrm{sum}}$ is uniformly distributed across $N$ steps:
  $$K_{\mathrm{per\,step}} = \frac{K_{\mathrm{sum}}}{N}$$  
  The per-step minor loss is  
  $$\Delta P_{\mathrm{minor}} = -K_{\mathrm{per\,step}}\left(\frac{\rho V^2}{2}\right)$$

- Total gas-side drop:  
  $$\Delta P_{\mathrm{total}} = \Delta P_{\mathrm{fric}} + \Delta P_{\mathrm{minor}}$$

Water-side pressure losses are intentionally not included in this model (water at constant pressure).

---

## Gas-Side ΔP per Stage

During each call to `solve_stage`, the solver marches through all steps and accumulates:

- `dP_stage_fric`
- `dP_stage_minor`
- `dP_stage_total`

These appear in each stage row of `summary_rows` returned by `run_hx()`.  
An example schema from `summary_from_profile()`:

```python
"ΔP_stage_fric[Pa]": dP_fric,
"ΔP_stage_minor[Pa]": dP_minor,
"ΔP_stage_total[Pa]": dP_total,
```

Values are integrated over the entire stage length:
$$\Delta P_{\mathrm{stage}} = \sum_{i=1}^{N} \Delta P(i)$$

---

## Water-Side ΔP per Stage

The present solver does not compute water-side frictional or accelerational pressure losses.  
From the code (`update_water_after_step`), pressure remains constant:

```python
WaterStream(mass_flow=w.mass_flow, h=h_new, P=w.P)
```

Thus:

- Water-side ΔP per stage = 0 Pa
- Total water-side ΔP = 0 Pa

This assumption is consistent with pool-boiling and saturated-drum configurations where the water is not routed through high-velocity conduits.

---

## Total Boiler ΔP and Stack Pressure

The boiler-level gas-side pressure drop is assembled in the `TOTAL_BOILER` row of `summary_from_profile()`:

```python
"ΔP_stage_fric[Pa]": dP_total_fric,
"ΔP_stage_minor[Pa]": dP_total_minor,
"ΔP_stage_total[Pa]": dP_total_total,
```

This yields:

- Total frictional drop:  
  $$\Delta P_{\mathrm{fric,tot}} = \sum_{k=1}^{6} \Delta P_{\mathrm{fric},k}$$
- Total minor-loss drop:  
  $$\Delta P_{\mathrm{minor,tot}} = \sum_{k=1}^{6} \Delta P_{\mathrm{minor},k}$$
- Overall boiler gas-side drop:  
  $$\Delta P_{\mathrm{boiler}} = \Delta P_{\mathrm{fric,tot}} + \Delta P_{\mathrm{minor,tot}}$$

Stack exit pressure is simply the outlet gas pressure after stage 6:

```python
gas_out.P
```

reported separately in the boiler summary.

---

## Consolidated ΔP Table (from solver output)

A typical extracted table structure (values populated after running `main.py`):

```python
| Stage | Kind              | ΔP_fric [Pa] | ΔP_minor [Pa] | ΔP_total [Pa] |
|-------|-------------------|--------------|----------------|----------------|
| HX_1  | single_tube       | ...          | ...            | ...            |
| HX_2  | reversal_chamber  | ...          | ...            | ...            |
| HX_3  | tube_bank         | ...          | ...            | ...            |
| HX_4  | reversal_chamber  | ...          | ...            | ...            |
| HX_5  | tube_bank         | ...          | ...            | ...            |
| HX_6  | economiser        | 0            | 0              | 0              |
| TOTAL | —                 | Σ            | Σ              | Σ              |
```

$HX_6$ (economiser) contributes zero ΔP by design (`_gas_dp_components` returns 0 for this stage).

The table is directly generated as part of `summary_rows` once `main.py` completes the mass-flow/efficiency iteration and writes final CSVs.

\newpage
