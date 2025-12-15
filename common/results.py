from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple
from common.units import Q_
from common.models import GasStream
from pathlib import Path
import pandas as pd

@dataclass(frozen=True)
class CombustionResult:
    LHV: Q_
    Q_in: Q_
    T_ad: Q_
    flue: GasStream
    flue_ad: GasStream | None = None
    fuel_LHV_mass: Q_ | None = None
    fuel_P_LHV: Q_ | None = None
    fuel_mass_flow: Q_ | None = None
    air_mass_flow: Q_ | None = None
    excess_air_ratio: Q_ | None = None

@dataclass(frozen=True)
class StepResult:
    i: int
    x: Q_
    dx: Q_
    gas: object
    water: object
    Tgw: Q_
    Tww: Q_
    UA_prime: Q_
    qprime: Q_
    boiling: bool
    h_g: Q_
    h_c: Q_
    stage_name: str = ""
    stage_index: int = -1
    dP_fric: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    dP_minor: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    dP_total: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    w_dP_fric: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    w_dP_minor: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    w_dP_tot: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    qprime_conv: Q_ = field(default_factory=lambda: Q_(0.0, "W/m"))
    qprime_rad: Q_ = field(default_factory=lambda: Q_(0.0, "W/m"))

@dataclass(frozen=True)
class StageResult:
    stage_name: str
    stage_kind: str
    steps: Sequence[StepResult]
    Q_stage: Q_
    UA_stage: Q_
    dP_stage_fric: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    dP_stage_minor: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    dP_stage_total: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    dP_water_stage_fric: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    dP_water_stage_minor: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    dP_water_stage_total: Q_ = field(default_factory=lambda: Q_(0.0, "Pa"))
    hot_flow_A: Q_ = field(default_factory=lambda: Q_(0.0, "m^2"))
    cold_flow_A: Q_ = field(default_factory=lambda: Q_(0.0, "m^2"))
    hot_Dh: Q_ = field(default_factory=lambda: Q_(0.0, "m"))
    cold_Dh: Q_ = field(default_factory=lambda: Q_(0.0, "m"))

@dataclass(frozen=True)
class GlobalProfile:
    x: List[Q_]
    dx: List[Q_]
    gas: List[object]
    water: List[object]
    qprime: List[Q_]
    UA_prime: List[Q_]
    h_g: List[Q_]
    h_c: List[Q_]
    stage_index: List[int]
    stage_name: List[str]
    dP_fric: List[Q_]
    dP_minor: List[Q_]
    dP_total: List[Q_]
    w_dP_fric: List[Q_]
    w_dP_minor: List[Q_]
    w_dP_tot: List[Q_]
    stage_results: List[StageResult]

def build_global_profile(stage_results: Sequence[StageResult]) -> GlobalProfile:
    xs: List[Q_] = []
    dxs: List[Q_] = []
    gas: List[object] = []
    water: List[object] = []
    qprime: List[Q_] = []
    UA_prime: List[Q_] = []
    h_g: List[Q_] = []
    h_c: List[Q_] = []
    sidx: List[int] = []
    sname: List[str] = []
    dP_fric: List[Q_] = []
    dP_minor: List[Q_] = []
    dP_total: List[Q_] = []
    w_dP_fric: List[Q_] = []
    w_dP_minor: List[Q_] = []
    w_dP_tot: List[Q_] = []

    for k, sr in enumerate(stage_results):
        for st in sr.steps:
            xs.append(st.x)
            dxs.append(st.dx)
            gas.append(st.gas)
            water.append(st.water)
            qprime.append(st.qprime)
            UA_prime.append(st.UA_prime)
            h_g.append(st.h_g)
            h_c.append(st.h_c)
            sidx.append(k if st.stage_index < 0 else st.stage_index)
            sname.append(sr.stage_name if not st.stage_name else st.stage_name)
            dP_fric.append(st.dP_fric)
            dP_minor.append(st.dP_minor)
            dP_total.append(st.dP_total)
            w_dP_fric.append(st.w_dP_fric)
            w_dP_minor.append(st.w_dP_minor)
            w_dP_tot.append(st.w_dP_tot)

    return GlobalProfile(
        x=xs, dx=dxs, gas=gas, water=water,
        qprime=qprime, UA_prime=UA_prime, h_g=h_g, h_c=h_c,
        stage_index=sidx, stage_name=sname,
        dP_fric=dP_fric, dP_minor=dP_minor, dP_total=dP_total,
        w_dP_fric=w_dP_fric, w_dP_minor=w_dP_minor, w_dP_tot=w_dP_tot,  
        stage_results=list(stage_results),
    )

