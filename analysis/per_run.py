#!/usr/bin/env python3
"""
Generate performance figures per parameter group from boiler KPI CSV data.

Usage:
    python generate_boiler_figures.py [csv_path] [output_dir]

Defaults:
    csv_path  = "results/summary/boiler_kpis_all_runs.csv"
    output_dir = "results/plots/per_run"
"""

from pathlib import Path
import sys
from typing import Dict

import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# Global style configuration
# =============================================================================

# Colors for logical variables
style_colors: Dict[str, str] = {
    "Q_in": "tab:blue",
    "Q_useful": "tab:orange",
    "eta_direct": "tab:green",
    "eta_indirect": "tab:red",
    "water_flow": "tab:blue",
    "steam_capacity": "tab:orange",
    "stack_temperature": "tab:red",
    "pressure_drop": "tab:purple",
}

# Linestyles for logical variables
style_linestyles: Dict[str, str] = {
    "Q_in": "-",
    "Q_useful": "--",
    "eta_direct": "-",
    "eta_indirect": "--",
    "water_flow": "-",
    "steam_capacity": "--",
    "stack_temperature": "-",
    "pressure_drop": "--",
}

# Marker styles per parameter group
style_markers: Dict[str, str] = {
    "excess_air": "o",
    "fuel_flow": "s",
    "water_pressure": "D",
    "control": "x",
}

param_xlabels: Dict[str, str] = {
    "excess_air": r"Excess air $\lambda$ [-]",
    "fuel_flow": "Fuel flow [kg/s]",
    "water_pressure": "Water pressure [bar]",
    "control": "Control setting [-]",
}

def _get_xlabel(param_group: str) -> str:
    """Return x-axis label for a given parameter group."""
    return param_xlabels.get(param_group, "Parameter value [-]")

# Matplotlib global defaults suitable for thesis-quality figures
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["legend.fontsize"] = 9
plt.rcParams["figure.dpi"] = 100
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.linestyle"] = ":"
plt.rcParams["grid.linewidth"] = 0.5
plt.rcParams["grid.alpha"] = 0.7


# =============================================================================
# Data loading and preprocessing
# =============================================================================

