from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(".")
KPI_CSV = BASE_DIR / "results" / "summary" / "boiler_kpis_all_runs.csv"
STAGE_CSV = BASE_DIR / "results" / "summary" / "stages_summary_all_runs.csv"
PLOT_DIR = BASE_DIR / "results" / "plots" / "sens"

PLOT_DIR.mkdir(parents=True, exist_ok=True)

STAGE_ORDER = ["HX_1", "HX_2", "HX_3", "HX_4", "HX_5", "HX_6"]
STAGE_INDEX = {s: i for i, s in enumerate(STAGE_ORDER, start=1)}

plt.rcParams.update(
    {
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "font.size": 9,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "legend.frameon": False,
        "axes.titlesize": 7,
        "axes.labelsize": 7,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "legend.fontsize": 6,
        "legend.title_fontsize": 6,
    }
)

def load_data():
    df_kpi = pd.read_csv(KPI_CSV)
    df_stage = pd.read_csv(STAGE_CSV)

    df_kpi["param_value"] = pd.to_numeric(df_kpi["param_value"], errors="coerce")
    df_stage["param_value"] = pd.to_numeric(df_stage["param_value"], errors="coerce")

    df_kpi = df_kpi.sort_values(["param_group", "param_value"])
    df_stage["stage_index"] = df_stage["stage"].map(STAGE_INDEX)

    return df_kpi, df_stage

def add_fig_legend(fig, axes, title=None, bottom=0.15, ncol=None):

    axes = np.atleast_1d(axes).ravel()

    handles = []
    labels = []
    for ax in axes:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    by_label = dict(zip(labels, handles))
    if not by_label:
        return

    if ncol is None:
        ncol = min(len(by_label), 4)

    fig.legend(
        by_label.values(),
        by_label.keys(),
        title=title,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.0),
        ncol=ncol,
    )
    fig.tight_layout(rect=[0, bottom, 1, 1])

def add_legend_under_axis(fig, ax, handles=None, labels=None, ncol=None, dy=0.02):

    if handles is None or labels is None:
        handles, labels = ax.get_legend_handles_labels()

    if not handles:
        return

    box = ax.get_position()
    x_center = 0.5 * (box.x0 + box.x1)
    y = box.y0 - dy

    if ncol is None:
        ncol = len(labels)

    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(x_center, y),
        ncol=ncol,
    )


def df_subset(df_kpi, group_name):
    sub = df_kpi[df_kpi["param_group"] == group_name].copy()
    return sub.sort_values("param_value")


def stage_subset(df_stage, group_name):
    sub = df_stage[df_stage["param_group"] == group_name].copy()
    return sub.sort_values(["param_value", "stage_index"])

def savefig(name, fig=None):
    path = PLOT_DIR / name
    if fig is None:
        fig = plt.gcf()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")

