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

def _water_mass_from_efficiency(
    eta: Q_,
    combustion: CombustionResult,
    water_template: WaterStream,
) -> Q_:
    Q_in = combustion.Q_in.to("W")  # Q_

    h_in = water_template.h.to("J/kg")

    h_steam = WaterProps.h_g(water_template.P).to("J/kg")

    delta_h = (h_steam - h_in).to("J/kg")
    if delta_h.magnitude <= 0.0:
        raise ValueError("Steam enthalpy must be greater than feedwater enthalpy.")

    Q_target = (eta * Q_in).to("W")

    m_w = (Q_target / delta_h).to("kg/s")
    return m_w

def run_boiler_case(
    stages_path: str = "config/stages.yaml",
    air_path: str = "config/air.yaml",
    fuel_path: str = "config/fuel.yaml",
    water_path: str = "config/water.yaml",
    drum_path: str = "config/drum.yaml",
    operation_path: str = "config/operation.yaml",
    *,
    eta_guess: Q_ = Q_(0.90, ""),
    tol_m: Q_ = Q_(1e-3, "kg/s"),
    max_iter: int = 20,
    write_csv: bool = True,
    operation_overrides: Dict[str, Q_] | None = None,
    water_overrides: Dict[str, Q_] | None = None,
    fuel_overrides: Dict[str, Q_] | None = None,
    run_id: str | None = None,
) -> Dict[str, Any]:
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

    if water_overrides:
        for attr, val in water_overrides.items():
            if hasattr(water, attr):
                setattr(water, attr, val)
            else:
                log.warning(f"WaterStream has no attribute '{attr}', ignoring override.")

    if fuel_overrides:
        for attr, val in fuel_overrides.items():
            if hasattr(fuel, attr):
                setattr(fuel, attr, val)
            else:
                log.warning(f"GasStream (fuel) has no attribute '{attr}', ignoring override.")


    svc = Combustor(air, fuel, operation["excess_air_ratio"])
    combustion_results = svc.run()
    log.info(f"Combustion results: {combustion_results}")

    water_template: WaterStream = water

    prev_m = None
    final_result = None
    final_m = None
    final_eta = None

    # --- Iteration loop ---
    for it in range(max_iter):
        if it % 5 == 0:
            log.info(f"Iteration {it}: eta_guess={eta_guess}, prev_m={prev_m}")

        m_w = _water_mass_from_efficiency(eta_guess, combustion_results, water_template)

        water_iter = WaterStream(
            mass_flow=m_w,
            h=water_template.h,
            P=water_template.P,
        )

        final_result = run_hx(
            stages_raw=stages,
            water=water_iter,
            gas=combustion_results.flue,
            drum=drum,
            target_dx="0.1 m",
            combustion=combustion_results,
            write_csv=False,
        )

        total_row = next(
            r for r in final_result["summary_rows"]
            if r["stage_name"] == "TOTAL_BOILER"
        )

        eta_indirect = total_row["η_indirect[-]"]
        if eta_indirect == "" or eta_indirect is None:
            final_m = m_w
            final_eta = eta_guess
            break

        eta_new = Q_(eta_indirect, "")

        final_m = m_w
        final_eta = eta_new

        if prev_m is not None:
            dm = (m_w - prev_m).to("kg/s")
            if abs(dm).magnitude < tol_m.magnitude:
                log.info(f"Converged in {it+1} iterations.")
                break

        prev_m = m_w
        eta_guess = eta_new

    else:
        log.warning("Did not reach mass-flow convergence within max_iter.")

    final_result = run_hx(
        stages_raw=stages,
        water=water_iter,
        gas=combustion_results.flue,
        drum=drum,
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
        )
        csv_paths = (steps_csv, stages_summary_csv, boiler_summary_csv)


    log.info(f"Final water mass flow: {final_m}")
    log.info(f"Final indirect efficiency: {final_eta}")

    return {
        "result": final_result,
        "final_m": final_m,
        "final_eta": final_eta,
        "combustion": combustion_results,
        "csv_paths": csv_paths,
    }