def write_results_csvs(
    global_profile: GlobalProfile,
    combustion: CombustionResult | None,
    outdir: str | Path,
    run_id: str,
    drum_pressure: Q_ | None = None,
    feed_pressure: Q_ | None = None,

) -> Tuple[str, str, str]:

    from heat.postproc import profile_to_dataframe, summary_from_profile

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    steps_path = outdir / f"{run_id}_steps.csv"
    stages_summary_path = outdir / f"{run_id}_stages_summary.csv"
    boiler_summary_path = outdir / f"{run_id}_boiler_summary.csv"

    df_steps = profile_to_dataframe(
        global_profile,
        remap_water=False,
    )
    df_steps.set_index("stage_name").to_csv(steps_path)

    rows, _, _ = summary_from_profile(
        global_profile,
        combustion=combustion,
        drum_pressure=drum_pressure
    )


    df_summary = pd.DataFrame(
        rows,
        columns=[
            "stage_index", "stage_name", "stage_kind",
            "Q_stage[MW]", "UA_stage[MW/K]",

            "gas_in_P[Pa]", "gas_in_T[°C]", "gas_in_h[kJ/kg]",
            "gas_out_P[Pa]", "gas_out_T[°C]", "gas_out_h[kJ/kg]",

            "water_in_P[Pa]", "water_in_T[°C]", "water_in_h[kJ/kg]",
            "water_out_P[Pa]", "water_out_T[°C]", "water_out_h[kJ/kg]",

            "gas_V_avg[m/s]", "water_V_avg[m/s]",

            "ΔP_stage_fric[Pa]", "ΔP_stage_minor[Pa]", "ΔP_stage_total[Pa]",
            "ΔP_water_stage_fric[Pa]", "ΔP_water_stage_minor[Pa]", "ΔP_water_stage_total[Pa]",
            "stack_temperature[°C]",
            "Q_conv_stage[MW]", "Q_rad_stage[MW]",

            "steam_capacity[kg/s]", "steam_capacity[t/h]",

            "η_direct[-]", "η_indirect[-]",
            "Q_total_useful[MW]", "Q_in_total[MW]",
            "P_LHV[MW]", "LHV_mass[kJ/kg]",
        ],
    ).set_index("stage_index")


    df_stages = df_summary[df_summary["stage_name"] != "TOTAL_BOILER"].copy()
    df_boiler = df_summary[df_summary["stage_name"] == "TOTAL_BOILER"].copy()

    try:
        m_w = global_profile.stage_results[5].steps[0].water.mass_flow.to("kg/s").magnitude
    except Exception:
        m_w = float("nan")

    try:
        m_circ = global_profile.stage_results[0].steps[0].water.mass_flow.to("kg/s").magnitude
    except Exception:
        m_circ = float("nan")


    df_stages = df_stages.set_index("stage_name")

    table = pd.DataFrame(
        {
            "name": df_stages.index,
            "kind": df_stages["stage_kind"],
            "gas in pressure[pa]": df_stages["gas_in_P[Pa]"],
            "gas in temp[°C]": df_stages["gas_in_T[°C]"],
            "gas in enthalpy[kJ/kg]": df_stages["gas_in_h[kJ/kg]"],
            "gas out pressure[pa]": df_stages["gas_out_P[Pa]"],
            "gas out temp[°C]": df_stages["gas_out_T[°C]"],
            "gas out enthalpy[kJ/kg]": df_stages["gas_out_h[kJ/kg]"],
            "water in temp[°C]": df_stages["water_in_T[°C]"],
            "water in enthalpy[kJ/kg]": df_stages["water_in_h[kJ/kg]"],
            "water in pressure[pa]": df_stages["water_in_P[Pa]"],
            "water out temp[°C]": df_stages["water_out_T[°C]"],
            "water out enthalpy[kJA/kg]": df_stages["water_out_h[kJ/kg]"],
            "water out pressure[pa]": df_stages["water_out_P[Pa]"],
            "gas avg velocity[m/s]": df_stages["gas_V_avg[m/s]"],
            "water avg velocity[m/s]": df_stages["water_V_avg[m/s]"],
            "pressure drop fric[pa]": df_stages["ΔP_stage_fric[Pa]"],
            "pressure drop minor[pa]": df_stages["ΔP_stage_minor[Pa]"],
            "pressure drop total[pa]": df_stages["ΔP_stage_total[Pa]"],
            "water pressure drop fric[pa]": df_stages["ΔP_water_stage_fric[Pa]"],
            "water pressure drop minor[pa]": df_stages["ΔP_water_stage_minor[Pa]"],
            "water pressure drop total[pa]": df_stages["ΔP_water_stage_total[Pa]"],
            "Q conv[MW]": df_stages["Q_conv_stage[MW]"],
            "Q rad[MW]": df_stages["Q_rad_stage[MW]"],
            "Q total[MW]": df_stages["Q_stage[MW]"],
            "UA[MW/K]": df_stages["UA_stage[MW/K]"],
            "steam capacity[t/h]": df_stages["steam_capacity[t/h]"],
        }
    ).set_index("name")

    table = table.drop(columns=["name"], errors="ignore")
    table.T.to_csv(stages_summary_path, index_label="name")

    if not df_boiler.empty:
        boiler_row = df_boiler.iloc[0].copy()

        try:
            m_w = global_profile.water[0].mass_flow.to("kg/s").magnitude
        except Exception:
            m_w = float("nan")
        boiler_row["water_mass_flow[kg/s]"] = m_w
        boiler_row["circulation_mass_flow[kg/s]"] = m_circ

        if feed_pressure is not None:
            try:
                boiler_row["feedwater_P[Pa]"] = feed_pressure.to("Pa").magnitude
            except Exception:
                boiler_row["feedwater_P[Pa]"] = ""
        else:
            boiler_row["feedwater_P[Pa]"] = ""

        if drum_pressure is not None:
            try:
                boiler_row["drum_P[Pa]"] = drum_pressure.to("Pa").magnitude
            except Exception:
                boiler_row["drum_P[Pa]"] = ""
        else:
            boiler_row["drum_P[Pa]"] = ""

        if combustion is not None:
            try:
                boiler_row["T_ad[°C]"] = combustion.T_ad.to("degC").magnitude
            except Exception:
                boiler_row["T_ad[°C]"] = ""

            if combustion.fuel_LHV_mass is not None:
                boiler_row["fuel_LHV_mass[kJ/kg]"] = combustion.fuel_LHV_mass.to("kJ/kg").magnitude
            else:
                boiler_row["fuel_LHV_mass[kJ/kg]"] = ""

            if combustion.fuel_P_LHV is not None:
                boiler_row["fuel_P_LHV[MW]"] = combustion.fuel_P_LHV.to("MW").magnitude
            else:
                boiler_row["fuel_P_LHV[MW]"] = ""

            if combustion.fuel_mass_flow is not None:
                boiler_row["fuel_mass_flow[kg/s]"] = combustion.fuel_mass_flow.to("kg/s").magnitude
            else:
                boiler_row["fuel_mass_flow[kg/s]"] = ""

            if combustion.excess_air_ratio is not None:
                boiler_row["excess_air_ratio[-]"] = combustion.excess_air_ratio.to("").magnitude
            else:
                boiler_row["excess_air_ratio[-]"] = ""

            if combustion.air_mass_flow is not None:
                boiler_row["air_mass_flow[kg/s]"] = combustion.air_mass_flow.to("kg/s").magnitude
            else:
                boiler_row["air_mass_flow[kg/s]"] = ""

        else:
            boiler_row["T_ad[°C]"] = ""
            boiler_row["fuel_LHV_mass[kJ/kg]"] = ""
            boiler_row["fuel_P_LHV[MW]"] = ""
            boiler_row["fuel_mass_flow[kg/s]"] = ""
            boiler_row["air_mass_flow[kg/s]"] = ""
            boiler_row["excess_air_ratio[-]"] = ""

        boiler_df = pd.DataFrame([boiler_row])

        summary_mapping = [
            ("fuel mass flow[kg/s]",            "fuel_mass_flow[kg/s]"),
            ("air flow[kg/s]",                  "air_mass_flow[kg/s]"),
            ("excess air ratio[-]",             "excess_air_ratio[-]"),
            ("water flow[kg/s]",                "water_mass_flow[kg/s]"),
            ("circulation flow[kg/s]",         "circulation_mass_flow[kg/s]"),
            ("steam capacity[t/h]",             "steam_capacity[t/h]"),
            ("eta direct[-]",                   "η_direct[-]"),
            ("eta indirect[-]",                 "η_indirect[-]"),
            ("UA[MW/K]",                        "UA_stage[MW/K]"),
            ("Q_in total[MW]",                  "Q_in_total[MW]"),
            ("Q_useful[MW]",                     "Q_total_useful[MW]"),
            ("pressure drop fric total[Pa]",     "ΔP_stage_fric[Pa]"),
            ("pressure drop minor total[Pa]",   "ΔP_stage_minor[Pa]"),
            ("pressure drop total[Pa]",         "ΔP_stage_total[Pa]"),
            ("water pressure drop fric total[Pa]",  "ΔP_water_stage_fric[Pa]"),
            ("water pressure drop minor total[Pa]", "ΔP_water_stage_minor[Pa]"),
            ("water pressure drop total[Pa]",       "ΔP_water_stage_total[Pa]"), 
            ("LHV[kJ/kg]",                      "LHV_mass[kJ/kg]"),
            ("P-LHV[MW]",                       "P_LHV[MW]"),
            ("Tad[°C]",                         "T_ad[°C]"),
            ("stack temperature[°C]",           "stack_temperature[°C]"),
            ("feedwater pressure[Pa]",              "feedwater_P[Pa]"),
            ("drum pressure[Pa]",                   "drum_P[Pa]"),
        ]

        out_row = {}
        row0 = boiler_df.iloc[0]
        for new_name, src_col in summary_mapping:
            out_row[new_name] = row0.get(src_col, "")

        boiler_out_df = pd.DataFrame([out_row]).T
        boiler_out_df = boiler_out_df.reset_index()
        boiler_out_df.columns = ["parameter", "value"]

        boiler_out_df.to_csv(boiler_summary_path, index=False)

    else:
        empty_cols = list(df_summary.columns) + [
            "water_mass_flow[kg/s]",
            "T_ad[°C]",
            "fuel_LHV_mass[kJ/kg]",
            "fuel_P_LHV[MW]",
            "fuel_mass_flow[kg/s]",
            "air_mass_flow[kg/s]",
            "excess_air_ratio[-]", 
        ]
        pd.DataFrame(columns=empty_cols).to_csv(boiler_summary_path, index=False)

    return str(steps_path), str(stages_summary_path), str(boiler_summary_path)   