def plot_excess_air_boiler_overview(df_ea):
    lam = df_ea["param_value"]
    q_in = df_ea["Q_in total[MW]"]
    q_useful = df_ea["Q_useful[MW]"]
    eta_d = df_ea["eta direct[-]"]
    eta_i = df_ea["eta indirect[-]"]
    t_stack = df_ea["stack temperature[°C]"]
    m_water = df_ea["water flow[kg/s]"]
    dp_total = df_ea["pressure drop total[Pa]"]

    fig, axes = plt.subplots(2, 2, figsize=(6.0, 5.5))

    fig.subplots_adjust(top=0.90, bottom=0.12, hspace=0.45)

    ax00 = axes[0, 0]
    ax00.plot(lam, q_in, "o-", label=r"$Q_\mathrm{in}$")
    ax00.plot(lam, q_useful, "s-", label=r"$Q_\mathrm{useful}$")
    ax00.set_xlabel(r"Excess air ratio $\lambda$ [-]")
    ax00.set_ylabel("Heat rate [MW]")
    ax00.set_title("Heat input and useful duty")

    h00, l00 = ax00.get_legend_handles_labels()

    ax01 = axes[0, 1]
    ax01.plot(lam, eta_d, "o-", label=r"$\eta_\mathrm{direct}$")
    ax01.plot(lam, eta_i, "s-", label=r"$\eta_\mathrm{indirect}$")
    ax01.set_xlabel(r"Excess air ratio $\lambda$ [-]")
    ax01.set_ylabel("Efficiency [-]")
    ax01.set_title("Boiler efficiency")

    h01, l01 = ax01.get_legend_handles_labels()

    ax10 = axes[1, 0]
    ax10b = ax10.twinx()
    ax10.plot(lam, t_stack, "o-", label=r"$T_\mathrm{stack}$")
    ax10b.plot(lam, m_water, "s--", label=r"$\dot m_w$")
    ax10.set_xlabel(r"Excess air ratio $\lambda$ [-]")
    ax10.set_ylabel(r"Stack temperature [°C]")
    ax10b.set_ylabel(r"Water flow [kg/s]")
    ax10.set_title("Stack temperature and water flow")

    h10, l10 = ax10.get_legend_handles_labels()
    h10b, l10b = ax10b.get_legend_handles_labels()
    h10_all = h10 + h10b
    l10_all = l10 + l10b

    ax11 = axes[1, 1]
    ax11.plot(lam, -dp_total, "o-", label=r"$\Delta P_\mathrm{gas}$")
    ax11.set_xlabel(r"Excess air ratio $\lambda$ [-]")
    ax11.set_ylabel(r"Total gas side $\Delta P$ [Pa]")
    ax11.set_title("Total gas side pressure drop")

    h11, l11 = ax11.get_legend_handles_labels()

    add_legend_under_axis(fig, ax00, h00, l00, dy=0.05)
    add_legend_under_axis(fig, ax01, h01, l01, dy=0.05)

    add_legend_under_axis(fig, ax10, h10_all, l10_all, dy=0.05)
    add_legend_under_axis(fig, ax11, h11, l11, dy=0.05)

    savefig("fig_lambda_boiler_overview.png", fig)

def plot_excess_air_stage_temperatures(df_stage_ea):
    lam_values = sorted(df_stage_ea["param_value"].dropna().unique())
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5), sharey=True)

    fig.subplots_adjust(top=0.88, bottom=0.20, wspace=0.25)

    for lam in lam_values:
        data = df_stage_ea[df_stage_ea["param_value"] == lam].sort_values("stage_index")
        x = data["stage_index"]

        axes[0].plot(x, data["gas out temp[°C]"], marker="o",
                     label=fr"$\lambda={lam:.1f}$")
        axes[1].plot(x, data["water out temp[°C]"], marker="s",
                     label=fr"$\lambda={lam:.1f}$")

    for ax, title, ylabel in [
        (axes[0], "Gas outlet temperature", r"Temperature [°C]"),
        (axes[1], "Water outlet temperature", r"Temperature [°C]"),
    ]:
        ax.set_xticks(range(1, len(STAGE_ORDER) + 1))
        ax.set_xticklabels(STAGE_ORDER)
        ax.set_xlabel("Heat exchanger stage")
        ax.set_ylabel(ylabel)
        ax.set_title(title)

    add_legend_under_axis(fig, axes[0], dy=0.05)
    add_legend_under_axis(fig, axes[1], dy=0.05)

    savefig("fig_lambda_stage_temperatures.png", fig)


def plot_excess_air_stage_duties_ua(df_stage_ea):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5))

    fig.subplots_adjust(top=0.88, bottom=0.20, wspace=0.30)

    ax0 = axes[0]
    for stage in STAGE_ORDER:
        data = df_stage_ea[df_stage_ea["stage"] == stage].sort_values("param_value")
        ax0.plot(data["param_value"], data["Q total[MW]"], marker="o", label=stage)
    ax0.set_xlabel(r"Excess air ratio $\lambda$ [-]")
    ax0.set_ylabel(r"Stage heat duty $Q_\mathrm{total}$ [MW]")
    ax0.set_title("Stage total duties vs excess air")

    ax1 = axes[1]
    for stage in STAGE_ORDER:
        data = df_stage_ea[df_stage_ea["stage"] == stage].sort_values("param_value")
        ax1.plot(data["param_value"], data["UA[MW/K]"], marker="s", label=stage)
    ax1.set_xlabel(r"Excess air ratio $\lambda$ [-]")
    ax1.set_ylabel(r"Global conductance $UA$ [MW/K]")
    ax1.set_title("Stage global conductance vs excess air")

    add_legend_under_axis(fig, ax0, dy=0.05)
    add_legend_under_axis(fig, ax1, dy=0.05)

    savefig("fig_lambda_stage_duties.png", fig)

