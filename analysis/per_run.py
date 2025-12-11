from pathlib import Path
import sys
from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt

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

def load_data(csv_path: str) -> pd.DataFrame:
    csv_file = Path(csv_path)
    df = pd.read_csv(csv_file)
    df["param_value"] = pd.to_numeric(df["param_value"], errors="coerce")
    return df

def _get_marker(param_group: str):
    return style_markers.get(param_group, None)


def plot_Qin_Quseful(ax, df_group: pd.DataFrame, param_group: str) -> None:
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
    df_plot = df_group.dropna(subset=["param_value"]).sort_values("param_value")
    marker = _get_marker(param_group)

    x = df_plot["param_value"]
    y_water = df_plot["water flow[kg/s]"]
    y_steam = df_plot["steam capacity[t/h]"]

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

    lines = [line_water, line_steam]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc="best", framealpha=0.8)


def plot_stack_pressure(ax, df_group: pd.DataFrame, param_group: str) -> None:
    df_plot = df_group.dropna(subset=["param_value"]).sort_values("param_value")
    marker = _get_marker(param_group)

    x = df_plot["param_value"]
    y_stack = df_plot["stack temperature[°C]"]
    y_dp = df_plot["pressure drop total[Pa]"].abs()

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

    lines = [line_stack, line_dp]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc="best", framealpha=0.8)

def generate_overall_kpi_figure(csv_path: str, output_dir: str = "figures") -> None:
    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = df.dropna(subset=["param_value"]).copy()

    kpi_defs = [
        {"column": "Tad[°C]",                 "ylabel": "Tad [°C]"},
        {"column": "stack temperature[°C]",   "ylabel": "Stack temperature [°C]"},
        {"column": "air flow[kg/s]",          "ylabel": "Air flow [kg/s]"},
        {"column": "water flow[kg/s]",        "ylabel": "Water flow [kg/s]"},
        {"column": "Q_in total[MW]",          "ylabel": r"Heat input $Q_{in}$ [MW]"},
        {"column": "steam capacity[t/h]",     "ylabel": "Steam capacity [t/h]"},
        {"column": "pressure drop total[Pa]", "ylabel": "Total pressure drop [Pa]", "abs": True},
        {"column": "eta direct[-]",           "ylabel": "Direct efficiency [-]"},
    ]

    fig, axes = plt.subplots(4, 2, figsize=(9, 10))
    axes_flat = axes.flatten()

    for ax, kpi in zip(axes_flat, kpi_defs):
        ax.set_xlabel("Parameter value [-]")
        ax.set_ylabel(kpi["ylabel"])
        ax.grid(True, which="both")

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

