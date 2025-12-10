from pathlib import Path
import re

import pandas as pd
import matplotlib.pyplot as plt


# ======================================================================
# Configuration
# ======================================================================

RESULTS_DIR = Path("results")
PLOTS_DIR = RESULTS_DIR / "plots"
SUMMARY_DIR = RESULTS_DIR / "summary"

# Regex to recognize filenames:
#   default_case_boiler_summary.csv
#   excess_air_1.1_steps.csv
#   fuel_flow_0.025kgs_stages_summary.csv
#   water_pressure_4.0bar_boiler_summary.csv
FILE_RE = re.compile(
    r"^(?P<case>(?P<param>excess_air|fuel_flow|water_pressure)_(?P<value>[^_]+)|default_case)_(?P<kind>boiler_summary|stages_summary|steps)\.csv$"
)


def parse_param_value(raw):
    """Turn '1.1', '0.025kgs', '10.0bar' into float; otherwise return raw/None."""
    if raw is None:
        return None

    # strip known unit suffixes
    for suffix in ("kgs", "bar"):
        if raw.endswith(suffix):
            raw = raw[: -len(suffix)]

    try:
        return float(raw)
    except ValueError:
        return raw


# Groupings for steps variables vs x[m]
STEP_GROUPS = {
    "temp": {
        "label": "Temperatures",
        "vars": ["gas_T[°C]", "water_T[°C]"],
    },
    "pressure": {
        "label": "Pressures",
        "vars": ["gas_P[Pa]", "water_P[Pa]"],
    },
    "enthalpy": {
        "label": "Enthalpies",
        "vars": ["gas_h[kJ/kg]", "water_h[kJ/kg]"],
    },
    "htc": {
        "label": "Heat transfer coefficients",
        "vars": ["h_gas[W/m^2/K]", "h_water[W/m^2/K]"],
    },
    "vel_re": {
        "label": "Velocities and Reynolds numbers",
        "vars": ["gas_V[m/s]", "water_V[m/s]", "Re_gas[-]", "Re_water[-]"],
    },
    "q_ua": {
        "label": "Linear heat / UA",
        "vars": ["qprime[MW/m]", "UA_prime[MW/K/m]"],
    },
    "dp": {
        "label": "Pressure drops",
        "vars": ["dP_fric[Pa]", "dP_minor[Pa]", "dP_total[Pa]"],
    },
    "gas_props": {
        "label": "Gas properties",
        "vars": [
            "gas_cp[kJ/kg/K]",
            "gas_mu[Pa*s]",
            "gas_k[W/m/K]",
            "gas_rho[kg/m^3]",
        ],
    },
    "water_props": {
        "label": "Water properties",
        "vars": [
            "water_cp[kJ/kg/K]",
            "water_mu[Pa*s]",
            "water_k[W/m/K]",
            "water_rho[kg/m^3]",
        ],
    },
    "quality": {
        "label": "Gas emissivity and water quality",
        "vars": ["gas_eps[-]", "water_x[-]"],
    },
}


# ======================================================================
# Discovery and loading
# ======================================================================

def discover_runs(results_dir: Path):
    """
    Scan results_dir and collect files into runs:
        {
          case_name: {
            "case": case_name,
            "param": "excess_air" | "fuel_flow" | "water_pressure" | "control",
            "value": numeric or raw parameter value,
            "files": {
               "boiler_summary": Path(...),
               "stages_summary": Path(...),
               "steps": Path(...),
            }
          },
          ...
        }
    """
    runs = {}

    for path in results_dir.glob("*.csv"):
        m = FILE_RE.match(path.name)
        if not m:
            # Skip files that don't match naming convention
            continue

        case = m.group("case")  # e.g. 'excess_air_1.1' or 'default_case'
        param = m.group("param")  # e.g. 'excess_air' or None
        raw_value = m.group("value")  # e.g. '1.1', '0.025kgs', '10.0bar'
        kind = m.group("kind")  # 'boiler_summary' | 'stages_summary' | 'steps'

        info = runs.setdefault(
            case,
            {
                "case": case,
                "param": param if param is not None else "control",
                "value": parse_param_value(raw_value),
                "files": {},
            },
        )
        info["files"][kind] = path

    return runs


def load_boiler_as_series(path: Path, run_name: str, param_group: str, param_value):
    """
    Load boiler_summary (parameter,value) -> turn into one Series with:
        index = parameter names
        plus 'run', 'param_group', 'param_value'
    """
    df = pd.read_csv(path)
    # Expect columns: parameter,value
    s = df.set_index("parameter")["value"]
    s = s.copy()
    s["run"] = run_name
    s["param_group"] = param_group
    s["param_value"] = param_value
    return s


