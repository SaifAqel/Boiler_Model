from pathlib import Path
import re

import pandas as pd


# ======================================================================
# Configuration
# ======================================================================

RESULTS_DIR = Path("results")
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
# Main driver
# ======================================================================

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
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

        # Steps file is discovered and loadable, but no plots are produced
        if "steps" not in files:
            print(f"[WARN] run {run_name}: steps file missing.")

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