def plot_excess_air_stage_pressure_drop(df_stage_ea):
    fig, ax = plt.subplots(figsize=(6.0, 3.5))

    fig.subplots_adjust(top=0.88, bottom=0.22)

    for stage in STAGE_ORDER:
        data = df_stage_ea[df_stage_ea["stage"] == stage].sort_values("param_value")
        ax.plot(data["param_value"], -data["pressure drop total[pa]"],
                marker="o", label=stage)

    ax.set_xlabel(r"Excess air ratio $\lambda$ [-]")
    ax.set_ylabel(r"Stage total $\Delta P$ [Pa]")
    ax.set_title("Gas side pressure loss per stage – excess air sweep")

    add_legend_under_axis(fig, ax, dy=0.06)

    savefig("fig_lambda_stage_dp.png", fig)

def plot_excess_air_compact(df_ea):
    lam = df_ea["param_value"]
    fig, axes = plt.subplots(2, 2, figsize=(6.0, 5.5))

    fig.subplots_adjust(top=0.90, bottom=0.12, hspace=0.45, wspace=0.30)

    ax00 = axes[0, 0]
    ax00.plot(lam, df_ea["eta direct[-]"], "o-", label="direct")
    ax00.plot(lam, df_ea["eta indirect[-]"], "s-", label="indirect")
    ax00.set_ylabel("Efficiency [-]")
    ax00.set_xlabel(r"$\lambda$ [-]")
    ax00.set_title("Efficiency")

    ax01 = axes[0, 1]
    ax01.plot(lam, df_ea["stack temperature[°C]"], "o-",
              label=r"$T_\mathrm{stack}$")
    ax01.set_ylabel(r"$T_\mathrm{stack}$ [°C]")
    ax01.set_xlabel(r"$\lambda$ [-]")
    ax01.set_title("Stack temperature")

    ax10 = axes[1, 0]
    ax10.plot(lam, df_ea["steam capacity[t/h]"], "o-", label="steam capacity")
    ax10.set_ylabel("Steam capacity [t/h]")
    ax10.set_xlabel(r"$\lambda$ [-]")
    ax10.set_title("Steam capacity")

    ax11 = axes[1, 1]
    ax11.plot(lam, -df_ea["pressure drop total[Pa]"], "o-",
              label=r"$\Delta P_\mathrm{gas}$")
    ax11.set_ylabel(r"Total gas $\Delta P$ [Pa]")
    ax11.set_xlabel(r"$\lambda$ [-]")
    ax11.set_title("Total gas pressure drop")

    add_legend_under_axis(fig, ax00, dy=0.05)
    add_legend_under_axis(fig, ax01, dy=0.05)
    add_legend_under_axis(fig, ax10, dy=0.05)
    add_legend_under_axis(fig, ax11, dy=0.05)

    savefig("fig_lambda_compact_summary.png", fig)

