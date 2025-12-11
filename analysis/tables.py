import os
import pandas as pd

INPUT_CSV = os.path.join("results", "summary", "boiler_kpis_all_runs.csv")
OUTPUT_MD = os.path.join("results", "summary", "boiler_kpis_tables.md")

def pretty_kpi_label(name: str) -> str:
    stripped = name.strip()

    if "[" in stripped and stripped.endswith("]"):
        base, unit = stripped.split("[", 1)
        base = base.strip()
        unit = "[" + unit
    else:
        base, unit = stripped, ""

    b = base.lower()

    if b.startswith("eta direct"):
        return r"$\eta_{\mathrm{direct}} [-]$"
    if b.startswith("eta indirect"):
        return r"$\eta_{\mathrm{indirect}} [-]$"
    if b.startswith("tad"):
        return f"adiabatic temperature {unit}".strip()
    if b.startswith("ua"):
        return f"conductance {unit}".strip()
    if b.startswith("q_in total"):
        return f"input heat {unit}".strip()
    if b.startswith("q_useful"):
        return f"useful heat {unit}".strip()
    if b.startswith("p-lhv"):
        return f"firing rate {unit}".strip()

    return stripped.lower()

def is_number(x) -> bool:
    try:
        float(x)
        return True
    except Exception:
        return False

def format_param_value(v) -> str:
    if is_number(v):
        return f"{float(v):.2f}"
    return str(v)

def main():
    df = pd.read_csv(INPUT_CSV)

    if "LHV[kJ/kg]" in df.columns:
        df["LHV[kJ/kg]"] = df["LHV[kJ/kg]"] / 1000.0
        df = df.rename(columns={"LHV[kJ/kg]": "LHV [MJ/kg]"})

    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].round(2)

    id_vars = ["run", "param_group", "param_value"]
    value_vars = [c for c in df.columns if c not in id_vars]

    group_meta = {
        "control": ("Control", "control"),
        "excess_air": ("Excess air", "excess air [-]"),
        "fuel_flow": ("Fuel flow", "fuel flow [kg/s]"),
        "water_pressure": ("Water pressure", "water pressure [bar]"),
    }

    lines = []

    melted = df.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="kpi",
        value_name="value",
    )

    for group_name, (title, index_label) in group_meta.items():

        if group_name == "control":
            sub = df[df["param_group"] == "control"]
            if sub.empty:
                continue

            row = sub.iloc[0]
            data = {"control": [row[k] for k in value_vars]}
            table = pd.DataFrame(data, index=value_vars)

            table.index = [pretty_kpi_label(i) for i in table.index]
            table.index.name = index_label

            lines.append(f"## {title.lower()}\n")
            lines.append(table.to_markdown())
            lines.append("")
            continue

        sub = melted[melted["param_group"] == group_name]
        if sub.empty:
            continue

        group_values = df.loc[df["param_group"] == group_name, "param_value"].tolist()
        seen = set()
        ordered = []
        for v in group_values:
            if v not in seen:
                seen.add(v)
                ordered.append(v)

        if group_name == "water_pressure":
            desired = [4.0, 10.0, 16.0]
            present = {float(v) for v in ordered if is_number(v)}
            ordered = [v for v in desired if v in present]

        table = sub.pivot_table(
            index="kpi", columns="param_value", values="value", aggfunc="first"
        )

        table = table.reindex(index=value_vars)
        table = table[ordered]
        table = table.dropna(how="all")

        table.index = [pretty_kpi_label(i) for i in table.index]
        table.columns = [format_param_value(c) for c in table.columns]
        table.index.name = index_label

        lines.append(f"## {title.lower()}\n")
        lines.append(table.to_markdown())
        lines.append("")

    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
