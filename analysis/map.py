from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HX_CSV = Path(r"results/summary/stages_summary_all_runs.csv")
OUTDIR = Path(r"results/plots/map")

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
            df["stage"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .astype(int)
        )
    return df

def _plot_single_heatmap(
    df: pd.DataFrame,
    value_col: str,
    outdir: Path,
    filename: str,
    title: str,
    cbar_label: str,
) -> None:
    if "run" not in df.columns or "stage_index" not in df.columns:
        return
    if value_col not in df.columns:
        return

    table = df.pivot_table(
        index="run",
        columns="stage_index",
        values=value_col,
        aggfunc="mean",
    )

    if table.empty:
        return

    fig, ax = plt.subplots()
    im = ax.imshow(table.values, aspect="auto")

    ax.set_yticks(np.arange(len(table.index)))
    ax.set_yticklabels(table.index)
    ax.set_xticks(np.arange(len(table.columns)))
    ax.set_xticklabels(table.columns)

    ax.set_xlabel("HX stage index [-]")
    ax.set_ylabel("Run")
    ax.set_title(title)

    fig.colorbar(im, ax=ax, label=cbar_label)
    fig.tight_layout()
    fig.savefig(outdir / filename, dpi=200)
    plt.close(fig)

def plot_hx_heatmaps(hx: pd.DataFrame, outdir: Path) -> None:
    df = hx.copy()
    outdir = ensure_outdir(outdir)
    if df.empty:
        return

    heatmaps = {
        "Q_total": (
            "heatmap_Q_total.png",
            "Heat duty per stage and run [MW]",
            "Q_total [MW]",
        ),
        "T_gas_out": (
            "heatmap_T_gas_out.png",
            "Gas outlet temperature per stage and run [°C]",
            "T_gas_out [°C]",
        ),
        "T_gas_in": (
            "heatmap_T_gas_in.png",
            "Gas inlet temperature per stage and run [°C]",
            "T_gas_in [°C]",
        ),
        "T_water_in": (
            "heatmap_T_water_in.png",
            "Water inlet temperature per stage and run [°C]",
            "T_water_in [°C]",
        ),
        "T_water_out": (
            "heatmap_T_water_out.png",
            "Water outlet temperature per stage and run [°C]",
            "T_water_out [°C]",
        ),
        "v_gas": (
            "heatmap_v_gas.png",
            "Gas velocity per stage and run [m/s]",
            "v_gas [m/s]",
        ),
        "v_water": (
            "heatmap_v_water.png",
            "Water velocity per stage and run [m/s]",
            "v_water [m/s]",
        ),
        "dp_total": (
            "heatmap_dp_total.png",
            "Total pressure drop per stage and run [Pa]",
            "Δp_total [Pa]",
        ),
        "Q_conv": (
            "heatmap_Q_conv.png",
            "Convective heat duty per stage and run [MW]",
            "Q_conv [MW]",
        ),
        "Q_rad": (
            "heatmap_Q_rad.png",
            "Radiative heat duty per stage and run [MW]",
            "Q_rad [MW]",
        ),
        "UA": (
            "heatmap_UA.png",
            "UA per stage and run [MW/K]",
            "UA [MW/K]",
        ),
        "steam_capacity": (
            "heatmap_steam_capacity.png",
            "Steam capacity per stage and run [t/h]",
            "Steam capacity [t/h]",
        ),
    }

    for col, (fname, title, cbar) in heatmaps.items():
        _plot_single_heatmap(df, col, outdir, fname, title, cbar)

def main():
    ensure_outdir(OUTDIR)
    hx = pd.read_csv(HX_CSV)
    hx = rename_hx_columns(hx)
    plot_hx_heatmaps(hx, OUTDIR)

if __name__ == "__main__":
    main()