def plot_pressure_boiler_overview(df_p):
    P_bar = df_p["param_value"]
    q_in = df_p["Q_in total[MW]"]
    q_useful = df_p["Q_useful[MW]"]
    eta_d = df_p["eta direct[-]"]
    eta_i = df_p["eta indirect[-]"]
    m_w = df_p["water flow[kg/s]"]
    steam_cap = df_p["steam capacity[t/h]"]
    t_stack = df_p["stack temperature[°C]"]
    dp_total = df_p["pressure drop total[Pa]"]

    fig, axes = plt.subplots(2, 2, figsize=(6.0, 5.5))
    fig.subplots_adjust(top=0.90, bottom=0.12, hspace=0.45)

    ax00 = axes[0, 0]
    ax00.plot(P_bar, q_in, "o-", label=r"$Q_\mathrm{in}$")
    ax00.plot(P_bar, q_useful, "s-", label=r"$Q_\mathrm{useful}$")
    ax00.set_xlabel("Drum pressure [bar]")
    ax00.set_ylabel("Heat rate [MW]")
    ax00.set_title("Heat input and useful duty")
    h00, l00 = ax00.get_legend_handles_labels()

    ax01 = axes[0, 1]
    ax01.plot(P_bar, eta_d, "o-", label="direct")
    ax01.plot(P_bar, eta_i, "s-", label="indirect")
    ax01.set_xlabel("Drum pressure [bar]")
    ax01.set_ylabel("Efficiency [-]")
    ax01.set_title("Boiler efficiency")
    h01, l01 = ax01.get_legend_handles_labels()

    ax10 = axes[1, 0]
    ax10b = ax10.twinx()
    ax10.plot(P_bar, m_w, "o-", label="water flow")
    ax10b.plot(P_bar, steam_cap, "s--", label="steam capacity")
    ax10.set_xlabel("Drum pressure [bar]")
    ax10.set_ylabel(r"Water flow [kg/s]")
    ax10b.set_ylabel(r"Steam capacity [t/h]")
    ax10.set_title("Water / steam throughput")
    h10, l10 = ax10.get_legend_handles_labels()
    h10b, l10b = ax10b.get_legend_handles_labels()
    h10_all = h10 + h10b
    l10_all = l10 + l10b

    ax11 = axes[1, 1]
    ax11b = ax11.twinx()
    ax11.plot(P_bar, t_stack, "o-", label=r"$T_\mathrm{stack}$")
    ax11b.plot(P_bar, -dp_total, "s--", label=r"$\Delta P_\mathrm{gas}$")
    ax11.set_xlabel("Drum pressure [bar]")
    ax11.set_ylabel(r"Stack temperature [°C]")
    ax11b.set_ylabel(r"Total gas $\Delta P$ [Pa]")
    ax11.set_title("Stack temperature and gas pressure drop")
    h11, l11 = ax11.get_legend_handles_labels()
    h11b, l11b = ax11b.get_legend_handles_labels()
    h11_all = h11 + h11b
    l11_all = l11 + l11b

    add_legend_under_axis(fig, ax00, h00, l00, dy=0.05)
    add_legend_under_axis(fig, ax01, h01, l01, dy=0.05)
    add_legend_under_axis(fig, ax10, h10_all, l10_all, dy=0.05)
    add_legend_under_axis(fig, ax11, h11_all, l11_all, dy=0.05)

    savefig("fig_pressure_boiler_overview.png", fig)

def plot_pressure_steam_tradeoff(df_p, df_stage_p):
    P_bar = df_p["param_value"]
    steam_cap = df_p["steam capacity[t/h]"]

    drum_stage = df_stage_p[df_stage_p["stage"] == "HX_1"]
    h_steam = (
        drum_stage.groupby("param_value")["water out enthalpy[kJ/kg]"]
        .mean()
        .reindex(P_bar.values)
        .values
    )

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5))
    fig.subplots_adjust(top=0.88, bottom=0.22, wspace=0.30)

    ax0 = axes[0]
    ax0.plot(P_bar, steam_cap, "o-", label="steam capacity")
    ax0.set_xlabel("Drum pressure [bar]")
    ax0.set_ylabel("Steam capacity [t/h]")
    ax0.set_title("Steam mass flow vs pressure")

    ax1 = axes[1]
    ax1.plot(P_bar, h_steam, "s-", label="steam enthalpy")
    ax1.set_xlabel("Drum pressure [bar]")
    ax1.set_ylabel("Steam specific enthalpy [kJ/kg]")
    ax1.set_title("Steam enthalpy vs pressure")

    add_legend_under_axis(fig, ax0, dy=0.06)
    add_legend_under_axis(fig, ax1, dy=0.06)

    savefig("fig_pressure_steam_tradeoff.png", fig)

