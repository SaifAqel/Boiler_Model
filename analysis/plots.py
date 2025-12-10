#!/usr/bin/env python3
"""
plot.py

Generate boiler-level and HX-level plots for all runs.

Input CSVs (fixed paths):
    results\summary\boiler_kpis_all_runs.csv
    results\summary\stages_summary_all_runs.csv

Output directory:
    results\plots

Dependencies:
    pip install pandas matplotlib numpy
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Config: paths (adapt if needed)
# ---------------------------------------------------------------------------

BOILER_CSV = Path(r"results/summary/boiler_kpis_all_runs.csv")
HX_CSV = Path(r"results/summary/stages_summary_all_runs.csv")
OUTDIR = Path(r"results/plots")


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def ensure_outdir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def rename_boiler_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "fuel mass flow[kg/s]": "fuel_flow",
        "air flow[kg/s]": "air_flow",
        "excess air ratio[-]": "excess_air_ratio",
        "water flow[kg/s]": "water_flow",
        "steam capacity[t/h]": "steam_capacity",
        "eta direct[-]": "eta_direct",
        "eta indirect[-]": "eta_indirect",
        "UA[MW/K]": "UA",
        "Q_in total[MW]": "Q_in_total",
        "Q_useful[MW]": "Q_useful",
        "pressue drop fric total[Pa]": "dp_fric_total",
        "pressure drop minor total[Pa]": "dp_minor_total",
        "pressure drop total[Pa]": "dp_total",
        "LHV[kJ/kg]": "LHV",
        "P-LHV[MW]": "P_LHV",
        "Tad[°C]": "Tad",
        "stack temperature[°C]": "stack_temp",
    }
    return df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})


def rename_hx_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "gas in pressure[pa]": "p_gas_in",
        "gas in temp[°C]": "T_gas_in",
        "gas in enthalpy[kJ/kg]": "h_gas_in",
        "gas out pressure[pa]": "p_gas_out",
        "gas out temp[°C]": "T_gas_out",
        "gas out enthalpy[kJ/kg]": "h_gas_out",
        "water pressure[pa]": "p_water",
        "water in temp[°C]": "T_water_in",
        "water in enthalpy[kJ/kg]": "h_water_in",
        "water out temp[°C]": "T_water_out",
        "water out enthalpy[kJ/kg]": "h_water_out",
        "gas avg velocity[m/s]": "v_gas",
        "water avg velocity[m/s]": "v_water",
        "pressure drop fric[pa]": "dp_fric",
        "pressure drop minor[pa]": "dp_minor",
        "pressure drop total[pa]": "dp_total",
        "Q conv[MW]": "Q_conv",
        "Q rad[MW]": "Q_rad",
        "Q total[MW]": "Q_total",
        "UA[MW/K]": "UA",
        "steam capacity[t/h]": "steam_capacity",
    }
    df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})

    # Add stage_index (1..N) from "HX_1" etc.
    if "stage" in df.columns:
        df["stage_index"] = (
            df["stage"].astype(str).str.extract(r"(\d+)", expand=False).astype(int)
        )
    return df


# ---------------------------------------------------------------------------
# Boiler-level plots
# ---------------------------------------------------------------------------

def plot_excess_air_sweep(boiler: pd.DataFrame, outdir: Path):
    df = boiler[boiler["param_group"] == "excess_air"].copy()
    if df.empty:
        return
    df = df.sort_values("param_value")
    x = df["param_value"]

    # 1) η_direct & η_indirect vs excess air
    fig, ax = plt.subplots()
    ax.plot(x, df["eta_direct"], marker="o", label="eta_direct")
    ax.plot(x, df["eta_indirect"], marker="s", label="eta_indirect")
    ax.set_xlabel("Excess air ratio [-]")
    ax.set_ylabel("Efficiency [-]")
    ax.set_title("Efficiencies vs excess air")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "excess_air_efficiencies.png", dpi=200)
    plt.close(fig)

    # 2) Q_useful & Q_in_total vs excess air
    fig, ax = plt.subplots()
    ax.plot(x, df["Q_useful"], marker="o", label="Q_useful [MW]")
    ax.plot(x, df["Q_in_total"], marker="s", label="Q_in_total [MW]")
    ax.set_xlabel("Excess air ratio [-]")
    ax.set_ylabel("Heat rate [MW]")
    ax.set_title("Heat input and useful heat vs excess air")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "excess_air_Q.png", dpi=200)
    plt.close(fig)

    # 3) Tad & stack temperature
    fig, ax = plt.subplots()
    ax.plot(x, df["Tad"], marker="o", label="Tad [°C]")
    ax.plot(x, df["stack_temp"], marker="s", label="Stack T [°C]")
    ax.set_xlabel("Excess air ratio [-]")
    ax.set_ylabel("Temperature [°C]")
    ax.set_title("Flame and stack temperature vs excess air")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "excess_air_temperatures.png", dpi=200)
    plt.close(fig)

    # 4) Steam capacity
    fig, ax = plt.subplots()
    ax.plot(x, df["steam_capacity"], marker="o")
    ax.set_xlabel("Excess air ratio [-]")
    ax.set_ylabel("Steam capacity [t/h]")
    ax.set_title("Steam capacity vs excess air")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(outdir / "excess_air_steam_capacity.png", dpi=200)
    plt.close(fig)

    # 5) UA & total pressure drop
    fig, ax1 = plt.subplots()
    ax1.plot(x, df["UA"], marker="o", label="UA [MW/K]")
    ax1.set_xlabel("Excess air ratio [-]")
    ax1.set_ylabel("UA [MW/K]")
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.plot(x, df["dp_total"], marker="s", color="tab:red", label="dp_total [Pa]")
    ax2.set_ylabel("Total pressure drop [Pa]")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")
    ax1.set_title("UA and total pressure drop vs excess air")
    fig.tight_layout()
    fig.savefig(outdir / "excess_air_UA_dp.png", dpi=200)
    plt.close(fig)


def plot_fuel_flow_sweep(boiler: pd.DataFrame, outdir: Path):
    df = boiler[boiler["param_group"] == "fuel_flow"].copy()
    if df.empty:
        return
    df = df.sort_values("fuel_flow")
    x = df["fuel_flow"]

    # 1) η vs fuel flow
    fig, ax = plt.subplots()
    ax.plot(x, df["eta_direct"], marker="o", label="eta_direct")
    ax.plot(x, df["eta_indirect"], marker="s", label="eta_indirect")
    ax.set_xlabel("Fuel mass flow [kg/s]")
    ax.set_ylabel("Efficiency [-]")
    ax.set_title("Efficiencies vs fuel flow")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "fuel_flow_efficiencies.png", dpi=200)
    plt.close(fig)

    # 2) Q_useful & Q_in_total vs fuel flow
    fig, ax = plt.subplots()
    ax.plot(x, df["Q_useful"], marker="o", label="Q_useful [MW]")
    ax.plot(x, df["Q_in_total"], marker="s", label="Q_in_total [MW]")
    ax.set_xlabel("Fuel mass flow [kg/s]")
    ax.set_ylabel("Heat rate [MW]")
    ax.set_title("Heat input and useful heat vs fuel flow")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "fuel_flow_Q.png", dpi=200)
    plt.close(fig)

    # 3) Steam capacity vs fuel flow
    fig, ax = plt.subplots()
    ax.plot(x, df["steam_capacity"], marker="o")
    ax.set_xlabel("Fuel mass flow [kg/s]")
    ax.set_ylabel("Steam capacity [t/h]")
    ax.set_title("Steam capacity vs fuel flow")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(outdir / "fuel_flow_steam_capacity.png", dpi=200)
    plt.close(fig)

    # 4) Tad & stack temperature
    fig, ax = plt.subplots()
    ax.plot(x, df["Tad"], marker="o", label="Tad [°C]")
    ax.plot(x, df["stack_temp"], marker="s", label="Stack T [°C]")
    ax.set_xlabel("Fuel mass flow [kg/s]")
    ax.set_ylabel("Temperature [°C]")
    ax.set_title("Temperatures vs fuel flow")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "fuel_flow_temperatures.png", dpi=200)
    plt.close(fig)

    # 5) Pressure drop total vs fuel flow
    fig, ax = plt.subplots()
    ax.plot(x, df["dp_total"], marker="o")
    ax.set_xlabel("Fuel mass flow [kg/s]")
    ax.set_ylabel("Total pressure drop [Pa]")
    ax.set_title("Total pressure drop vs fuel flow")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(outdir / "fuel_flow_dp_total.png", dpi=200)
    plt.close(fig)

    # 6) Specific useful heat and specific steam
    fig, ax = plt.subplots()
    q_specific = df["Q_useful"] / df["fuel_flow"]
    steam_specific = df["steam_capacity"] / df["fuel_flow"]
    ax.plot(x, q_specific, marker="o", label="Q_useful / fuel [MW/(kg/s)]")
    ax.set_xlabel("Fuel mass flow [kg/s]")
    ax.set_ylabel("Q_useful / fuel")
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.plot(x, steam_specific, marker="s", color="tab:red",
             label="steam / fuel [t/h per kg/s]")
    ax2.set_ylabel("Steam / fuel [t/h per kg/s]")

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="best")
    ax.set_title("Specific useful heat and steam vs fuel flow")
    fig.tight_layout()
    fig.savefig(outdir / "fuel_flow_specifics.png", dpi=200)
    plt.close(fig)


def plot_water_pressure_sweep(boiler: pd.DataFrame, outdir: Path):
    df = boiler[boiler["param_group"] == "water_pressure"].copy()
    if df.empty:
        return
    df = df.sort_values("param_value")
    x = df["param_value"]

    # 1) η vs water pressure
    fig, ax = plt.subplots()
    ax.plot(x, df["eta_direct"], marker="o", label="eta_direct")
    ax.plot(x, df["eta_indirect"], marker="s", label="eta_indirect")
    ax.set_xlabel("Water/steam pressure [bar]")
    ax.set_ylabel("Efficiency [-]")
    ax.set_title("Efficiencies vs water pressure")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "water_pressure_efficiencies.png", dpi=200)
    plt.close(fig)

    # 2) Steam capacity vs water pressure
    fig, ax = plt.subplots()
    ax.plot(x, df["steam_capacity"], marker="o")
    ax.set_xlabel("Water/steam pressure [bar]")
    ax.set_ylabel("Steam capacity [t/h]")
    ax.set_title("Steam capacity vs water pressure")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(outdir / "water_pressure_steam_capacity.png", dpi=200)
    plt.close(fig)

    # 3) Stack temperature vs water pressure
    fig, ax = plt.subplots()
    ax.plot(x, df["stack_temp"], marker="o")
    ax.set_xlabel("Water/steam pressure [bar]")
    ax.set_ylabel("Stack temperature [°C]")
    ax.set_title("Stack temperature vs water pressure")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(outdir / "water_pressure_stack_temp.png", dpi=200)
    plt.close(fig)

    # 4) UA and dp_total vs water pressure
    fig, ax1 = plt.subplots()
    ax1.plot(x, df["UA"], marker="o", label="UA [MW/K]")
    ax1.set_xlabel("Water/steam pressure [bar]")
    ax1.set_ylabel("UA [MW/K]")
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.plot(x, df["dp_total"], marker="s", color="tab:red", label="dp_total [Pa]")
    ax2.set_ylabel("Total pressure drop [Pa]")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")
    ax1.set_title("UA and total pressure drop vs water pressure")
    fig.tight_layout()
    fig.savefig(outdir / "water_pressure_UA_dp.png", dpi=200)
    plt.close(fig)


def plot_boiler_cross_plots(boiler: pd.DataFrame, outdir: Path):
    df = boiler.copy()
    if df.empty:
        return

    # 1) eta_direct vs stack_temp, colored by param_group
    fig, ax = plt.subplots()
    groups = df["param_group"].unique()
    for g in groups:
        gdf = df[df["param_group"] == g]
        ax.scatter(gdf["stack_temp"], gdf["eta_direct"], label=g)
    ax.set_xlabel("Stack temperature [°C]")
    ax.set_ylabel("eta_direct [-]")
    ax.set_title("eta_direct vs stack temperature")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "cross_eta_vs_stack_temp.png", dpi=200)
    plt.close(fig)

    # 2) Q_useful vs dp_total
    fig, ax = plt.subplots()
    for g in groups:
        gdf = df[df["param_group"] == g]
        ax.scatter(gdf["dp_total"], gdf["Q_useful"], label=g)
    ax.set_xlabel("Total pressure drop [Pa]")
    ax.set_ylabel("Q_useful [MW]")
    ax.set_title("Q_useful vs total pressure drop")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / "cross_Q_vs_dp.png", dpi=200)
    plt.close(fig)

    # 3) steam_capacity vs eta_direct colored by param_group
    fig, ax = plt.subplots()
    colors, labels = pd.factorize(df["param_group"])
    sc = ax.scatter(df["steam_capacity"], df["eta_direct"], c=colors, cmap="tab10")
    ax.set_xlabel("Steam capacity [t/h]")
    ax.set_ylabel("eta_direct [-]")
    ax.set_title("eta_direct vs steam capacity")
    ax.grid(True)
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_ticks(range(len(labels)))
    cbar.set_ticklabels(labels)
    fig.tight_layout()
    fig.savefig(outdir / "cross_eta_vs_steam_capacity.png", dpi=200)
    plt.close(fig)


def make_boiler_plots(boiler: pd.DataFrame, outdir: Path):
    outdir = ensure_outdir(outdir / "boiler")
    plot_excess_air_sweep(boiler, outdir)
    plot_fuel_flow_sweep(boiler, outdir)
    plot_water_pressure_sweep(boiler, outdir)
    plot_boiler_cross_plots(boiler, outdir)


# ---------------------------------------------------------------------------
# HX-level plots
# ---------------------------------------------------------------------------

def plot_hx_profile_for_run(hx: pd.DataFrame, run: str, outdir: Path):
    df = hx[hx["run"] == run].copy()
    if df.empty:
        return
    df = df.sort_values("stage_index")
    outdir = ensure_outdir(outdir)

    x = df["stage_index"]

    # 1) Gas and water temperatures
    fig, ax = plt.subplots()
    ax.plot(x, df["T_gas_in"], marker="o", label="T_gas_in")
    ax.plot(x, df["T_gas_out"], marker="s", label="T_gas_out")
    ax.plot(x, df["T_water_in"], marker="^", label="T_water_in")
    ax.plot(x, df["T_water_out"], marker="v", label="T_water_out")
    ax.set_xlabel("HX stage index [-]")
    ax.set_ylabel("Temperature [°C]")
    ax.set_title(f"Temperature profiles along HX chain ({run})")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / f"{run}_hx_temperatures.png", dpi=200)
    plt.close(fig)

    # 2) Q_conv, Q_rad, Q_total per stage
    fig, ax = plt.subplots()
    ax.bar(x - 0.2, df["Q_conv"], width=0.2, label="Q_conv [MW]")
    ax.bar(x, df["Q_rad"], width=0.2, label="Q_rad [MW]")
    ax.bar(x + 0.2, df["Q_total"], width=0.2, label="Q_total [MW]")
    ax.set_xlabel("HX stage index [-]")
    ax.set_ylabel("Heat duty [MW]")
    ax.set_title(f"Heat duty per HX ({run})")
    ax.grid(True, axis="y")
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / f"{run}_hx_Q.png", dpi=200)
    plt.close(fig)

    # 3) Pressure drops per stage
    fig, ax = plt.subplots()
    ax.bar(x - 0.15, df["dp_fric"], width=0.3, label="dp_fric [Pa]")
    ax.bar(x + 0.15, df["dp_minor"], width=0.3, label="dp_minor [Pa]")
    ax.plot(x, df["dp_total"], marker="o", linestyle="--", label="dp_total [Pa]")
    ax.set_xlabel("HX stage index [-]")
    ax.set_ylabel("Pressure drop [Pa]")
    ax.set_title(f"Stage-wise pressure drop ({run})")
    ax.grid(True, axis="y")
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / f"{run}_hx_dp.png", dpi=200)
    plt.close(fig)

    # 4) Approach temperatures per stage
    fig, ax = plt.subplots()
    approach1 = df["T_gas_out"] - df["T_water_in"]
    approach2 = df["T_gas_in"] - df["T_water_out"]
    ax.plot(x, approach1, marker="o", label="T_gas_out - T_water_in")
    ax.plot(x, approach2, marker="s", label="T_gas_in - T_water_out")
    ax.set_xlabel("HX stage index [-]")
    ax.set_ylabel("Approach temperature [°C]")
    ax.set_title(f"Approach temperatures per stage ({run})")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outdir / f"{run}_hx_approach.png", dpi=200)
    plt.close(fig)

    # 5) UA per stage
    if "UA" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(x, df["UA"])
        ax.set_xlabel("HX stage index [-]")
        ax.set_ylabel("UA [MW/K]")
        ax.set_title(f"UA distribution along HX chain ({run})")
        ax.grid(True, axis="y")
        fig.tight_layout()
        fig.savefig(outdir / f"{run}_hx_UA.png", dpi=200)
        plt.close(fig)


def plot_hx_default_case(hx: pd.DataFrame, outdir: Path):
    if "run" not in hx.columns:
        return
    if "default_case" not in hx["run"].unique():
        return
    plot_hx_profile_for_run(hx, "default_case", outdir / "default_case")


def plot_hx_all_runs(hx: pd.DataFrame, outdir: Path, max_runs: int = None):
    runs = list(hx["run"].unique())
    if max_runs is not None:
        runs = runs[:max_runs]
    for r in runs:
        plot_hx_profile_for_run(hx, r, outdir / "per_run")


def plot_hx_heatmaps(hx: pd.DataFrame, outdir: Path):
    df = hx.copy()
    outdir = ensure_outdir(outdir)
    if df.empty or "Q_total" not in df.columns:
        return

    # Heat map of Q_total per stage and run
    table_Q = df.pivot_table(
        index="run", columns="stage_index", values="Q_total", aggfunc="mean"
    )
    fig, ax = plt.subplots()
    im = ax.imshow(table_Q.values, aspect="auto")
    ax.set_yticks(np.arange(len(table_Q.index)))
    ax.set_yticklabels(table_Q.index)
    ax.set_xticks(np.arange(len(table_Q.columns)))
    ax.set_xticklabels(table_Q.columns)
    ax.set_xlabel("HX stage index [-]")
    ax.set_ylabel("Run")
    ax.set_title("Heat duty per stage and run [MW]")
    fig.colorbar(im, ax=ax, label="Q_total [MW]")
    fig.tight_layout()
    fig.savefig(outdir / "heatmap_Q_total.png", dpi=200)
    plt.close(fig)

    # Heat map of gas outlet temperature
    if "T_gas_out" in df.columns:
        table_T = df.pivot_table(
            index="run", columns="stage_index", values="T_gas_out", aggfunc="mean"
        )
        fig, ax = plt.subplots()
        im = ax.imshow(table_T.values, aspect="auto")
        ax.set_yticks(np.arange(len(table_T.index)))
        ax.set_yticklabels(table_T.index)
        ax.set_xticks(np.arange(len(table_T.columns)))
        ax.set_xticklabels(table_T.columns)
        ax.set_xlabel("HX stage index [-]")
        ax.set_ylabel("Run")
        ax.set_title("Gas outlet temperature per stage and run [°C]")
        fig.colorbar(im, ax=ax, label="T_gas_out [°C]")
        fig.tight_layout()
        fig.savefig(outdir / "heatmap_T_gas_out.png", dpi=200)
        plt.close(fig)


def make_hx_plots(hx: pd.DataFrame, outdir: Path, max_runs_for_per_run: int = None):
    outdir = ensure_outdir(outdir / "hx")
    plot_hx_default_case(hx, outdir)
    plot_hx_all_runs(hx, outdir, max_runs=max_runs_for_per_run)
    plot_hx_heatmaps(hx, outdir)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ensure_outdir(OUTDIR)

    boiler = pd.read_csv(BOILER_CSV)
    hx = pd.read_csv(HX_CSV)

    boiler = rename_boiler_columns(boiler)
    hx = rename_hx_columns(hx)

    make_boiler_plots(boiler, OUTDIR)
    make_hx_plots(hx, OUTDIR, max_runs_for_per_run=None)


if __name__ == "__main__":
    main()
