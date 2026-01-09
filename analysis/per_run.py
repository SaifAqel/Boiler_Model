from pathlib import Path
import sys
from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

style_colors: Dict[str, str] = {
    "Q_in": "tab:blue",
    "Q_useful": "tab:orange",
    "eta_direct": "tab:green",
    "eta_indirect": "tab:red",
    "feedwater_flow": "tab:blue",
    "steam_capacity": "tab:orange",
    "stack_temperature": "tab:red",
    "pressure_drop": "tab:purple",
}

style_linestyles: Dict[str, str] = {
    "Q_in": "-",
    "Q_useful": "--",
    "eta_direct": "-",
    "eta_indirect": "--",
    "feedwater_flow": "-",
    "steam_capacity": "--",
    "stack_temperature": "-",
    "pressure_drop": "--",
}

style_markers: Dict[str, str] = {
    "excess_air": "o",
    "fuel_flow": "s",
    "drum_pressure": "D",
    "control": "x",
    "fouling": "^",
}

param_xlabels: Dict[str, str] = {
    "excess_air": "Excess air [-]",
    "fuel_flow": "Fuel flow [kg/s]",
    "drum_pressure": "Drum pressure [bar]",
    "control": "Control case [-]",
    "fouling": "Fouling factor [-]", 
}

def _get_xlabel(param_group: str) -> str:
    return param_xlabels.get(param_group, "Parameter value [-]")

param_group_style = {
    "excess_air":    dict(color="tab:blue",   marker="o", linestyle="-"),
    "fuel_flow":     dict(color="tab:orange", marker="s", linestyle="--"),
    "drum_pressure": dict(color="tab:green",  marker="D", linestyle="-"),
    "control":       dict(color="tab:red",    marker="x", linestyle="-"),
    "fouling":       dict(color="tab:purple", marker="^", linestyle="-."),
}

def _get_pg_style(param_group: str) -> dict:
    return param_group_style.get(
        param_group,
        dict(color="black", marker="o", linestyle="-"),
    )

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

def load_steps_data(csv_path: str) -> pd.DataFrame:
    csv_file = Path(csv_path)
    df = pd.read_csv(csv_file)

    num_cols = [
        "x[m]",
        "gas_T[°C]", "water_T[°C]",
        "gas_P[kPa]", "water_P[kPa]",
        "gas_V[m/s]", "water_V[m/s]",
        "h_gas[W/m^2/K]", "h_water[W/m^2/K]",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


def _sweep_percent(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    smin = s.min()
    smax = s.max()
    if pd.isna(smin) or pd.isna(smax) or smax == smin:
        return pd.Series([0.0] * len(s), index=s.index)
    return (s - smin) / (smax - smin) * 100.0

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
    y_water = df_plot["feedwater flow[kg/s]"]
    y_steam = df_plot["steam capacity[t/h]"]

    line_water, = ax.plot(
        x,
        y_water,
        label="feedwater_flow",
        color=style_colors.get("feedwater_flow", None),
        linestyle=style_linestyles.get("feedwater_flow", "-"),
        marker=marker,
    )
    ax.set_xlabel(_get_xlabel(param_group))
    ax.set_ylabel("feedwater flow [kg/s]")
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
    y_dp = df_plot["pressure drop total[kPa]"].abs()

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
    df_all = df.copy()
    kpi_defs = [
        {"column": "Tad[°C]",                 "ylabel": "Tad [°C]"},
        {"column": "stack temperature[°C]",   "ylabel": "Stack temperature [°C]"},
        {"column": "air flow[kg/s]",          "ylabel": "Air flow [kg/s]"},
        {"column": "feedwater flow[kg/s]",        "ylabel": "feedwater flow [kg/s]"},
        {"column": "Q_in total[MW]",          "ylabel": "Heat input $Q_{in}$ [MW]"},
        {"column": "steam capacity[t/h]",     "ylabel": "Steam capacity [t/h]"},
        {"column": "pressure drop total[kPa]", "ylabel": "Total pressure drop [kPa]", "abs": True},
        {"column": "eta direct[-]",           "ylabel": "Direct efficiency [-]"},
    ]

    fig, axes = plt.subplots(4, 2, figsize=(9, 10))
    axes_flat = axes.flatten()

    for ax in axes_flat:
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 100])
        ax.set_xticklabels(["Min", "Max"])

    for ax, kpi in zip(axes_flat, kpi_defs):
        ax.set_xlabel("Parameter range")
        ax.set_ylabel(kpi["ylabel"])
        ax.grid(True, which="both")

    legend_handles = {}

    for param_group, df_group in df.groupby("param_group"):
        df_group_sorted = df_group.sort_values("param_value")
        x = _sweep_percent(df_group_sorted["param_value"])

        pg_style = _get_pg_style(param_group)
        marker = pg_style["marker"]
        color = pg_style["color"]
        line_style = pg_style["linestyle"]

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

    for ax, kpi in zip(axes_flat, kpi_defs):
        col = kpi["column"]
        if col not in df_all.columns:
            continue

        df_overlay = df_all.dropna(subset=["param_value", col]).copy()
        if kpi.get("abs", False):
            df_overlay[col] = df_overlay[col].abs()

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