def plot_pressure_stage_duties(df_stage_p):
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    fig.subplots_adjust(top=0.88, bottom=0.22)

    for stage in STAGE_ORDER:
        data = df_stage_p[df_stage_p["stage"] == stage].sort_values("param_value")
        ax.plot(data["param_value"], data["Q total[MW]"], marker="o", label=stage)

    ax.set_xlabel("Drum pressure [bar]")
    ax.set_ylabel(r"Stage duty $Q_\mathrm{total}$ [MW]")
    ax.set_title("Stage-wise total duty vs drum pressure")

    add_legend_under_axis(fig, ax, dy=0.06)

    savefig("fig_pressure_stage_duties.png", fig)

def plot_pressure_economiser_detail(df_stage_p):
    eco = df_stage_p[df_stage_p["stage"] == "HX_6"].sort_values("param_value")
    P_bar = eco["param_value"]

    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    fig.subplots_adjust(top=0.88, bottom=0.22)

    ax.plot(P_bar, eco["gas in temp[°C]"], "o-", label=r"$T_{g,\mathrm{in}}$")
    ax.plot(P_bar, eco["gas out temp[°C]"], "s-", label=r"$T_{g,\mathrm{out}}$")
    ax.plot(P_bar, eco["water in temp[°C]"], "d-", label=r"$T_{w,\mathrm{in}}$")
    ax.plot(P_bar, eco["water out temp[°C]"], "x-", label=r"$T_{w,\mathrm{out}}$")
    ax.set_xlabel("Drum pressure [bar]")
    ax.set_ylabel("Temperature [°C]")

    ax2 = ax.twinx()
    ax2.plot(P_bar, eco["Q total[MW]"], "k--", label=r"$Q_{\mathrm{HX6}}$")
    ax2.set_ylabel(r"Economiser duty $Q_{\mathrm{HX6}}$ [MW]")

    ax.set_title("Economiser performance vs drum pressure")

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    add_legend_under_axis(fig, ax, h1 + h2, l1 + l2, dy=0.06)

    savefig("fig_pressure_economiser.png", fig)

def plot_pressure_compact(df_p, df_stage_p):
    P_bar = df_p["param_value"]

    drum_stage = df_stage_p[df_stage_p["stage"] == "HX_1"]
    h_steam = (
        drum_stage.groupby("param_value")["water out enthalpy[kJ/kg]"]
        .mean()
        .reindex(P_bar.values)
        .values
    )

    fig, axes = plt.subplots(2, 2, figsize=(6.0, 5.5))
    fig.subplots_adjust(top=0.90, bottom=0.12, hspace=0.45, wspace=0.30)

    ax00 = axes[0, 0]
    ax00.plot(P_bar, df_p["eta direct[-]"], "o-", label="direct")
    ax00.plot(P_bar, df_p["eta indirect[-]"], "s-", label="indirect")
    ax00.set_xlabel("Drum pressure [bar]")
    ax00.set_ylabel("Efficiency [-]")
    ax00.set_title("Efficiency")

    ax01 = axes[0, 1]
    ax01.plot(P_bar, df_p["stack temperature[°C]"], "o-",
              label=r"$T_\mathrm{stack}$")
    ax01.set_xlabel("Drum pressure [bar]")
    ax01.set_ylabel(r"$T_\mathrm{stack}$ [°C]")
    ax01.set_title("Stack temperature")

    ax10 = axes[1, 0]
    ax10.plot(P_bar, df_p["steam capacity[t/h]"], "o-",
              label="steam capacity")
    ax10.set_xlabel("Drum pressure [bar]")
    ax10.set_ylabel("Steam capacity [t/h]")
    ax10.set_title("Steam capacity")

    ax11 = axes[1, 1]
    ax11.plot(P_bar, h_steam, "o-", label="steam enthalpy")
    ax11.set_xlabel("Drum pressure [bar]")
    ax11.set_ylabel("Steam enthalpy [kJ/kg]")
    ax11.set_title("Steam enthalpy")

    add_legend_under_axis(fig, ax00, dy=0.05)
    add_legend_under_axis(fig, ax01, dy=0.05)
    add_legend_under_axis(fig, ax10, dy=0.05)
    add_legend_under_axis(fig, ax11, dy=0.05)

    savefig("fig_pressure_compact_summary.png", fig)

