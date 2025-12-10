# plotty.py
"""
Generate publication-quality plots for boiler KPI and stage-wise HX data.

Input CSVs (relative to repository root):
    results/summary/boiler_kpis_all_runs.csv
    results/summary/stages_summary_all_runs.csv

Outputs:
    Figures (PNG + PDF) into:
    results/plots/
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# General configuration
# ---------------------------------------------------------------------------

def set_thesis_style():
    """Configure Matplotlib defaults for a scientific/engineering thesis."""
    plt.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "figure.figsize": (6.0, 4.0),
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.grid": True,
            "grid.linestyle": "--",
            "grid.alpha": 0.4,
            "lines.linewidth": 1.5,
            "lines.markersize": 4,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

# Fixed order so param groups keep consistent colors across figures
PARAM_GROUP_ORDER = ["excess_air", "fuel_flow", "water_pressure", "control"]


def get_param_color_map(param_groups):
    """
    Return a dict param_group -> color, consistent across all plots.

    Uses a fixed logical order (PARAM_GROUP_ORDER), then any remaining groups.
    Colors are taken from the Matplotlib default color cycle.
    """
    colors = plt.rcParams["axes.prop_cycle"].by_key().get("color", [])
    if not colors:
        # Fallback if prop_cycle not available
        colors = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]

    ordered_groups = [
        g for g in PARAM_GROUP_ORDER if g in param_groups
    ] + [
        g for g in param_groups if g not in PARAM_GROUP_ORDER
    ]

    color_map = {}
    for i, g in enumerate(ordered_groups):
        color_map[g] = colors[i % len(colors)]
    return color_map


def save_figure(fig: plt.Figure, out_dir: Path, filename: str):
    """Save figure as PNG only in the given directory."""
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / f"{filename}.png"
    fig.tight_layout()
    fig.savefig(png_path, bbox_inches="tight")
    plt.close(fig)



def to_numeric_columns(df: pd.DataFrame, exclude=None) -> pd.DataFrame:
    """Convert all columns except some to numeric where possible."""
    if exclude is None:
        exclude = []
    for col in df.columns:
        if col not in exclude:
            df[col] = pd.to_numeric(df[col], errors="ignore")
    return df


# ---------------------------------------------------------------------------
# Boiler-level plots
# ---------------------------------------------------------------------------

def create_boiler_plots(df: pd.DataFrame, out_dir: Path):
    """
    Create boiler KPI plots:

    1) Flows and steam capacity vs parameter
    2) Thermal performance vs parameter
    3) Temperatures and pressure drops vs parameter
    4) Parallel coordinates overview (all key variables)
    """
    # Clean numeric columns
    df = to_numeric_columns(
        df,
        exclude=["run", "param_group", "param_value"],
    )

    # Exclude rows without a param_value for param-based plots
    df_param = df.copy()
    df_param["param_value_num"] = pd.to_numeric(df_param["param_value"], errors="coerce")
    df_param = df_param.dropna(subset=["param_value_num"])

    param_groups = df_param["param_group"].unique()
    markers = ["o", "s", "D", "^", "v", "P", "X", "*"]
    marker_map = {g: markers[i % len(markers)] for i, g in enumerate(param_groups)}

    color_map = get_param_color_map(param_groups)

    # Human-readable parameter label by group
    param_label_map = {
        "excess_air": "Excess air ratio [-]",
        "fuel_flow": "Fuel mass flow set-point [kg/s]",
        "water_pressure": "Feedwater pressure [bar]",
        "control": "Case index [-]",
    }

    # Helper: label for x-axis based on param_group in each subplot
    def get_param_label(group: str) -> str:
        return param_label_map.get(group, "Parameter value [-]")

    # --------------------------------------------------------------
    # 1) Flows and capacity vs parameter (4 subplots in one figure)
    # --------------------------------------------------------------
    flow_vars = [
        ("fuel mass flow[kg/s]", "Fuel mass flow [kg/s]"),
        ("air flow[kg/s]", "Air flow [kg/s]"),
        ("water flow[kg/s]", "Water flow [kg/s]"),
        ("steam capacity[t/h]", "Steam capacity [t/h]"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), sharex=False)
    axes = axes.ravel()

    for ax, (col, ylabel) in zip(axes, flow_vars):
        for group in param_groups:
            d = df_param[df_param["param_group"] == group].sort_values("param_value_num")
            if d.empty:
                continue
            ax.plot(
                d["param_value_num"],
                d[col],
                marker=marker_map[group],
                linestyle="-",
                label=group,
                alpha=0.9,
                color=color_map[group],
            )
        ax.set_ylabel(ylabel)
        ax.grid(True)

    # Put a generic x-label on bottom axes
    axes[2].set_xlabel("Parameter value [-]")
    axes[3].set_xlabel("Parameter value [-]")

    # Single legend outside
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=min(len(labels), 4),
        frameon=False,
        bbox_to_anchor=(0.5, 1.03),
    )
    fig.suptitle("Boiler: Flows and Steam Capacity vs Parameter", y=1.05)
    save_figure(fig, out_dir, "boiler_flows_and_capacity_vs_param")

    # --------------------------------------------------------------
    # 2) Thermal performance vs parameter (4 subplots)
    # --------------------------------------------------------------
    perf_vars = [
        ("Q_in total[MW]", "Total heat input $Q_\\mathrm{in}$ [MW]"),
        ("Q_useful[MW]", "Useful heat $Q_\\mathrm{useful}$ [MW]"),
        ("P-LHV[MW]", "Thermal input based on LHV [MW]"),
        ("UA[MW/K]", "Overall UA [MW/K]"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), sharex=False)
    axes = axes.ravel()

    for ax, (col, ylabel) in zip(axes, perf_vars):
        for group in param_groups:
            d = df_param[df_param["param_group"] == group].sort_values("param_value_num")
            if d.empty:
                continue
            ax.plot(
                d["param_value_num"],
                d[col],
                marker=marker_map[group],
                linestyle="-",
                label=group,
                alpha=0.9,
                color=color_map[group],
            )
        ax.set_ylabel(ylabel)
        ax.grid(True)

    axes[2].set_xlabel("Parameter value [-]")
    axes[3].set_xlabel("Parameter value [-]")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=min(len(labels), 4),
        frameon=False,
        bbox_to_anchor=(0.5, 1.03),
    )
    fig.suptitle("Boiler: Thermal Performance vs Parameter", y=1.05)
    save_figure(fig, out_dir, "boiler_thermal_performance_vs_param")

    # --------------------------------------------------------------
    # 3) Temperatures and pressure drops vs parameter (4 subplots)
    # --------------------------------------------------------------
    temp_press_vars = [
        ("Tad[°C]", "Adiabatic flame temperature $T_\\mathrm{ad}$ [°C]"),
        ("stack temperature[°C]", "Stack gas temperature [°C]"),
        ("pressue drop fric total[Pa]", "Total frictional pressure drop [Pa]"),
        ("pressure drop total[Pa]", "Total pressure drop [Pa]"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), sharex=False)
    axes = axes.ravel()

    for ax, (col, ylabel) in zip(axes, temp_press_vars):
        for group in param_groups:
            d = df_param[df_param["param_group"] == group].sort_values("param_value_num")
            if d.empty:
                continue
            ax.plot(
                d["param_value_num"],
                d[col],
                marker=marker_map[group],
                linestyle="-",
                label=group,
                alpha=0.9,
                color=color_map[group],
            )
        ax.set_ylabel(ylabel)
        ax.grid(True)

    axes[2].set_xlabel("Parameter value [-]")
    axes[3].set_xlabel("Parameter value [-]")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=min(len(labels), 4),
        frameon=False,
        bbox_to_anchor=(0.5, 1.03),
    )
    fig.suptitle("Boiler: Temperatures and Pressure Drops vs Parameter", y=1.05)
    save_figure(fig, out_dir, "boiler_temperatures_and_pressure_drops_vs_param")

    # --------------------------------------------------------------
    # 4) Boiler parallel-coordinates style overview
    #    (not true parallel-coordinates, but a compact multi-axis overview)
    # --------------------------------------------------------------
    # Select key numeric variables
    key_cols = [
        "fuel mass flow[kg/s]",
        "air flow[kg/s]",
        "excess air ratio[-]",
        "water flow[kg/s]",
        "steam capacity[t/h]",
        "eta direct[-]",
        "eta indirect[-]",
        "UA[MW/K]",
        "Q_in total[MW]",
        "Q_useful[MW]",
        "Tad[°C]",
        "stack temperature[°C]",
    ]
    subset = df[key_cols + ["run"]].copy()

    # Normalize each variable for plotting on common scale [0, 1]
    norm = (subset[key_cols] - subset[key_cols].min()) / (
        subset[key_cols].max() - subset[key_cols].min()
    )

    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    x_positions = range(len(key_cols))

    for _, row in norm.iterrows():
        ax.plot(x_positions, row[key_cols].values, alpha=0.4, linewidth=1.0,color=color_map[group],)

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(
        [
            "Fuel\n[kg/s]",
            "Air\n[kg/s]",
            "λ [-]",
            "Water\n[kg/s]",
            "Steam\n[t/h]",
            "η_direct\n[-]",
            "η_indirect\n[-]",
            "UA\n[MW/K]",
            "Q_in\n[MW]",
            "Q_useful\n[MW]",
            "T_ad\n[°C]",
            "T_stack\n[°C]",
        ],
        rotation=0,
    )
    ax.set_ylabel("Normalised value [-]")
    ax.set_title("Boiler: Normalised KPI Overview (All Runs)")
    ax.grid(True, axis="x")
    save_figure(fig, out_dir, "boiler_kpi_parallel_overview")


# ---------------------------------------------------------------------------
# HX stage-level plots
# ---------------------------------------------------------------------------

def create_hx_plots(df: pd.DataFrame, out_dir: Path):
    """
    Create HX stage-wise plots:

    1) Temperatures vs stage (gas + water)
    2) Enthalpies vs stage (gas + water)
    3) Pressures, velocities, and pressure drops vs stage
    4) Heat transfer (Q) and UA vs stage
    """
    # Convert columns to numeric where possible
    df = to_numeric_columns(
        df,
        exclude=["run", "param_group", "param_value", "stage", "kind"],
    )

    # Extract stage index as integer from "HX_1" etc.
    df = df.copy()
    df["stage_index"] = (
        df["stage"].astype(str).str.extract(r"HX_(\d+)")[0].astype(int)
    )

    # Color by param_group, consistent with boiler plots
    param_groups = df["param_group"].unique()
    color_map = get_param_color_map(param_groups)

    # Map each run to its dominant param_group (in case of duplicates, use mode)
    run_to_group = df.groupby("run")["param_group"].agg(lambda x: x.mode()[0])

    # One marker per run; same run keeps same marker in all HX plots
    runs = df["run"].unique()
    markers = ["o", "s", "D", "^", "v", "P", "X", "*", "h", "d"]
    marker_map = {r: markers[i % len(markers)] for i, r in enumerate(runs)}


    # --------------------------------------------------------------
    # 1) Temperatures vs stage (gas + water)
    # --------------------------------------------------------------
    temp_cols = [
        ("gas in temp[°C]", "Gas in temperature [°C]"),
        ("gas out temp[°C]", "Gas out temperature [°C]"),
        ("water in temp[°C]", "Water in temperature [°C]"),
        ("water out temp[°C]", "Water out temperature [°C]"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), sharex=True)
    axes = axes.ravel()

    for ax, (col, ylabel) in zip(axes, temp_cols):
        for run in runs:
            d = df[df["run"] == run].sort_values("stage_index")
            group = run_to_group[run]
            ax.plot(
                d["stage_index"],
                d[col],
                marker=marker_map[run],
                linestyle="-",
                alpha=0.8,
                color=color_map[group],
            )
        ax.set_ylabel(ylabel)
        ax.grid(True)

    for ax in axes[2:]:
        ax.set_xlabel("HX stage index [-]")

    # Legend: show runs with their marker and color (group color)
    handles = [
        plt.Line2D(
            [], [],
            marker=marker_map[r],
            linestyle="-",
            label=r,
            color=color_map[run_to_group[r]],
        )
        for r in runs
    ]
    fig.legend(
        handles,
        [r for r in runs],
        loc="upper center",
        ncol=min(len(runs), 4),
        frameon=False,
        bbox_to_anchor=(0.5, 1.03),
    )
    fig.suptitle("HX Train: Gas/Water Temperatures vs Stage", y=1.05)
    save_figure(fig, out_dir, "hx_temperatures_vs_stage")


    # --------------------------------------------------------------
    # 2) Enthalpies vs stage (gas + water)
    # --------------------------------------------------------------
    h_cols = [
        ("gas in enthalpy[kJ/kg]", "Gas in enthalpy [kJ/kg]"),
        ("gas out enthalpy[kJ/kg]", "Gas out enthalpy [kJ/kg]"),
        ("water in enthalpy[kJ/kg]", "Water in enthalpy [kJ/kg]"),
        ("water out enthalpy[kJ/kg]", "Water out enthalpy [kJ/kg]"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), sharex=True)
    axes = axes.ravel()

    for ax, (col, ylabel) in zip(axes, h_cols):
        for run in runs:
            d = df[df["run"] == run].sort_values("stage_index")
            group = run_to_group[run]
            ax.plot(
                d["stage_index"],
                d[col],
                marker=marker_map[run],
                linestyle="-",
                alpha=0.8,
                color=color_map[group],
            )
        ax.set_ylabel(ylabel)
        ax.grid(True)

    for ax in axes[2:]:
        ax.set_xlabel("HX stage index [-]")

    handles = [
        plt.Line2D(
            [], [],
            marker=marker_map[r],
            linestyle="-",
            label=r,
            color=color_map[run_to_group[r]],
        )
        for r in runs
    ]
    fig.legend(
        handles,
        [r for r in runs],
        loc="upper center",
        ncol=min(len(runs), 4),
        frameon=False,
        bbox_to_anchor=(0.5, 1.03),
    )
    fig.suptitle("HX Train: Gas/Water Enthalpies vs Stage", y=1.05)
    save_figure(fig, out_dir, "hx_enthalpies_vs_stage")


    # --------------------------------------------------------------
    # 3) Pressures, velocities, and pressure drops vs stage
    # --------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), sharex=True)
    ax_p_gas = axes[0, 0]
    ax_p_water = axes[0, 1]
    ax_v = axes[1, 0]
    ax_dp = axes[1, 1]

    for run in runs:
        d = df[df["run"] == run].sort_values("stage_index")
        group = run_to_group[run]
        c = color_map[group]
        m = marker_map[run]

        # Gas pressures in/out
        ax_p_gas.plot(
            d["stage_index"],
            d["gas in pressure[pa]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )
        ax_p_gas.plot(
            d["stage_index"],
            d["gas out pressure[pa]"],
            marker=m,
            linestyle="--",
            alpha=0.8,
            color=c,
        )

        # Water pressure
        ax_p_water.plot(
            d["stage_index"],
            d["water pressure[pa]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )

        # Velocities
        ax_v.plot(
            d["stage_index"],
            d["gas avg velocity[m/s]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )
        ax_v.plot(
            d["stage_index"],
            d["water avg velocity[m/s]"],
            marker=m,
            linestyle="--",
            alpha=0.8,
            color=c,
        )

        # Pressure drops
        ax_dp.plot(
            d["stage_index"],
            d["pressure drop fric[pa]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )
        ax_dp.plot(
            d["stage_index"],
            d["pressure drop minor[pa]"],
            marker=m,
            linestyle="--",
            alpha=0.8,
            color=c,
        )
        ax_dp.plot(
            d["stage_index"],
            d["pressure drop total[pa]"],
            marker=m,
            linestyle=":",
            alpha=0.8,
            color=c,
        )


    ax_p_gas.set_ylabel("Gas pressure [Pa]")
    ax_p_water.set_ylabel("Water pressure [Pa]")
    ax_v.set_ylabel("Average velocity [m/s]")
    ax_dp.set_ylabel("Pressure drops [Pa]")

    ax_v.set_xlabel("HX stage index [-]")
    ax_dp.set_xlabel("HX stage index [-]")

    for ax in axes.ravel():
        ax.grid(True)

    # Legends: custom for line styles
    gas_p_handles = [
        plt.Line2D([], [], linestyle="-", color="black", label="Gas in"),
        plt.Line2D([], [], linestyle="--", color="black", label="Gas out"),
    ]
    vel_handles = [
        plt.Line2D([], [], linestyle="-", color="black", label="Gas"),
        plt.Line2D([], [], linestyle="--", color="black", label="Water"),
    ]
    dp_handles = [
        plt.Line2D([], [], linestyle="-", color="black", label="Friction"),
        plt.Line2D([], [], linestyle="--", color="black", label="Minor"),
        plt.Line2D([], [], linestyle=":", color="black", label="Total"),
    ]

    ax_p_gas.legend(handles=gas_p_handles, frameon=False)
    ax_v.legend(handles=vel_handles, frameon=False)
    ax_dp.legend(handles=dp_handles, frameon=False)

    fig.suptitle("HX Train: Pressures, Velocities, and Pressure Drops vs Stage", y=1.03)
    save_figure(fig, out_dir, "hx_pressures_velocities_dp_vs_stage")

    # --------------------------------------------------------------
    # 4) Heat transfer and UA vs stage
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), sharex=True)
    ax_qconv = axes[0, 0]
    ax_qrad = axes[0, 1]
    ax_qtot = axes[1, 0]
    ax_ua_steam = axes[1, 1]

    for run in runs:
        d = df[df["run"] == run].sort_values("stage_index")
        group = run_to_group[run]
        c = color_map[group]
        m = marker_map[run]

        ax_qconv.plot(
            d["stage_index"],
            d["Q conv[MW]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )
        ax_qrad.plot(
            d["stage_index"],
            d["Q rad[MW]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )
        ax_qtot.plot(
            d["stage_index"],
            d["Q total[MW]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )

        ax_ua_steam.plot(
            d["stage_index"],
            d["UA[MW/K]"],
            marker=m,
            linestyle="-",
            alpha=0.8,
            color=c,
        )

    ax_qconv.set_ylabel("Convective heat $Q_\\mathrm{conv}$ [MW]")
    ax_qrad.set_ylabel("Radiative heat $Q_\\mathrm{rad}$ [MW]")
    ax_qtot.set_ylabel("Total heat $Q_\\mathrm{total}$ [MW]")
    ax_ua_steam.set_ylabel("UA [MW/K]")

    for ax in axes[2:]:
        ax.set_xlabel("HX stage index [-]")

    for ax in axes.ravel():
        ax.grid(True)

    fig.suptitle("HX Train: Heat Transfer and UA vs Stage", y=1.03)
    save_figure(fig, out_dir, "hx_heat_transfer_and_UA_vs_stage")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    set_thesis_style()

    # Paths (relative to where plotty.py is executed)
    base = Path(".")
    boiler_csv = base / "results" / "summary" / "boiler_kpis_all_runs.csv"
    stages_csv = base / "results" / "summary" / "stages_summary_all_runs.csv"
    plots_dir = base / "results" / "plots" / "plotty"

    # Load data
    df_boiler = pd.read_csv(boiler_csv)
    df_stages = pd.read_csv(stages_csv)

    # Generate plots
    create_boiler_plots(df_boiler, plots_dir)
    create_hx_plots(df_stages, plots_dir)


if __name__ == "__main__":
    main()
