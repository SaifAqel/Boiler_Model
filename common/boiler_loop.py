from __future__ import annotations
import logging
from typing import Dict, Any, Tuple
from common.new_loader import load_all
from combustion.combustor import Combustor
from heat.runner import run_hx
from common.units import Q_
from common.props import WaterProps
from common.models import WaterStream
from common.results import CombustionResult, write_results_csvs

log = logging.getLogger(__name__)

def _drum_steam_rate(
    *,
    P_drum: Q_,
    Q_evap: Q_,
    m_fw: Q_,
    h_fw_out: Q_,
    steam_quality_out: float = 1.0,
) -> Q_:
    hf = WaterProps.h_f(P_drum).to("J/kg")
    hg = WaterProps.h_g(P_drum).to("J/kg")
    h_s = (hf + Q_(steam_quality_out, "") * (hg - hf)).to("J/kg")

    denom = (h_s - hf).to("J/kg")
    if denom.magnitude <= 0:
        raise ValueError("Invalid drum latent enthalpy (h_s - h_f) <= 0.")

    m_s = (Q_evap.to("W") + m_fw * (h_fw_out - hf)) / denom
    return m_s.to("kg/s")

def run_boiler_case(
    stages_path: str = "config/stages.yaml",
    air_path: str = "config/air.yaml",
    fuel_path: str = "config/fuel.yaml",
    water_path: str = "config/water.yaml",
    drum_path: str = "config/drum.yaml",
    operation_path: str = "config/operation.yaml",
    *,
    tol_m: Q_ = Q_(1e-3, "kg/s"),
    max_iter: int = 20,
    write_csv: bool = True,
    operation_overrides: Dict[str, Q_] | None = None,
    fuel_overrides: Dict[str, Q_] | None = None,
    run_id: str | None = None,
) -> Dict[str, Any]:
    log.info(f"Load config")
    stages, air, fuel, water, drum, operation = load_all(
        stages_path=stages_path,
        air_path=air_path,
        fuel_path=fuel_path,
        water_path=water_path,
        drum_path=drum_path,
        operation_path=operation_path,
    )

    if operation_overrides:
        operation.update(operation_overrides)

    if fuel_overrides:
        for attr, val in fuel_overrides.items():
            if hasattr(fuel, attr):
                setattr(fuel, attr, val)
            else:
                log.warning(f"GasStream (fuel) has no attribute '{attr}', ignoring override.")

    P_drum: Q_ | None = operation.get("drum_pressure", None)
    blowdown_fraction = operation.get("blowdown_fraction", Q_(0.0, ""))
    steam_quality_out = float(operation.get("steam_quality_out", Q_(1.0, "")).to("").magnitude)

    water_template: WaterStream = water

    if P_drum is not None:
        water_template.P = P_drum

    log.info(f"Running Combustor")
    svc = Combustor(air, fuel, operation["excess_air_ratio"])
    combustion_results = svc.run()
    log.info(f"Combustion Done")

    if P_drum is None:
        raise ValueError("Option B requires operation.drum_pressure")

    hf = WaterProps.h_f(P_drum).to("J/kg")
    hg = WaterProps.h_g(P_drum).to("J/kg")
    h_feed = water_template.h.to("J/kg")
    latent = (hg - hf).to("J/kg")
    m_fw = ((Q_(0.85, "") * combustion_results.Q_in.to("W")) / (latent + (hf - h_feed))).to("kg/s")

    prev_m = None
    final_result = None
    final_m_fw = None
    final_m_s = None

    tol_m_fw = tol_m.to("kg/s").magnitude

    for it in range(max_iter):
        m_bd = (blowdown_fraction.to("").magnitude * m_fw).to("kg/s")

        water_in = WaterStream(mass_flow=m_fw, h=water_template.h, P=water_template.P)

        final_result = run_hx(
            stages_raw=stages,
            water=water_in,
            gas=combustion_results.flue,
            drum=drum,
            drum_pressure=P_drum,
            target_dx="0.1 m",
            combustion=combustion_results,
            write_csv=False,
        )

        h_fw_out = final_result["water_out"].h.to("J/kg")

        evap_names = {f"HX_{i}" for i in range(1, 6)}
        Q_evap_W = 0.0
        for r in final_result["summary_rows"]:
            if r.get("stage_name") in evap_names and isinstance(r.get("Q_stage[MW]"), (int, float)):
                Q_evap_W += Q_(r["Q_stage[MW]"], "MW").to("W").magnitude
        Q_evap = Q_(Q_evap_W, "W")

        m_s = _drum_steam_rate(
            P_drum=P_drum,
            Q_evap=Q_evap,
            m_fw=m_fw,
            h_fw_out=h_fw_out,
            steam_quality_out=steam_quality_out,
        )

        resid = (m_s + m_bd - m_fw).to("kg/s").magnitude

        final_m_fw = m_fw
        final_m_s = m_s

        if prev_m is not None:
            dm = (m_fw - prev_m).to("kg/s").magnitude
            if abs(dm) < tol_m_fw and abs(resid) < tol_m_fw:
                break

        m_fw_new = (m_s + m_bd).to("kg/s")
        m_fw = (Q_(0.5, "") * m_fw_new + Q_(0.5, "") * m_fw).to("kg/s")

        prev_m = final_m_fw

    else:
        log.warning("Did not reach drum mass-balance convergence within max_iter.")

    feed_P: Q_ | None = None

    if P_drum is not None and final_m_fw is not None:
        P_drum_Pa = P_drum.to("Pa")

        # Start guess: above drum pressure
        P_in = (P_drum_Pa * Q_(1.01, "")).to("Pa")

        max_p_iter = 30
        tol_P = Q_(1.0, "Pa")

        feed_P = None
        last_result: Dict[str, Any] | None = None

        for _ in range(max_p_iter):
            water_trial = WaterStream(
                mass_flow=final_m_fw,
                h=water_template.h,
                P=P_in,
            )

            last_result = run_hx(
                stages_raw=stages,
                water=water_trial,
                gas=combustion_results.flue,
                drum=drum,
                drum_pressure=P_drum,
                target_dx="0.1 m",
                combustion=combustion_results,
                write_csv=False,
            )

            P_out = last_result["water_out"].P.to("Pa")

            # Want economiser outlet == drum pressure
            err = (P_drum_Pa - P_out).to("Pa")

            if abs(err).to("Pa").magnitude < tol_P.to("Pa").magnitude:
                feed_P = P_in
                break

            # Update inlet pressure by the outlet error
            P_in = (P_in + err).to("Pa")

            # Physical clamp: feed must be >= drum
            if P_in < P_drum_Pa:
                P_in = P_drum_Pa

        if feed_P is None:
            feed_P = P_in

        log.info(f"Solved feedwater inlet pressure: {feed_P:~P} for drum pressure {P_drum:~P}")

    if feed_P is None:
        feed_P = P_drum

    water_final_in = WaterStream(
        mass_flow=final_m_fw,
        h=water_template.h,
        P=feed_P,
    )

    log.info(f"Final feedwater inlet mass flow: {water_final_in.mass_flow:~P}")

    final_result = run_hx(
        stages_raw=stages,
        water=water_final_in,
        gas=combustion_results.flue,
        drum=drum,
        drum_pressure=P_drum,
        target_dx="0.1 m",
        combustion=combustion_results,
        write_csv=write_csv,
    )

    csv_paths: Tuple[str, str, str] | None = None
    if write_csv:
        effective_run_id = run_id if run_id is not None else final_result["run_id"]

        steps_csv, stages_summary_csv, boiler_summary_csv = write_results_csvs(
            global_profile=final_result["global_profile"],
            combustion=final_result["combustion"],
            outdir=final_result["outdir"],
            run_id=effective_run_id,
            drum_pressure=P_drum,
            feed_pressure=feed_P,
        )
        csv_paths = (steps_csv, stages_summary_csv, boiler_summary_csv)

    m_bd_final = None
    if final_m_fw is not None:
        m_bd_final = (blowdown_fraction.to("").magnitude * final_m_fw).to("kg/s")
    else:
        m_bd_final = Q_(0.0, "kg/s")

    return {
        "result": final_result,
        "m_fw": final_m_fw,
        "m_s": final_m_s,
        "m_bd": m_bd_final,
        "drum_pressure": P_drum,
        "combustion": combustion_results,
        "csv_paths": csv_paths,
    }