def generate_eff_stack_scatter(
    csv_path: str = "results/summary/boiler_kpis_all_runs.csv",
    output_dir: str = "figures",
) -> None:
    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    needed = ["param_group", "stack temperature[°C]", "eta direct[-]", "eta indirect[-]"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns for scatter: {missing}")

    dfp = df.dropna(subset=["stack temperature[°C]", "eta direct[-]", "eta indirect[-]"]).copy()

    fig, ax_dir = plt.subplots(1, 1, figsize=(7.5, 4))

    df_non_control = dfp[dfp["param_group"].astype(str).str.lower() != "control"].copy()
    df_control     = dfp[dfp["param_group"].astype(str).str.lower() == "control"].copy()

    for pg, dpg in df_non_control.groupby("param_group"):
        st = _get_pg_style(str(pg))
        ax_dir.scatter(
            dpg["stack temperature[°C]"],
            dpg["eta direct[-]"],
            label=str(pg),
            color=st["color"],
            marker=st["marker"],
            s=28,
            alpha=0.85,
            zorder=2,
        )

    if not df_control.empty:
        stc = _get_pg_style("control")
        ax_dir.scatter(
            df_control["stack temperature[°C]"],
            df_control["eta direct[-]"],
            label="control",
            color=stc["color"],
            marker=stc["marker"],
            s=60,
            alpha=1.0,
            linewidths=0.6,
            zorder=10,
        )

    ax_dir.set_title("Direct efficiency vs stack temperature")
    ax_dir.set_xlabel("Stack temperature [°C]")
    ax_dir.set_ylabel("Direct efficiency [-] (LHV)")
    ax_dir.grid(True, which="both")

    handles, labels = ax_dir.get_legend_handles_labels()
    if handles:
        ax_dir.legend(
            handles=handles,
            labels=labels,
            loc="best",
            framealpha=0.8,
        )

    fig.tight_layout()

    out_path = out_dir / "scatter_efficiency_vs_stack_temperature_all_runs.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

def generate_stage_combined_control_figure(
    csv_path: str = "results/summary/stages_summary_all_runs.csv",
    output_dir: str = "figures",
) -> None:
    df = load_data(csv_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = df[df["param_group"].astype(str).str.lower() == "control"].copy()
    if df.empty:
        raise ValueError("No rows found for param_group == 'control' in stages summary CSV.")

    if df["stage"].dtype == object:
        df["stage_index"] = (
            df["stage"].astype(str).str.extract(r"(\d+)", expand=False).astype(int)
        )
    else:
        df["stage_index"] = df["stage"].astype(int)

    df = df.dropna(subset=["stage_index"]).copy()

    plot_cols = [
        "gas out temp[°C]",
        "Q total[MW]",
        "Q rad[MW]",
        "Q conv[MW]",
        "UA[MW/K]",
        "gas out pressure[kpa]",
        "pressure drop total[kpa]",
        "gas avg velocity[m/s]",
    ]
    for c in plot_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    fig, axes = plt.subplots(4, 2, figsize=(10, 10))
    ax_Tg   = axes[0, 0]
    ax_Q    = axes[0, 1]
    ax_Qrad = axes[1, 0]
    ax_Qconv= axes[1, 1]
    ax_UA   = axes[2, 0]
    ax_p    = axes[2, 1]
    ax_dp   = axes[3, 0]
    ax_vel  = axes[3, 1]

    stage_ticks = sorted(df["stage_index"].unique())
    for ax in (ax_Tg, ax_Q, ax_Qrad, ax_Qconv, ax_UA, ax_p, ax_dp, ax_vel):
        ax.set_xlabel("Stage [-]")
        ax.set_xticks(stage_ticks)
        ax.grid(True, which="both")

    ax_Tg.set_ylabel("Gas outlet temperature [°C]")
    ax_Q.set_ylabel("Stage duty $Q_{\\mathrm{stage}}$ [MW]")
    ax_Qrad.set_ylabel("$Q_{\\mathrm{rad}}$ [MW]")
    ax_Qconv.set_ylabel("$Q_{\\mathrm{conv}}$ [MW]")
    ax_UA.set_ylabel("Stage conductance $UA$ [MW/K]")
    ax_p.set_ylabel("Gas outlet pressure [kPa]")
    ax_dp.set_ylabel("Total pressure drop [kPa]")
    ax_vel.set_ylabel("Gas average velocity [m/s]")

    st = _get_pg_style("control")
    color = st["color"]
    marker = st["marker"]
    line_style = st["linestyle"]
    lw = 0.9

    for run_name, df_run in df.groupby("run"):
        df_run = df_run.sort_values("stage_index")

        x = df_run["stage_index"]
        y_Tg   = df_run["gas out temp[°C]"]
        y_Q    = df_run["Q total[MW]"]
        y_Qrad = df_run["Q rad[MW]"]
        y_Qconv= df_run["Q conv[MW]"]
        y_UA   = df_run["UA[MW/K]"]
        y_p    = df_run["gas out pressure[kpa]"]
        y_dp   = df_run["pressure drop total[kpa]"].abs()
        y_vel  = df_run["gas avg velocity[m/s]"]

        ax_Tg.plot(x, y_Tg,   marker=marker, linestyle=line_style, color=color, linewidth=lw, label="Control case")
        ax_Q.plot(x, y_Q,     marker=marker, linestyle=line_style, color=color, linewidth=lw)
        ax_Qrad.plot(x, y_Qrad, marker=marker, linestyle=line_style, color=color, linewidth=lw)
        ax_Qconv.plot(x, y_Qconv, marker=marker, linestyle=line_style, color=color, linewidth=lw)
        ax_UA.plot(x, y_UA,   marker=marker, linestyle=line_style, color=color, linewidth=lw)
        ax_p.plot(x, y_p,     marker=marker, linestyle=line_style, color=color, linewidth=lw)
        ax_dp.plot(x, y_dp,   marker=marker, linestyle=line_style, color=color, linewidth=lw)
        ax_vel.plot(x, y_vel, marker=marker, linestyle=line_style, color=color, linewidth=lw)

    handles, labels = ax_Tg.get_legend_handles_labels()
    if handles:
        fig.legend(
            handles=handles,
            labels=labels,
            loc="lower center",
            ncol=min(len(labels), 4),
            framealpha=0.8,
            bbox_to_anchor=(0.5, 0.02),
        )

    fig.tight_layout(rect=(0.0, 0.06, 1.0, 0.98))

    out_path = out_dir / "stages_control_combined_8plots.png"
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

    generate_eff_stack_scatter(csv_arg, output_dir=out_arg)

    stage_csv = "results/summary/stages_summary_all_runs.csv"
    generate_stage_combined_control_figure(stage_csv, output_dir=out_arg)