def plot_fuel_boiler_overview(df_f):
    mdot = df_f["param_value"]
    q_in = df_f["Q_in total[MW]"]
    q_useful = df_f["Q_useful[MW]"]
    eta_d = df_f["eta direct[-]"]
    eta_i = df_f["eta indirect[-]"]
    steam_cap = df_f["steam capacity[t/h]"]
    t_stack = df_f["stack temperature[°C]"]
    dp_total = df_f["pressure drop total[Pa]"]

    fig, axes = plt.subplots(2, 2, figsize=(6.0, 5.5))
    fig.subplots_adjust(top=0.90, bottom=0.12, hspace=0.45)

    ax00 = axes[0, 0]
    ax00.plot(mdot, q_in, "o-", label=r"$Q_\mathrm{in}$")
    ax00.plot(mdot, q_useful, "s-", label=r"$Q_\mathrm{useful}$")
    ax00.set_xlabel(r"Fuel mass flow $\dot m_f$ [kg/s]")
    ax00.set_ylabel("Heat rate [MW]")
    ax00.set_title("Heat input and useful duty")
    h00, l00 = ax00.get_legend_handles_labels()

    ax01 = axes[0, 1]
    ax01.plot(mdot, eta_d, "o-", label="direct")
    ax01.plot(mdot, eta_i, "s-", label="indirect")
    ax01.set_xlabel(r"Fuel mass flow $\dot m_f$ [kg/s]")
    ax01.set_ylabel("Efficiency [-]")
    ax01.set_title("Boiler efficiency")
    h01, l01 = ax01.get_legend_handles_labels()

    ax10 = axes[1, 0]
    ax10.plot(mdot, steam_cap, "o-", label="steam capacity")
    ax10.set_xlabel(r"Fuel mass flow $\dot m_f$ [kg/s]")
    ax10.set_ylabel("Steam capacity [t/h]")
    ax10.set_title("Steam capacity")
    h10, l10 = ax10.get_legend_handles_labels()

    ax11 = axes[1, 1]
    ax11b = ax11.twinx()
    ax11.plot(mdot, t_stack, "o-", label=r"$T_\mathrm{stack}$")
    ax11b.plot(mdot, -dp_total, "s--", label=r"$\Delta P_\mathrm{gas}$")
    ax11.set_xlabel(r"Fuel mass flow $\dot m_f$ [kg/s]")
    ax11.set_ylabel(r"Stack temperature [°C]")
    ax11b.set_ylabel(r"Total gas $\Delta P$ [Pa]")
    ax11.set_title("Stack temperature and gas pressure drop")
    h11, l11 = ax11.get_legend_handles_labels()
    h11b, l11b = ax11b.get_legend_handles_labels()
    h11_all = h11 + h11b
    l11_all = l11 + l11b

    add_legend_under_axis(fig, ax00, h00, l00, dy=0.05)
    add_legend_under_axis(fig, ax01, h01, l01, dy=0.05)
    add_legend_under_axis(fig, ax10, h10, l10, dy=0.05)
    add_legend_under_axis(fig, ax11, h11_all, l11_all, dy=0.05)

    savefig("fig_fuel_boiler_overview.png", fig)