def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load CSV into a DataFrame and ensure param_value is numeric.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded and minimally preprocessed data.
    """
    csv_file = Path(csv_path)
    df = pd.read_csv(csv_file)

    # Ensure param_value is numeric; non-convertible values become NaN
    df["param_value"] = pd.to_numeric(df["param_value"], errors="coerce")

    return df


# =============================================================================
# Helper plotting functions
# =============================================================================

def _get_marker(param_group: str):
    """Return marker style for a given parameter group, or None if unknown."""
    return style_markers.get(param_group, None)


def plot_Qin_Quseful(ax, df_group: pd.DataFrame, param_group: str) -> None:
    """
    Plot Q_in total and Q_useful vs param_value on a single Axes.
    """
    df_plot = df_group.dropna(subset=["param_value"]).sort_values("param_value")

    marker = _get_marker(param_group)

    x = df_plot["param_value"]
    y_qin = df_plot["Q_in total[MW]"]
    y_quse = df_plot["Q_useful[MW]"]

    line_qin, = ax.plot(
        x,
        y_qin,
        label="Total heat input $Q_{in}$",
        color=style_colors.get("Q_in", None),
        linestyle=style_linestyles.get("Q_in", "-"),
        marker=marker,
    )
    line_quse, = ax.plot(
        x,
        y_quse,
        label="Useful heat $Q_{useful}$",
        color=style_colors.get("Q_useful", None),
        linestyle=style_linestyles.get("Q_useful", "--"),
        marker=marker,
    )

    ax.set_xlabel(_get_xlabel(param_group))
    ax.set_ylabel("Heat rate [MW]")
    ax.set_title("Heat rates")
    ax.grid(True, which="both")
    ax.legend(loc="best", framealpha=0.8)


def plot_eta(ax, df_group: pd.DataFrame, param_group: str) -> None:
    """
    Plot direct and indirect efficiency vs param_value on a single Axes.
    """
    df_plot = df_group.dropna(subset=["param_value"]).sort_values("param_value")

    marker = _get_marker(param_group)

    x = df_plot["param_value"]
    y_eta_dir = df_plot["eta direct[-]"]
    y_eta_ind = df_plot["eta indirect[-]"]

    line_eta_dir, = ax.plot(
        x,
        y_eta_dir,
        label="Direct efficiency",
        color=style_colors.get("eta_direct", None),
        linestyle=style_linestyles.get("eta_direct", "-"),
        marker=marker,
    )
    line_eta_ind, = ax.plot(
        x,
        y_eta_ind,
        label="Indirect efficiency",
        color=style_colors.get("eta_indirect", None),
        linestyle=style_linestyles.get("eta_indirect", "--"),
        marker=marker,
    )
    ax.set_xlabel(_get_xlabel(param_group))
    ax.set_ylabel("Efficiency [-]")
    ax.set_title("Boiler efficiency")
    ax.grid(True, which="both")
    ax.legend(loc="best", framealpha=0.8)


def plot_water_steam(ax, df_group: pd.DataFrame, param_group: str) -> None:
    """
    Plot water flow and steam capacity vs param_value using twin y-axes.
    """
    df_plot = df_group.dropna(subset=["param_value"]).sort_values("param_value")

    marker = _get_marker(param_group)

    x = df_plot["param_value"]
    y_water = df_plot["water flow[kg/s]"]
    y_steam = df_plot["steam capacity[t/h]"]

    # Primary axis: water flow
    line_water, = ax.plot(
        x,
        y_water,
        label="Water flow",
        color=style_colors.get("water_flow", None),
        linestyle=style_linestyles.get("water_flow", "-"),
        marker=marker,
    )
    ax.set_xlabel(_get_xlabel(param_group))
    ax.set_ylabel("Water flow [kg/s]")
    ax.set_title("Water and steam")

    # Secondary axis: steam capacity
    ax2 = ax.twinx()
    line_steam, = ax2.plot(
        x,
        y_steam,
        label="Steam capacity",
        color=style_colors.get("steam_capacity", None),
        linestyle=style_linestyles.get("steam_capacity", "--"),
        marker=marker,
    )
    ax2.set_ylabel("Steam capacity [t/h]")

    ax.grid(True, which="both")

    # Combined legend from both axes
    lines = [line_water, line_steam]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc="best", framealpha=0.8)


def plot_stack_pressure(ax, df_group: pd.DataFrame, param_group: str) -> None:
    """
    Plot stack temperature and total pressure drop vs param_value with twin y-axes.
    """
    df_plot = df_group.dropna(subset=["param_value"]).sort_values("param_value")

    marker = _get_marker(param_group)

    x = df_plot["param_value"]
    y_stack = df_plot["stack temperature[°C]"]
    y_dp = df_plot["pressure drop total[Pa]"].abs()

    # Primary axis: stack temperature
    line_stack, = ax.plot(
        x,
        y_stack,
        label="Stack temperature",
        color=style_colors.get("stack_temperature", None),
        linestyle=style_linestyles.get("stack_temperature", "-"),
        marker=marker,
    )
    ax.set_xlabel(_get_xlabel(param_group))
    ax.set_ylabel("Stack temperature [°C]")
    ax.set_title("Stack and pressure drop")

    # Secondary axis: pressure drop
    ax2 = ax.twinx()
    line_dp, = ax2.plot(
        x,
        y_dp,
        label="Total pressure drop",
        color=style_colors.get("pressure_drop", None),
        linestyle=style_linestyles.get("pressure_drop", "--"),
        marker=marker,
    )
    ax2.set_ylabel("Total pressure drop [Pa]")

    ax.grid(True, which="both")

    # Combined legend from both axes
    lines = [line_stack, line_dp]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc="best", framealpha=0.8)

def generate_overall_kpi_figure(csv_path: str, output_dir: str = "figures") -> None:
    """
    Generate a single 2x4 figure (2 columns, 4 rows) showing all parameter groups
    together for eight KPIs, one KPI per subplot.

    Colors and linestyles correspond to PARAMETER GROUPS,
    reusing the existing style dictionaries deterministically.

    One global legend for all param_group markers.
    Each subplot has:
        x-axis: Parameter value [-]
        y-axis: KPI value
    No titles.

    Layout (rows x columns):
        Row 1: Tad                 | Stack temperature
        Row 2: Air flow            | Water flow
        Row 3: Q_in total          | Steam capacity
        Row 4: Pressure drop       | Direct efficiency
    """
    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = df.dropna(subset=["param_value"]).copy()

    # KPI definitions in the desired layout order
    kpi_defs = [
        # Row 1
        {"column": "Tad[°C]",                 "ylabel": "Tad [°C]"},
        {"column": "stack temperature[°C]",   "ylabel": "Stack temperature [°C]"},
        # Row 2
        {"column": "air flow[kg/s]",          "ylabel": "Air flow [kg/s]"},
        {"column": "water flow[kg/s]",        "ylabel": "Water flow [kg/s]"},
        # Row 3
        {"column": "Q_in total[MW]",          "ylabel": r"Heat input $Q_{in}$ [MW]"},
        {"column": "steam capacity[t/h]",     "ylabel": "Steam capacity [t/h]"},
        # Row 4
        {"column": "pressure drop total[Pa]", "ylabel": "Total pressure drop [Pa]", "abs": True},
        {"column": "eta direct[-]",           "ylabel": "Direct efficiency [-]"},
    ]

    # Prepare 4 x 2 grid (4 rows, 2 columns)
    fig, axes = plt.subplots(4, 2, figsize=(9, 10))
    axes_flat = axes.flatten()

    for ax, kpi in zip(axes_flat, kpi_defs):
        ax.set_xlabel("Parameter value [-]")
        ax.set_ylabel(kpi["ylabel"])
        ax.grid(True, which="both")

    # Assign each param_group a stable color + linestyle from the existing dicts
    pg_list = sorted(df["param_group"].unique())

    style_color_keys = list(style_colors.keys())
    style_line_keys  = list(style_linestyles.keys())

    pg_color = {
        pg: style_colors[style_color_keys[i % len(style_color_keys)]]
        for i, pg in enumerate(pg_list)
    }
    pg_line = {
        pg: style_linestyles[style_line_keys[i % len(style_line_keys)]]
        for i, pg in enumerate(pg_list)
    }

    legend_handles = {}

    # Plot
    for param_group, df_group in df.groupby("param_group"):
        df_group_sorted = df_group.sort_values("param_value")
        x = df_group_sorted["param_value"]

        marker = _get_marker(param_group) or "o"
        color = pg_color[param_group]
        line_style = pg_line[param_group]

        for ax, kpi in zip(axes_flat, kpi_defs):
            col = kpi["column"]
            if col not in df_group_sorted.columns:
                continue

            y_raw = df_group_sorted[col]
            y = y_raw.abs() if kpi.get("abs", False) else y_raw

            line, = ax.plot(
                x, y,
                marker=marker,
                linestyle=line_style,
                color=color,
                label=param_group,
            )

            if param_group not in legend_handles:
                legend_handles[param_group] = line

    # Global legend
    if legend_handles:
        fig.legend(
            handles=list(legend_handles.values()),
            labels=list(legend_handles.keys()),
            loc="lower center",
            ncol=min(len(legend_handles), 4),
            framealpha=0.8,
            bbox_to_anchor=(0.5, 0.02),
        )

    fig.tight_layout(rect=(0.0, 0.05, 1.0, 1.0))

    out_path = out_dir / "kpi_overview_all_param_groups.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)

def generate_stage_param_figure(
    csv_path: str = "results/summary/stages_summary_all_runs.csv",
    output_dir: str = "figures",
) -> None:
    """
    Generate a 2x2 figure with stage-wise results, grouped by param_group.

    Subplots:
        (0,0): Stage duty Q_total vs stage
        (0,1): Stage conductance UA vs stage
        (1,0): Gas outlet temperature vs stage
        (1,1): Total pressure drop vs stage

    x-axis for all subplots: stage index (1–6)
    Colors / linestyles / markers: same scheme as in generate_overall_kpi_figure.
    """
    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Extract numeric stage index from strings like "HX_1" -> 1
    # If 'stage' is already numeric, this will leave it unchanged.
    if df["stage"].dtype == object:
        df["stage_index"] = (
            df["stage"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .astype(int)
        )
    else:
        df["stage_index"] = df["stage"].astype(int)

    # Drop rows without stage index
    df = df.dropna(subset=["stage_index"]).copy()

    # Prepare figure
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    ax_duty = axes[0, 0]
    ax_UA   = axes[0, 1]
    ax_Tg   = axes[1, 0]
    ax_dp   = axes[1, 1]

    # Common x-ticks: all stages present
    stage_ticks = sorted(df["stage_index"].unique())

    for ax in (ax_duty, ax_UA, ax_Tg, ax_dp):
        ax.set_xlabel("Stage [-]")
        ax.set_xticks(stage_ticks)
        ax.grid(True, which="both")

    ax_duty.set_ylabel("Stage duty $Q_{\\mathrm{stage}}$ [MW]")
    ax_UA.set_ylabel("Stage conductance $UA$ [MW/K]")
    ax_Tg.set_ylabel("Gas outlet temperature [°C]")
    ax_dp.set_ylabel("Total pressure drop [Pa]")

    # Colors / linestyles per param_group, same logic as generate_overall_kpi_figure
    pg_list = sorted(df["param_group"].unique())

    style_color_keys = list(style_colors.keys())
    style_line_keys  = list(style_linestyles.keys())

    pg_color = {
        pg: style_colors[style_color_keys[i % len(style_color_keys)]]
        for i, pg in enumerate(pg_list)
    }
    pg_line = {
        pg: style_linestyles[style_line_keys[i % len(style_line_keys)]]
        for i, pg in enumerate(pg_list)
    }

    legend_handles = {}

    # Plot one line per RUN, colored by param_group
    for param_group, df_pg in df.groupby("param_group"):
        marker = _get_marker(param_group) or "o"
        color = pg_color[param_group]
        line_style = pg_line[param_group]
        lw = 0.7

        for run_name, df_run in df_pg.groupby("run"):
            df_run_sorted = df_run.sort_values("stage_index")
            x = df_run_sorted["stage_index"]

            # Column names from stages_summary_all_runs.csv
            y_Q  = df_run_sorted["Q total[MW]"]
            y_UA = df_run_sorted["UA[MW/K]"]
            y_Tg = df_run_sorted["gas out temp[°C]"]
            y_dp = df_run_sorted["pressure drop total[pa]"].abs()

            # Duty
            line_duty, = ax_duty.plot(
                x,
                y_Q,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
                label=param_group,
            )

            # Conductance
            ax_UA.plot(
                x,
                y_UA,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            # Gas outlet temperature
            ax_Tg.plot(
                x,
                y_Tg,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            # Pressure drop
            ax_dp.plot(
                x,
                y_dp,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            # One legend handle per param_group (so 4 entries, not 13)
            if param_group not in legend_handles:
                legend_handles[param_group] = line_duty


    # Global legend for param_groups
    if legend_handles:
        fig.legend(
            handles=list(legend_handles.values()),
            labels=list(legend_handles.keys()),
            loc="lower center",
            ncol=min(len(legend_handles), 4),
            framealpha=0.8,
            bbox_to_anchor=(0.5, 0.02),
        )

    fig.tight_layout(rect=(0.0, 0.05, 1.0, 1.0))

    out_path = out_dir / "stages_param_groups.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


# =============================================================================
# Main figure generation
# =============================================================================

def generate_all_figures(csv_path: str, output_dir: str = "figures") -> None:
    """
    Generate one figure per parameter group with at least two distinct param_value entries.

    Parameters
    ----------
    csv_path : str
        Path to the input CSV file.
    output_dir : str, optional
        Output directory for figures. Created if it does not exist.
    """
    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Only consider groups with at least two distinct numeric param_value entries
    grouped = df.groupby("param_group")

    for param_group, df_group in grouped:
        df_group_numeric = df_group.dropna(subset=["param_value"])
        if df_group_numeric["param_value"].nunique(dropna=True) < 2:
            # Skip groups without enough variation for meaningful plots
            continue

        fig, axes = plt.subplots(2, 2, figsize=(8, 6))
        ax_tl = axes[0, 0]
        ax_tr = axes[0, 1]
        ax_bl = axes[1, 0]
        ax_br = axes[1, 1]

        plot_Qin_Quseful(ax_tl, df_group_numeric, param_group)
        plot_eta(ax_tr, df_group_numeric, param_group)
        plot_water_steam(ax_bl, df_group_numeric, param_group)
        plot_stack_pressure(ax_br, df_group_numeric, param_group)

        fig.tight_layout()

        # Construct output filenames
        safe_group = str(param_group).replace(" ", "_")
        png_path = out_dir / f"performance_{safe_group}.png"

        fig.savefig(png_path, dpi=300)
        plt.close(fig)


if __name__ == "__main__":
    # Defaults for this workflow
    default_csv = "results/summary/boiler_kpis_all_runs.csv"
    default_output = "results/plots/per_run"

    if len(sys.argv) >= 2:
        csv_arg = sys.argv[1]
    else:
        csv_arg = default_csv

    if len(sys.argv) >= 3:
        out_arg = sys.argv[2]
    else:
        out_arg = default_output

    # Existing per-parameter-group figures (unchanged behavior)
    generate_all_figures(csv_arg, output_dir=out_arg)

    # NEW: one 4x2 figure with all param_groups on each KPI subplot
    generate_overall_kpi_figure(csv_arg, output_dir=out_arg)

    # NEW: stage-wise figure from stages_summary_all_runs.csv
    stage_csv = "results/summary/stages_summary_all_runs.csv"
    generate_stage_param_figure(stage_csv, output_dir=out_arg)

