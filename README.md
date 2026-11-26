# Boiler_Model

Steady-state model of a fire-tube boiler: combustion → flue-gas path → staged heat
exchangers → drum. Pure Python, config-driven, writes CSV results that are then turned
into KPI tables and plots. Bachelor thesis code (BME, QTY3S6).

## How it works

`main.py` calls `run_boiler_case()` in `common/boiler_loop.py`, which:

1. loads the YAML config from `config/`,
2. burns the fuel (`combustion/`) — adiabatic flame temperature, flue-gas composition,
   mass/mole balance,
3. marches the gas through the heat-exchange stages (`heat/`), each solved for
   convection + radiation + wall conduction + fouling,
4. closes the mass/energy balance on the drum (steam rate, feedwater),
5. writes `*_boiler_summary.csv`, `*_stages_summary.csv`, `*_steps.csv` into `results/runs/`.

## Layout

| Path | Contents |
|---|---|
| `main.py` | entry point + sensitivity-case runners |
| `config/` | air, fuel, water, drum, operation, `stages.yaml` (HX geometry) |
| `combustion/` | combustor, flue gas, adiabatic flame temperature |
| `heat/` | geometry, gas/water HTCs, stage solver, post-processing |
| `common/` | boiler loop, property wrappers (`pint`, `iapws`), config loader, CSV output |
| `analysis/` | KPI tables and per-run / heat-map plots from `results/runs` |
| `results/` | generated CSVs, summary tables, plots |
| `Thesis/` | thesis source (Markdown → pandoc/LaTeX), figures, PDF |
| `Presentation/` | beamer talk |

## Requirements

```bash
pip install pint iapws cantera pyyaml pandas numpy scipy matplotlib reportlab
```

## Run

```bash
python main.py                 # default case only
```

Sensitivity sweeps (excess air, drum pressure, fuel flow, fouling) live in `main.py` and
are commented out — uncomment the one you want.

Then analyse what was written:

```bash
python analysis/analyze_boiler_runs.py
python analysis/tables.py
python analysis/per_run.py
python analysis/map.py
```

## Config

Every value is `{ value: <number>, unit: <pint unit> }`, so units are explicit and
checked. Geometry in `config/stages.yaml`, operating point in `config/operation.yaml`
(excess air ratio, drum pressure), fuel composition in `config/fuel.yaml`, fouling via
the `fouling_factor` argument to `run_boiler_case()`.

## Thesis build

```bash
pandoc Thesis/master.md Thesis/chapters/*.md -o Thesis/thesis.pdf \
  --filter pandoc-crossref --biblatex \
  --pdf-engine=latexmk --pdf-engine-opt=-xelatex
```

Requires xelatex, pandoc-crossref and biber.