def plot_fuel_linearity(df_f):
    mdot = df_f["param_value"]
    q_in = df_f["Q_in total[MW]"]
    q_useful = df_f["Q_useful[MW]"]
    steam_cap = df_f["steam capacity[t/h]"]

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5))
    fig.subplots_adjust(top=0.88, bottom=0.22, wspace=0.30)

    ax0 = axes[0]
    ax0.plot(q_in, q_useful, "o", label="model")
    coeff = np.polyfit(q_in, q_useful, 1)
    q_fit = np.linspace(q_in.min(), q_in.max(), 50)
    ax0.plot(q_fit, np.polyval(coeff, q_fit), "k--",
             label=f"linear fit, slope={coeff[0]:.3f}")
    ax0.set_xlabel(r"$Q_\mathrm{in}$ [MW]")
    ax0.set_ylabel(r"$Q_\mathrm{useful}$ [MW]")
    ax0.set_title("Linearity of useful duty")

    ax1 = axes[1]
    ax1.plot(mdot, steam_cap, "o", label="model")
    coeff2 = np.polyfit(mdot, steam_cap, 1)
    mdot_fit = np.linspace(mdot.min(), mdot.max(), 50)
    ax1.plot(mdot_fit, np.polyval(coeff2, mdot_fit), "k--",
             label=f"linear fit, slope={coeff2[0]:.1f}")
    ax1.set_xlabel(r"Fuel mass flow $\dot m_f$ [kg/s]")
    ax1.set_ylabel("Steam capacity [t/h]")
    ax1.set_title("Linearity of steam capacity")

    add_legend_under_axis(fig, ax0, dy=0.06)
    add_legend_under_axis(fig, ax1, dy=0.06)

    savefig("fig_fuel_linearity.png", fig)

def plot_fuel_stage_duties_dp(df_stage_f):
    fig, axes = plt.subplots(2, 1, figsize=(6.0, 6.0), sharex=True)
    fig.subplots_adjust(top=0.90, bottom=0.12, hspace=0.45)

    ax0 = axes[0]
    for stage in STAGE_ORDER:
        data = df_stage_f[df_stage_f["stage"] == stage].sort_values("param_value")
        ax0.plot(data["param_value"], data["Q total[MW]"], marker="o", label=stage)
    ax0.set_ylabel(r"Stage duty $Q_\mathrm{total}$ [MW]")
    ax0.set_title("Stage total duties vs fuel mass flow")

    ax1 = axes[1]
    for stage in STAGE_ORDER:
        data = df_stage_f[df_stage_f["stage"] == stage].sort_values("param_value")
        ax1.plot(data["param_value"], -data["pressure drop total[pa]"],
                 marker="s", label=stage)
    ax1.set_xlabel(r"Fuel mass flow $\dot m_f$ [kg/s]")
    ax1.set_ylabel(r"Stage total $\Delta P$ [Pa]")
    ax1.set_title("Stage pressure drops vs fuel mass flow")

    add_legend_under_axis(fig, ax0, dy=0.05)
    add_legend_under_axis(fig, ax1, dy=0.05)

    savefig("fig_fuel_stage_duty_dp.png", fig)

def plot_fuel_stage_temperatures(df_stage_f):
    mdot_values = sorted(df_stage_f["param_value"].dropna().unique())

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5), sharey=True)
    fig.subplots_adjust(top=0.88, bottom=0.22, wspace=0.25)

    for mdot in mdot_values:
        data = df_stage_f[df_stage_f["param_value"] == mdot].sort_values("stage_index")
        x = data["stage_index"]

        axes[0].plot(x, data["gas out temp[°C]"], marker="o",
                     label=fr"$\dot m_f={mdot:.3f}$")
        axes[1].plot(x, data["water out temp[°C]"], marker="s",
                     label=fr"$\dot m_f={mdot:.3f}$")

    for ax, title, ylabel in [
        (axes[0], "Gas outlet temperature", r"Temperature [°C]"),
        (axes[1], "Water outlet temperature", r"Temperature [°C]"),
    ]:
        ax.set_xticks(range(1, len(STAGE_ORDER) + 1))
        ax.set_xticklabels(STAGE_ORDER)
        ax.set_xlabel("Heat exchanger stage")
        ax.set_ylabel(ylabel)
        ax.set_title(title)

    add_legend_under_axis(fig, axes[0], dy=0.06)
    add_legend_under_axis(fig, axes[1], dy=0.06)

    savefig("fig_fuel_stage_temperatures.png", fig)