def generate_stage_heat_figure(
    csv_path: str = "results/summary/stages_summary_all_runs.csv",
    output_dir: str = "figures",
) -> None:

    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if df["stage"].dtype == object:
        df["stage_index"] = (
            df["stage"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .astype(int)
        )
    else:
        df["stage_index"] = df["stage"].astype(int)

    df = df.dropna(subset=["stage_index"]).copy()

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    ax_Tg    = axes[0, 0]
    ax_duty  = axes[0, 1]
    ax_Qrad  = axes[1, 0]
    ax_Qconv = axes[1, 1]

    stage_ticks = sorted(df["stage_index"].unique())

    for ax in (ax_Tg, ax_duty, ax_Qrad, ax_Qconv):
        ax.set_xlabel("Stage [-]")
        ax.set_xticks(stage_ticks)
        ax.grid(True, which="both")

    ax_Tg.set_ylabel("Gas outlet temperature [°C]")
    ax_duty.set_ylabel("Stage duty $Q_{\\mathrm{stage}}$ [MW]")
    ax_Qrad.set_ylabel("$Q_{\\mathrm{rad}}$ [MW]")
    ax_Qconv.set_ylabel("$Q_{\\mathrm{conv}}$ [MW]")

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

    for param_group, df_pg in df.groupby("param_group"):
        marker = _get_marker(param_group) or "o"
        color = pg_color[param_group]
        line_style = pg_line[param_group]
        lw = 0.7

        for run_name, df_run in df_pg.groupby("run"):
            df_run_sorted = df_run.sort_values("stage_index")
            x     = df_run_sorted["stage_index"]
            y_Tg  = df_run_sorted["gas out temp[°C]"]
            y_Q   = df_run_sorted["Q total[MW]"]     # stage duty
            y_Qrad = df_run_sorted["Q rad[MW]"]
            y_Qconv = df_run_sorted["Q conv[MW]"]

            line_Tg, = ax_Tg.plot(
                x,
                y_Tg,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
                label=param_group,
            )

            ax_duty.plot(
                x,
                y_Q,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            ax_Qrad.plot(
                x,
                y_Qrad,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            ax_Qconv.plot(
                x,
                y_Qconv,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            if param_group not in legend_handles:
                legend_handles[param_group] = line_Tg

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

    out_path = out_dir / "stages_heat.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)

def generate_stage_hydraulics_figure(
    csv_path: str = "results/summary/stages_summary_all_runs.csv",
    output_dir: str = "figures",
) -> None:
    
    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if df["stage"].dtype == object:
        df["stage_index"] = (
            df["stage"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .astype(int)
        )
    else:
        df["stage_index"] = df["stage"].astype(int)

    df = df.dropna(subset=["stage_index"]).copy()

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    ax_UA  = axes[0, 0]
    ax_p   = axes[0, 1]
    ax_dp  = axes[1, 0]
    ax_vel = axes[1, 1]

    stage_ticks = sorted(df["stage_index"].unique())

    for ax in (ax_UA, ax_p, ax_dp, ax_vel):
        ax.set_xlabel("Stage [-]")
        ax.set_xticks(stage_ticks)
        ax.grid(True, which="both")

    ax_UA.set_ylabel("Stage conductance $UA$ [MW/K]")
    ax_p.set_ylabel("Gas outlet pressure [Pa]")
    ax_dp.set_ylabel("Total pressure drop [Pa]")
    ax_vel.set_ylabel("Gas average velocity [m/s]")

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

    for param_group, df_pg in df.groupby("param_group"):
        marker = _get_marker(param_group) or "o"
        color = pg_color[param_group]
        line_style = pg_line[param_group]
        lw = 0.7

        for run_name, df_run in df_pg.groupby("run"):
            df_run_sorted = df_run.sort_values("stage_index")
            x     = df_run_sorted["stage_index"]
            y_vel = df_run_sorted["gas avg velocity[m/s]"]
            y_p   = df_run_sorted["gas out pressure[pa]"]
            y_dp  = df_run_sorted["pressure drop total[pa]"].abs()
            y_UA  = df_run_sorted["UA[MW/K]"]

            line_UA, = ax_UA.plot(
                x,
                y_UA,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
                label=param_group,
            )

            ax_p.plot(
                x,
                y_p,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            ax_dp.plot(
                x,
                y_dp,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            ax_vel.plot(
                x,
                y_vel,
                marker=marker,
                linestyle=line_style,
                color=color,
                linewidth=lw,
            )

            if param_group not in legend_handles:
                legend_handles[param_group] = line_UA

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

    out_path = out_dir / "stages_hydraulics.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)

def generate_all_figures(csv_path: str, output_dir: str = "figures") -> None:

    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    grouped = df.groupby("param_group")

    for param_group, df_group in grouped:
        df_group_numeric = df_group.dropna(subset=["param_value"])
        if df_group_numeric["param_value"].nunique(dropna=True) < 2:
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

        safe_group = str(param_group).replace(" ", "_")
        png_path = out_dir / f"performance_{safe_group}.png"

        fig.savefig(png_path, dpi=300)
        plt.close(fig)

if __name__ == "__main__":
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

    generate_all_figures(csv_arg, output_dir=out_arg)

    generate_overall_kpi_figure(csv_arg, output_dir=out_arg)

    stage_csv = "results/summary/stages_summary_all_runs.csv"
    generate_stage_heat_figure(stage_csv, output_dir=out_arg)

    generate_stage_hydraulics_figure(stage_csv, output_dir=out_arg)
