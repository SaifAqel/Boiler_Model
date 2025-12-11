from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HX_CSV = Path(r"results/summary/stages_summary_all_runs.csv")
OUTDIR = Path(r"results/plots")

def ensure_outdir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

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

    if "stage" in df.columns:
        df["stage_index"] = (
            df["stage"].astype(str).str.extract(r"(\d+)", expand=False).astype(int)
        )
    return df

def plot_hx_profile_for_run(hx: pd.DataFrame, run: str, outdir: Path):
    df = hx[hx["run"] == run].copy()
    if df.empty:
        return

    df = df.sort_values("stage_index")
    outdir = ensure_outdir(outdir)
    x = df["stage_index"]

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

def make_hx_plots(hx: pd.DataFrame, outdir: Path):
    outdir = ensure_outdir(outdir / "hx")
    runs = sorted(hx["run"].unique())
    for r in runs:
        plot_hx_profile_for_run(hx, r, outdir)

def main():
    ensure_outdir(OUTDIR)

    hx = pd.read_csv(HX_CSV)
    hx = rename_hx_columns(hx)

    make_hx_plots(hx, OUTDIR)


if __name__ == "__main__":
    main()