def plot_fuel_compact(df_f):
    mdot = df_f["param_value"]

    fig, axes = plt.subplots(2, 2, figsize=(6.0, 5.5))
    fig.subplots_adjust(top=0.90, bottom=0.12, hspace=0.45, wspace=0.30)

    ax00 = axes[0, 0]
    ax00.plot(mdot, df_f["eta direct[-]"], "o-", label="direct")
    ax00.plot(mdot, df_f["eta indirect[-]"], "s-", label="indirect")
    ax00.set_xlabel(r"$\dot m_f$ [kg/s]")
    ax00.set_ylabel("Efficiency [-]")
    ax00.set_title("Efficiency")

    ax01 = axes[0, 1]
    ax01.plot(mdot, df_f["stack temperature[°C]"], "o-",
              label=r"$T_\mathrm{stack}$")
    ax01.set_xlabel(r"$\dot m_f$ [kg/s]")
    ax01.set_ylabel(r"$T_\mathrm{stack}$ [°C]")
    ax01.set_title("Stack temperature")

    ax10 = axes[1, 0]
    ax10.plot(mdot, df_f["steam capacity[t/h]"], "o-",
              label="steam capacity")
    ax10.set_xlabel(r"$\dot m_f$ [kg/s]")
    ax10.set_ylabel("Steam capacity [t/h]")
    ax10.set_title("Steam capacity")

    ax11 = axes[1, 1]
    ax11.plot(mdot, -df_f["pressure drop total[Pa]"], "o-",
              label=r"$\Delta P_\mathrm{gas}$")
    ax11.set_xlabel(r"$\dot m_f$ [kg/s]")
    ax11.set_ylabel(r"Total gas $\Delta P$ [Pa]")
    ax11.set_title("Total gas pressure drop")

    add_legend_under_axis(fig, ax00, dy=0.05)
    add_legend_under_axis(fig, ax01, dy=0.05)
    add_legend_under_axis(fig, ax10, dy=0.05)
    add_legend_under_axis(fig, ax11, dy=0.05)

    savefig("fig_fuel_compact_summary.png", fig)

def plot_global_eta_vs_stack(df_kpi):
    fig, ax = plt.subplots(figsize=(5.0, 3.5))
    fig.subplots_adjust(top=0.88, bottom=0.22)

    groups = df_kpi["param_group"].fillna("control").unique()
    markers = {
        "control": "o",
        "excess_air": "s",
        "water_pressure": "d",
        "fuel_flow": "^",
    }

    for g in groups:
        sub = df_kpi[df_kpi["param_group"].fillna("control") == g]
        ax.scatter(
            sub["stack temperature[°C]"],
            sub["eta indirect[-]"],
            marker=markers.get(g, "o"),
            label=g,
        )

    ax.set_xlabel(r"Stack temperature [°C]")
    ax.set_ylabel(r"Indirect efficiency $\eta_\mathrm{indirect}$ [-]")
    ax.set_title("Global relation of efficiency and stack temperature")

    add_legend_under_axis(fig, ax, dy=0.06)

    savefig("fig_global_eta_vs_stack.png", fig)

def main():
    df_kpi, df_stage = load_data()

    df_ea = df_subset(df_kpi, "excess_air")
    df_stage_ea = stage_subset(df_stage, "excess_air")
    if not df_ea.empty:
        plot_excess_air_boiler_overview(df_ea)
        plot_excess_air_stage_temperatures(df_stage_ea)
        plot_excess_air_stage_duties_ua(df_stage_ea)
        plot_excess_air_stage_pressure_drop(df_stage_ea)
        plot_excess_air_compact(df_ea)

    df_p = df_subset(df_kpi, "water_pressure")
    df_stage_p = stage_subset(df_stage, "water_pressure")
    if not df_p.empty:
        plot_pressure_boiler_overview(df_p)
        plot_pressure_steam_tradeoff(df_p, df_stage_p)
        plot_pressure_stage_duties(df_stage_p)
        plot_pressure_economiser_detail(df_stage_p)
        plot_pressure_compact(df_p, df_stage_p)

    df_f = df_subset(df_kpi, "fuel_flow")
    df_stage_f = stage_subset(df_stage, "fuel_flow")
    if not df_f.empty:
        plot_fuel_boiler_overview(df_f)
        plot_fuel_linearity(df_f)
        plot_fuel_stage_duties_dp(df_stage_f)
        plot_fuel_stage_temperatures(df_stage_f)
        plot_fuel_compact(df_f)

    plot_global_eta_vs_stack(df_kpi)


if __name__ == "__main__":
    main()