def load_stage_as_tidy(path: Path, run_name: str, param_group: str, param_value):
    """
    Load stages_summary CSV with rows as parameters and columns as HX_1..HX_n.

    Returns a tidy DataFrame with columns:
        run, param_group, param_value, stage, <all stage parameters...>
    """
    df_raw = pd.read_csv(path, index_col=0)
    # Transpose so each row is a stage
    df = df_raw.T.reset_index().rename(columns={"index": "stage"})
    df.insert(0, "run", run_name)
    df.insert(1, "param_group", param_group)
    df.insert(2, "param_value", param_value)
    return df


def load_steps(path: Path):
    """
    Load steps CSV as DataFrame, no extra processing here.
    """
    return pd.read_csv(path)


# ======================================================================
# Plotting helpers
# ======================================================================

def safe_name(s: str) -> str:
    """Turn an arbitrary string into a filename-safe token."""
    return re.sub(r"[^0-9A-Za-z]+", "_", s).strip("_")


def plot_steps_groups(run_info, steps_df: pd.DataFrame, outdir: Path):
    """
    For a single run, create grouped plots of various step variables vs x[m].
    """
    if "x[m]" not in steps_df.columns:
        print(f"[WARN] run {run_info['case']}: 'x[m]' column not found in steps, skipping plots.")
        return

    x = steps_df["x[m]"]
    outdir.mkdir(parents=True, exist_ok=True)

    for group_key, group in STEP_GROUPS.items():
        label = group["label"]
        vars_ = [v for v in group["vars"] if v in steps_df.columns]

        if not vars_:
            # Nothing from this group present in the DataFrame
            continue

        plt.figure()
        for var in vars_:
            plt.plot(x, steps_df[var], label=var)

        plt.xlabel("x[m]")
        plt.ylabel(label)
        plt.title(f"{run_info['case']} – {label} vs x")
        plt.legend()
        plt.tight_layout()
        fname = f"{run_info['case']}_steps_{safe_name(group_key)}.png"
        plt.savefig(outdir / fname, dpi=150)
        plt.close()


# ======================================================================
# Main driver
# ======================================================================

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    runs = discover_runs(RESULTS_DIR)

    if not runs:
        print("[INFO] No runs discovered in 'results/' matching expected patterns.")
        return

    # Collect boiler KPIs and stage summaries for all runs
    boiler_rows = []
    stage_rows = []

    for case, info in runs.items():
        files = info["files"]
        run_name = info["case"]
        param_group = info["param"]
        param_value = info["value"]

        # Boiler summary -> KPI Series
        if "boiler_summary" in files:
            s = load_boiler_as_series(files["boiler_summary"], run_name, param_group, param_value)
            boiler_rows.append(s)
        else:
            print(f"[WARN] run {run_name}: boiler_summary file missing.")

        # Stages summary -> tidy rows
        if "stages_summary" in files:
            df_stages = load_stage_as_tidy(files["stages_summary"], run_name, param_group, param_value)
            stage_rows.append(df_stages)
        else:
            print(f"[WARN] run {run_name}: stages_summary file missing.")

        # Steps -> grouped plots vs x
        if "steps" in files:
            steps_df = load_steps(files["steps"])
            run_plot_dir = PLOTS_DIR / run_name
            plot_steps_groups(info, steps_df, run_plot_dir)
        else:
            print(f"[WARN] run {run_name}: steps file missing, no step plots.")

    # ==================================================================
    # Combined boiler KPI table (all runs)
    # ==================================================================
    if boiler_rows:
        boiler_df = pd.DataFrame(boiler_rows)
        # Move 'run', 'param_group', 'param_value' to the front
        cols = list(boiler_df.columns)
        for key in ["run", "param_group", "param_value"]:
            if key in cols:
                cols.remove(key)
        ordered_cols = ["run", "param_group", "param_value"] + cols
        boiler_df = boiler_df[ordered_cols]
        boiler_df.to_csv(SUMMARY_DIR / "boiler_kpis_all_runs.csv", index=False)
        print(f"[INFO] Wrote boiler KPIs table: {SUMMARY_DIR / 'boiler_kpis_all_runs.csv'}")
    else:
        print("[INFO] No boiler KPI data collected.")

    # ==================================================================
    # Combined stages summary table (all runs, all stages)
    # ==================================================================
    if stage_rows:
        # Filter out empty dataframes to avoid FutureWarning
        non_empty_stage_rows = [df for df in stage_rows if not df.empty]

        if non_empty_stage_rows:
            stages_df = pd.concat(non_empty_stage_rows, ignore_index=True)
            stages_df.to_csv(SUMMARY_DIR / "stages_summary_all_runs.csv", index=False)
            print(f"[INFO] Wrote stages summary table: {SUMMARY_DIR / 'stages_summary_all_runs.csv'}")
        else:
            print("[INFO] Stage summary dataframes are all empty; nothing to write.")
    else:
        print("[INFO] No stage summary data collected.")


if __name__ == "__main__":
    main()
