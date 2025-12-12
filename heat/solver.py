from __future__ import annotations
from typing import List, Tuple, Optional
from math import ceil, log10
import logging

from common.units import Q_
from common.models import HXStage, GasStream, WaterStream
from common.results import StepResult, StageResult
from heat.step_solver import solve_step
from common.props import GasProps, WaterProps
from common.logging_utils import setup_logging

_gasprops = GasProps()
_gas = GasProps()

def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))

def _median_length(stages: List[HXStage]) -> Q_:
    Ls = sorted([st.spec["inner_length"].to("m") for st in stages], key=lambda x: x.magnitude)
    return Ls[len(Ls)//2]

def _make_grid(L: Q_, n_steps: int) -> tuple[List[Q_], Q_]:
    dx = (L / n_steps).to("m")
    xs = [(i * dx).to("m") for i in range(n_steps)]
    return xs, dx

def _copy_step_with_stage(
    sr: StepResult,
    stage_name: str,
    stage_index: int,
    *,
    dP_fric: Q_ | None = None,
    dP_minor: Q_ | None = None,
    dP_total: Q_ | None = None,
    w_dP_fric: Q_ | None = None,
    w_dP_minor: Q_ | None = None,
    w_dP_tot: Q_ | None = None,
) -> StepResult:
    return StepResult(
        i=sr.i, x=sr.x, dx=sr.dx,
        gas=sr.gas, water=sr.water,
        Tgw=sr.Tgw, Tww=sr.Tww,
        UA_prime=sr.UA_prime, qprime=sr.qprime,
        boiling=sr.boiling,
        h_g=sr.h_g, h_c=sr.h_c,
        qprime_conv=sr.qprime_conv,
        qprime_rad=sr.qprime_rad,  
        stage_name=stage_name, stage_index=stage_index,
        dP_fric=dP_fric if dP_fric is not None else Q_(0.0, "Pa"),
        dP_minor=dP_minor if dP_minor is not None else Q_(0.0, "Pa"),
        dP_total=dP_total if dP_total is not None else Q_(0.0, "Pa"),
        w_dP_fric=w_dP_fric if w_dP_fric is not None else Q_(0.0, "Pa"),
        w_dP_minor=w_dP_minor if w_dP_minor is not None else Q_(0.0, "Pa"),
        w_dP_tot=w_dP_tot if w_dP_tot is not None else Q_(0.0, "Pa"),
    )

def initial_wall_guesses(g: GasStream, w: WaterStream) -> tuple[Q_, Q_, Q_]:
    Tg = g.T.to("K")
    Tw = WaterProps.T_from_Ph(w.P, w.h).to("K")
    qprime = Q_(1e4, "W/m")
    return Tg, Tw, qprime

def _colebrook_white_f(Re: float, eps_over_D: float) -> float:
    Re = max(Re, 1e-6)
    if Re < 2300.0:
        return 64.0 / max(Re, 1e-12)

    f = 0.25 / (log10(eps_over_D/3.7 + 5.74/(Re**0.9)) ** 2)

    for _ in range(30):
        invsqrtf_old = 1.0 / (f ** 0.5)
        rhs = -2.0 * log10(eps_over_D/3.7 + 2.51/(Re * (f ** 0.5)))
        invsqrtf = rhs
        if abs(invsqrtf - invsqrtf_old) < 1e-6:
            break
        f = 1.0 / (invsqrtf ** 2)
    return float(f)

def _friction_factor(Re: float, eps_over_D: float) -> float:
    if Re < 2300.0:
        return 64.0 / max(Re, 1e-12)
    if Re >= 4000.0:
        return _colebrook_white_f(Re, eps_over_D)
    f_lam = 64.0 / max(Re, 1e-12)
    f_turb = _colebrook_white_f(4000.0, eps_over_D)
    w = (Re - 2300.0) / (4000.0 - 2300.0)
    return float((1-w) * f_lam + w * f_turb)

def _stage_minor_K_sum(stage: HXStage) -> Q_:
    spec = stage.spec
    kind = stage.kind.lower()

    K_hot_bend = spec.get("K_hot_bend", None)
    if K_hot_bend is not None:
        return K_hot_bend.to("")

    if kind == "reversal_chamber":
        Rc = spec.get("curvature_radius", None)
        Do = spec.get("outer_diameter", None)
        if Rc is not None and Do is not None and Rc.to("m").magnitude > 0 and Do.to("m").magnitude > 0:
            r = (Rc / Do).to("").magnitude
            Kbend = max(0.2, min(2.0, 0.9 / max(r, 1e-6)))
        else:
            Kbend = 0.5
        return Q_(Kbend, "")

    return Q_(0.0, "")

def _gas_dp_economiser_crossflow(
    g: GasStream,
    stage: HXStage,
    dx: Q_,
    i_step: int,
    n_steps: int,
) -> tuple[Q_, Q_, Q_]:
    spec = stage.spec

    A_hot = spec["hot_flow_A"].to("m^2")
    L     = spec["inner_length"].to("m")
    Do    = spec["outer_diameter"].to("m")
    ST    = spec["ST"].to("m")
    SL    = spec["SL"].to("m")

    N_rows_q = spec.get("N_rows", None)
    N_rows = int(round(N_rows_q.to("").magnitude)) if N_rows_q is not None else 1
    N_rows = max(N_rows, 1)

    arrangement = str(spec.get("arrangement", "inline") or "inline").lower()

    rho = _gas.rho(g.T, g.P, g.comp)
    mu  = _gas.mu(g.T, g.P, g.comp)

    V_bulk = (g.mass_flow / (rho * A_hot)).to("m/s")

    umax_factor_q = spec.get("umax_factor", Q_(1.0, ""))
    umax_factor = umax_factor_q.to("").magnitude
    V_char = (V_bulk * umax_factor).to("m/s")

    Re_D = (rho * V_char * Do / mu).to("").magnitude
    Re_D = max(Re_D, 1e-3)

    ST_over_D = (ST / Do).to("").magnitude
    SL_over_D = (SL / Do).to("").magnitude

    if arrangement == "staggered":
        C0 = 1.2
        m  = -0.15
    else:
        C0 = 1.0
        m  = -0.15

    geom_fac = (ST_over_D / 1.5) ** -0.2 * (SL_over_D / 1.5) ** -0.2

    zeta_row = C0 * (Re_D ** m) * geom_fac
    zeta_row = max(zeta_row, 1e-4)

    zeta_total = zeta_row * N_rows

    q_dyn = (rho * V_char**2 / 2.0).to("Pa")

    dP_bundle = (-zeta_total * q_dyn).to("Pa")

    frac = (dx / L).to("").magnitude
    dP_fric = (dP_bundle * frac).to("Pa")
    K_bend_per_step = spec.get("_K_bend_per_step", Q_(0.0, "")).to("")
    K_inlet = spec.get("K_hot_inlet", Q_(0.0, "")).to("")
    K_outlet = spec.get("K_hot_outlet", Q_(0.0, "")).to("")

    K_minor = K_bend_per_step

    if i_step == 0:
        K_minor = (K_minor + K_inlet).to("")

    if i_step == max(n_steps - 1, 0):
        K_minor = (K_minor + K_outlet).to("")

    dP_minor = (-K_minor * q_dyn).to("Pa")
    dP_total = (dP_fric + dP_minor).to("Pa")

    return dP_fric, dP_minor, dP_total

def _gas_dp_components(
    g: GasStream,
    stage: HXStage,
    dx: Q_,
    i_step: int,
    n_steps: int,
) -> tuple[Q_, Q_, Q_]:
    kind = stage.kind.lower()

    if kind == "economiser":
        return _gas_dp_economiser_crossflow(g, stage, dx, i_step, n_steps)

    spec = stage.spec
    A = spec["hot_flow_A"].to("m^2")
    Dh = spec["hot_Dh"].to("m")
    eps = spec.get("roughness_in", Q_(0.0, "m")).to("m")
    rho = _gas.rho(g.T, g.P, g.comp)
    mu  = _gas.mu(g.T, g.P, g.comp)

    V = (g.mass_flow / (rho * A)).to("m/s")
    Re = max((rho * V * Dh / mu).to("").magnitude, 1e-6)
    eps_over_D = (eps / Dh).to("").magnitude

    f = _friction_factor(Re, eps_over_D)
    q = (rho * V**2 / 2.0).to("Pa")

    dP_fric = (-f * (dx / Dh) * q).to("Pa")

    K_bend_per_step = spec.get("_K_bend_per_step", Q_(0.0, "")).to("")

    K_inlet = spec.get("K_hot_inlet", Q_(0.0, "")).to("")
    K_outlet = spec.get("K_hot_outlet", Q_(0.0, "")).to("")

    K_minor = K_bend_per_step

    if i_step == 0:
        K_minor = (K_minor + K_inlet).to("")

    if i_step == max(n_steps - 1, 0):
        K_minor = (K_minor + K_outlet).to("")

    dP_minor = (-K_minor * q).to("Pa")
    dP_total = (dP_fric + dP_minor).to("Pa")
    return dP_fric, dP_minor, dP_total

def pressure_drop_gas(g: GasStream, stage: HXStage, i: int, dx: Q_, n_steps: int) -> Q_:
    _, _, dP_total = _gas_dp_components(g, stage, dx, i, n_steps)
    return dP_total

def _solve_T_for_h(P, X, h_target, T0, maxit=30):
    T = T0.to("K"); h_target = h_target.to("J/kg")
    for _ in range(maxit):
        h  = _gasprops.h(T, P, X)
        dh = (h_target - h).to("J/kg")
        if abs(dh).magnitude < 1e-3:
            return T
        cp = _gasprops.cp(T, P, X)
        dT = (dh / cp).to("K")
        T  = (T + 0.8*dT).to("K")
    return T

def update_gas_after_step(g, qprime, dx, stage, i: int, n_steps: int) -> GasStream:
    Q_step = (qprime * dx).to("W")
    dh     = (-Q_step / g.mass_flow).to("J/kg")
    h_old  = _gasprops.h(g.T, g.P, g.comp)
    h_new  = (h_old + dh).to("J/kg")
    T_new  = _solve_T_for_h(g.P, g.comp, h_new, g.T)
    P_new  = (g.P + pressure_drop_gas(g, stage, i=i, dx=dx, n_steps=n_steps)).to("Pa")
    return GasStream(mass_flow=g.mass_flow, T=T_new, P=P_new, comp=g.comp)

def _water_dp_components(w: WaterStream, stage: HXStage, dx: Q_, i_step: int, n_steps: int) -> tuple[Q_, Q_, Q_]:
    spec = stage.spec
    kind = stage.kind.lower()

    dP_fric = Q_(0.0, "Pa")
    dP_minor = Q_(0.0, "Pa")

    if kind == "economiser":
        A = spec["cold_flow_A"].to("m^2")
        Dh = spec["cold_Dh"].to("m")
        eps = spec.get("roughness_cold_surface", Q_(0.0, "m")).to("m")

        rho = WaterProps.rho_from_Ph(w.P, w.h)
        mu  = WaterProps.mu_from_Ph(w.P, w.h)

        V = (w.mass_flow / (rho * A)).to("m/s")
        Re = max((rho * V * Dh / mu).to("").magnitude, 1e-6)
        eps_over_D = (eps / Dh).to("").magnitude

        f = _friction_factor(Re, eps_over_D)
        q = (rho * V**2 / 2.0).to("Pa")

        dP_fric = (-f * (dx / Dh) * q).to("Pa")
    else:
        A = spec.get("cold_flow_A", None)
        if A is not None:
            A = A.to("m^2")
            rho = WaterProps.rho_from_Ph(w.P, w.h)
            V = (w.mass_flow / (rho * A)).to("m/s")
            q = (rho * V**2 / 2.0).to("Pa")
        else:
            rho = WaterProps.rho_from_Ph(w.P, w.h)
            q = Q_(0.0, "Pa")

    K_cold_bend_total = spec.get("K_cold_bend", Q_(0.0, "")).to("")
    K_cold_bend_per_step = (K_cold_bend_total / max(n_steps, 1)).to("")

    K_cold_inlet = spec.get("K_cold_inlet", Q_(0.0, "")).to("")
    K_cold_outlet = spec.get("K_cold_outlet", Q_(0.0, "")).to("")

    K_minor = K_cold_bend_per_step

    if i_step == 0:
        K_minor = (K_minor + K_cold_inlet).to("")

    if i_step == max(n_steps - 1, 0):
        K_minor = (K_minor + K_cold_outlet).to("")

    if "q" not in locals():
        A = spec.get("cold_flow_A", None)
        if A is not None:
            A = A.to("m^2")
            rho = WaterProps.rho_from_Ph(w.P, w.h)
            V = (w.mass_flow / (rho * A)).to("m/s")
            q = (rho * V**2 / 2.0).to("Pa")
        else:
            q = Q_(0.0, "Pa")

    dP_minor = (-K_minor * q).to("Pa")

    dP_total = (dP_fric + dP_minor).to("Pa")
    return dP_fric, dP_minor, dP_total

def update_water_after_step(w: WaterStream, qprime: Q_, dx: Q_, stage: HXStage, i: int, n_steps: int) -> WaterStream:
    Q_step = (qprime * dx).to("W")
    dh = (Q_step / w.mass_flow).to("J/kg")
    h_new = (w.h + dh).to("J/kg")

    dP_fric, dP_minor, dP_tot = _water_dp_components(w, stage, dx, i, n_steps)
    P_new = (w.P + dP_tot).to("Pa")

    return WaterStream(mass_flow=w.mass_flow, h=h_new, P=P_new)


def solve_stage(
    g_in: GasStream,
    w_in: WaterStream,
    stage: HXStage,
    n_steps: int,
    *,
    stage_index: int,
    logger_name: str = "solver",
) -> tuple[GasStream, WaterStream, StageResult]:
    log = logging.getLogger(logger_name)
    L = stage.spec["inner_length"].to("m")
    xs, dx = _make_grid(L, n_steps)

    K_sum = _stage_minor_K_sum(stage).to("")
    K_per_step = (K_sum / max(n_steps, 1)).to("")
    stage.spec["_K_bend_per_step"] = K_per_step

    steps: List[StepResult] = []

    g = g_in
    w = w_in
    Tgw_guess, Tww_guess, qprime_guess = initial_wall_guesses(g, w)

    Q_sum = Q_(0.0, "W")
    UA_sum = Q_(0.0, "W/K")
    dP_fric_sum = Q_(0.0, "Pa")
    dP_minor_sum = Q_(0.0, "Pa")
    dP_total_sum = Q_(0.0, "Pa")
    w_dP_fric_sum  = Q_(0.0, "Pa")
    w_dP_minor_sum  = Q_(0.0, "Pa")
    w_dP_tot_sum  = Q_(0.0, "Pa")

    for i, x in enumerate(xs):
        dP_fric_step, dP_minor_step, dP_tot_step = _gas_dp_components(g, stage, dx, i, n_steps)
        w_dP_fric_step, w_dP_minor_step, w_dP_tot_step = _water_dp_components(w, stage, dx, i, n_steps)

        sr = solve_step(
            g=g, w=w, stage=stage,
            Tgw_guess=Tgw_guess, Tww_guess=Tww_guess, qprime_guess=qprime_guess,
            i=i, x=x, dx=dx
        )

        sr = _copy_step_with_stage(
            sr, stage.name, stage_index,
            dP_fric=dP_fric_step,
            dP_minor=dP_minor_step,
            dP_total=dP_tot_step,
            w_dP_fric=w_dP_fric_step,
            w_dP_minor=w_dP_minor_step,
            w_dP_tot=w_dP_tot_step,
        )
        steps.append(sr)

        Q_sum = (Q_sum + (sr.qprime * dx)).to("W")
        UA_sum = (UA_sum + (sr.UA_prime * dx)).to("W/K")

        dP_fric_sum  = (dP_fric_sum  + dP_fric_step).to("Pa")
        dP_minor_sum = (dP_minor_sum + dP_minor_step).to("Pa")
        dP_total_sum = (dP_total_sum + dP_tot_step).to("Pa")

        w_dP_fric_sum  = (w_dP_fric_sum  + w_dP_fric_step).to("Pa")
        w_dP_minor_sum = (w_dP_minor_sum + w_dP_minor_step).to("Pa")
        w_dP_tot_sum   = (w_dP_tot_sum   + w_dP_tot_step).to("Pa")

        Tgw_guess, Tww_guess, qprime_guess = sr.Tgw, sr.Tww, sr.qprime
        g = update_gas_after_step(g, sr.qprime, dx, stage, i, n_steps)
        w = update_water_after_step(w, sr.qprime, dx, stage, i, n_steps)

        log.debug(
            "step",
            extra={"stage": stage.name, "step": f"{i+1}/{n_steps}"}
        )

    g_out = g
    w_out = w

    stage_res = StageResult(
        stage_name=stage.name,
        stage_kind=stage.kind,  
        steps=steps,
        Q_stage=Q_sum,
        UA_stage=UA_sum,
        dP_stage_fric=dP_fric_sum,
        dP_stage_minor=dP_minor_sum,
        dP_stage_total=dP_total_sum,
        dP_water_stage_fric=w_dP_fric_sum,
        dP_water_stage_minor=w_dP_minor_sum,
        dP_water_stage_total=w_dP_tot_sum,
        hot_flow_A=stage.spec["hot_flow_A"],
        cold_flow_A=stage.spec["cold_flow_A"],
        hot_Dh=stage.spec["hot_Dh"],
        cold_Dh=stage.spec["cold_Dh"],
    )

    recon = sum([(s.qprime * s.dx).to("W") for s in steps], Q_(0.0, "W"))
    if abs((stage_res.Q_stage - recon) / (stage_res.Q_stage + Q_(1e-12, "W"))) > 0.005:
        raise RuntimeError(f"Stage energy accumulation mismatch >0.5% in {stage.name}")

    log.debug(
        f"{stage.name}: dP_fric={stage_res.dP_stage_fric:~P}, "
        f"dP_minor={stage_res.dP_stage_minor:~P}, dP_total={stage_res.dP_stage_total:~P}",
        extra={"stage": stage.name, "step": "ΔP"},
    )

    log.debug(
        f"{stage.name}: gas_in(T={g_in.T:~P},P={g_in.P:~P}) gas_out(T={g_out.T:~P},P={g_out.P:~P}) "
        f"water_in(h={w_in.h:~P},P={w_in.P:~P}) water_out(h={w_out.h:~P}) Q_stage={stage_res.Q_stage:~P}",
        extra={"stage": stage.name, "step": f"{len(steps)}/{n_steps}"},
    )

    

    return g_out, w_out, stage_res

def solve_exchanger(
    stages: List[HXStage],
    gas_in: GasStream,
    water_in: WaterStream,
    *,
    target_dx: Q_ | None = None,
    min_steps_per_stage: int = 20,
    max_steps_per_stage: int = 400,
    max_passes: int = 20,
    tol_Q: Q_ = Q_(1e-3, "W"),
    tol_end: Q_ = Q_(1e-3, "J/kg"),
    log_level: str = "INFO",
) -> tuple[List[StageResult], GasStream, WaterStream]:
    setup_logging(level=log_level)
    log = logging.getLogger("solver")

    if len(stages) != 6:
        raise ValueError(f"Expected 6 stages. Got {len(stages)}.")

    if target_dx is None:
        dx_target = (_median_length(stages) / 100).to("m")
    else:
        dx_target = target_dx.to("m")

    n_steps_by_stage: List[int] = []
    for st in stages:
        L = st.spec["inner_length"].to("m")
        n = _clamp(int(ceil((L / dx_target).to("").magnitude)), min_steps_per_stage, max_steps_per_stage)
        n_steps_by_stage.append(n)

    prev_Q_total: Optional[Q_] = None
    prev_end_h: Optional[Tuple[Q_, Q_, Q_, Q_]] = None
    final_stage_results: List[StageResult] = []

    h_g_in = _gasprops.h(gas_in.T, gas_in.P, gas_in.comp)
    h_w_in = water_in.h

    for p in range(max_passes + 1):
        gas_stage_results: List[StageResult] = []
        gas_at_stage_in: List[GasStream] = []
        water_for_stage_boundary: List[WaterStream] = []

        g = gas_in
        for i, st in enumerate(stages):
            if p == 0:
                w_boundary = water_in
            else:
                w_boundary = final_stage_results[i].steps[0].water

            gas_at_stage_in.append(g)
            water_for_stage_boundary.append(w_boundary)

            g, w_tmp, st_res = solve_stage(g, w_boundary, st, n_steps_by_stage[i], stage_index=i)
            gas_stage_results.append(st_res)

        water_stage_results: List[StageResult] = []
        g_fields_for_water: List[GasStream] = [gs for gs in gas_at_stage_in]

        w = water_in
        for i_rev, st in enumerate(reversed(stages)):
            idx = 5 - i_rev
            g_for_stage = g_fields_for_water[idx]
            g_new, w, st_res = solve_stage(g_for_stage, w, st, n_steps_by_stage[idx], stage_index=idx)
            g_fields_for_water[idx] = g_new
            water_stage_results.append(st_res)

        water_stage_results = list(reversed(water_stage_results))

        Q_total = sum([sr.Q_stage.to("W") for sr in water_stage_results], Q_(0.0, "W")).to("W")

        g_out = gas_stage_results[-1].steps[-1].gas
        w_out = water_stage_results[0].steps[-1].water

        h_g_out = _gasprops.h(g_out.T, g_out.P, g_out.comp)
        h_w_out = w_out.h

        end_tuple = (h_g_in, h_g_out, h_w_in, h_w_out)

        duty_ok = prev_Q_total is not None and abs(Q_total - prev_Q_total) < tol_Q
        end_ok = prev_end_h is not None and max(
            abs(end_tuple[0] - prev_end_h[0]),
            abs(end_tuple[1] - prev_end_h[1]),
            abs(end_tuple[2] - prev_end_h[2]),
            abs(end_tuple[3] - prev_end_h[3]),
        ) < tol_end

        log.info(
            f"pass {p}: Q_total={Q_total:~P} "
            f"ΔQ={(Q_total - (prev_Q_total or Q_(0,'W'))):~P} "
            f"max Δends={max( (abs(end_tuple[i] - (prev_end_h[i] if prev_end_h else end_tuple[i])) for i in range(4)), default=Q_(0,'J/kg')):~P} "
            f"converged={'yes' if (duty_ok and end_ok) else 'no'}",
            extra={"stage": "ALL", "step": f"pass {p}"},
        )

        if duty_ok and end_ok:
            water_boundaries = [sr.steps[0].water for sr in water_stage_results]
            g = gas_in
            final_forward_results: List[StageResult] = []
            w_out_sync = None

            for i, st in enumerate(stages):
                w_boundary = water_boundaries[i]
                g, w_tmp, st_res = solve_stage(g, w_boundary, st, n_steps_by_stage[i], stage_index=i)
                final_forward_results.append(st_res)
                if i == 0:
                    w_out_sync = w_tmp

            g_out_sync = g

            h_g_out = _gasprops.h(g_out_sync.T, g_out_sync.P, g_out_sync.comp)
            h_w_out = w_out_sync.h
            Q_gas = (gas_in.mass_flow * (h_g_in - h_g_out)).to("W")
            Q_wat = (water_in.mass_flow * (h_w_out - h_w_in)).to("W")
            mismatch = abs(Q_gas - Q_wat) / (abs(Q_wat) + Q_(1e-12, "W"))

            log.info(
                f"FINAL forward: Q_total={sum((sr.Q_stage for sr in final_forward_results), Q_(0,'W')):~P} "
                f"Q_gas={Q_gas:~P} Q_water={Q_wat:~P} rel_err={mismatch:~P}",
                extra={"stage": "ALL", "step": "final_forward"},
            )

            if mismatch.magnitude > 0.005:
                raise RuntimeError(
                    f"Energy mismatch >0.5% on final sweep. "
                    f"Q_gas={Q_gas:~P}, Q_water={Q_wat:~P}, rel_err={mismatch:~P}"
                )

            return final_forward_results, g_out_sync, w_out_sync

        prev_Q_total = Q_total
        prev_end_h = end_tuple
        final_stage_results = water_stage_results

    worst_idx = max(range(6), key=lambda k: abs(final_stage_results[k].Q_stage).to("W").magnitude if final_stage_results else 0)
    raise RuntimeError(
        f"Did not converge in {max_passes} passes. "
        f"last_Q_total={prev_Q_total:~P if prev_Q_total else 'n/a'} "
        f"last_end_delta={prev_end_h if prev_end_h else 'n/a'} "
        f"worst_stage_index={worst_idx}"
    )
