from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Dict, Any
from common.units import Q_
from heat.geometry import GeometryBuilder
from heat.solver import solve_exchanger
from common.models import HXStage, WaterStream, GasStream, Drum
from common.results import build_global_profile,CombustionResult
from heat.postproc import profile_to_dataframe, summary_from_profile
from common.props import WaterProps


def _q_or_none(s: Optional[str]) -> Optional[Q_]:
    if s is None:
        return None
    s = s.strip()
    return Q_(s) if s else None

def run_hx(
    *,
    stages_raw: List[HXStage],
    water: WaterStream,
    gas: GasStream,
    drum: Drum,
    drum_pressure: Q_ | None = None,
    target_dx: str | None = None,
    min_steps: int = 20,
    max_steps: int = 400,
    max_passes: int = 20,
    tol_Q: str = "1e-3 W",
    tol_end: str = "1e-3 J/kg",
    write_csv: bool,
    outdir: str | Path = "results/runs",
    run_id: str | None = None,
    log_level: str = "INFO",
    combustion: CombustionResult | None = None,
) -> Dict[str, Any]:
    
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not run_id:
        from datetime import datetime
        run_id = datetime.now().strftime("%Y%m%d-%H%M%S")

    target_dx_q = _q_or_none(target_dx)
    tol_Q_q = Q_(tol_Q)
    tol_end_q = Q_(tol_end)

    if gas is None or water is None or drum is None:
        raise ValueError("missing required inputs: 'gas', 'water', and 'drum'")

    stages: List[HXStage] = GeometryBuilder(drum).enrich(stages_raw)

    drum_pool = None
    if drum_pressure is not None:
        P_d = drum_pressure.to("Pa")
        h_f = WaterProps.h_f(P_d).to("J/kg")

        drum_pool = WaterStream(mass_flow=water.mass_flow, h=h_f, P=P_d)


    stage_results, gas_out, water_out = solve_exchanger(
        stages,
        gas,
        water,
        drum_pool=drum_pool,
        drum_pool_stage_count=5,
        target_dx=target_dx_q,
        min_steps_per_stage=min_steps,
        max_steps_per_stage=max_steps,
        max_passes=max_passes,
        tol_Q=tol_Q_q,
        tol_end=tol_end_q,
        log_level=log_level,
    )

    global_profile = build_global_profile(stage_results)

    if write_csv:
        df_steps = profile_to_dataframe(global_profile)
    else:
        df_steps = None

    rows, _, _ = summary_from_profile(global_profile, combustion=combustion, drum_pressure=drum_pressure)

    return {
        "gas_in": gas,
        "water_in": water,
        "gas_out": gas_out,
        "water_out": water_out,
        "stage_results": stage_results,
        "global_profile": global_profile,
        "steps_df": df_steps,
        "summary_rows": rows,
        "steps_csv": None,
        "summary_csv": None,
        "run_id": run_id,
        "outdir": str(outdir),
        "combustion": combustion,
    }