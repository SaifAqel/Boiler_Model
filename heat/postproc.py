from __future__ import annotations
import pandas as pd
from common.results import GlobalProfile, CombustionResult
from common.props import WaterProps, GasProps
from common.units import Q_
from heat.gas_htc import emissivity 
from combustion.mass_mole import to_mole

_gas = GasProps()

def _mag_or_nan(q, unit):
    return q.to(unit).magnitude if q is not None else float("nan")

def profile_to_dataframe(gp: "GlobalProfile", *, remap_water: bool = True) -> "pd.DataFrame":
    stage_ranges: dict[int, tuple[int, int]] = {}
    for i in range(len(gp.x)):
        k = gp.stage_index[i]
        if k not in stage_ranges:
            stage_ranges[k] = [i, i]
        else:
            stage_ranges[k][1] = i
    stage_ranges = {k: (v[0], v[1]) for k, v in stage_ranges.items()}

    stage_offsets: dict[int, Q_] = {}
    offset = Q_(0.0, "m")
    for k, sr in enumerate(gp.stage_results):
        stage_offsets[k] = offset
        if sr.steps:
            last = sr.steps[-1]
            offset = (offset + last.x + last.dx).to("m")

    rows = []
    for i in range(len(gp.x)):
        g = gp.gas[i]

        k_stage = gp.stage_index[i]
        disable_water_hydraulics = (k_stage <= 4)
        sr_stage = gp.stage_results[k_stage]
        A_hot = sr_stage.hot_flow_A
        A_cold = sr_stage.cold_flow_A
        Dh_hot = sr_stage.hot_Dh
        Dh_cold = sr_stage.cold_Dh

        if remap_water:
            i0, iN = stage_ranges[gp.stage_index[i]]
            i_local = i - i0
            j = iN - i_local
        else:
            j = i

        w = gp.water[j]

        xq = WaterProps.quality_from_Ph(w.P, w.h)
        Two_phase = xq is not None

        if Two_phase:
            Tw = WaterProps.Tsat(w.P)
            w_cp = w_mu = w_k = None
            w_rho = WaterProps.rho_from_Px(w.P, xq) if xq is not None else None
        else:
            Tw   = WaterProps.T_from_Ph(w.P, w.h)
            w_cp = WaterProps.cp_from_Ph(w.P, w.h)
            w_mu = WaterProps.mu_from_Ph(w.P, w.h)
            w_k  = WaterProps.k_from_Ph(w.P, w.h)
            w_rho = WaterProps.rho_from_Ph(w.P, w.h)

        g_h   = _gas.h_sensible(g.T, g.P, g.comp)
        g_cp  = _gas.cp(g.T, g.P, g.comp)
        g_mu  = _gas.mu(g.T, g.P, g.comp)
        g_k   = _gas.k(g.T, g.P, g.comp)
        g_rho = _gas.rho(g.T, g.P, g.comp)

        gas_V = (g.mass_flow / (g_rho * A_hot)).to("m/s")
        Re_gas = (g_rho * gas_V * Dh_hot / g_mu).to("").magnitude

        if w_rho is not None and A_cold is not None:
            water_V = (w.mass_flow / (w_rho * A_cold)).to("m/s")
        else:
            water_V = None

        if w_rho is not None and w_mu is not None and water_V is not None:
            Re_water = (w_rho * water_V * Dh_cold / w_mu).to("").magnitude
        else:
            Re_water = float("nan")

        if disable_water_hydraulics:
            water_V = None
            Re_water = float("nan")
            w_cp = w_mu = w_k = w_rho = None
            w_dP_fric = w_dP_minor = w_dP_tot = float("nan")
        else:
            if Two_phase:
                Tw = WaterProps.Tsat(w.P)
                w_cp = w_mu = w_k = None
                w_rho = WaterProps.rho_from_Px(w.P, xq) if xq is not None else None
            else:
                Tw   = WaterProps.T_from_Ph(w.P, w.h)
                w_cp = WaterProps.cp_from_Ph(w.P, w.h)
                w_mu = WaterProps.mu_from_Ph(w.P, w.h)
                w_k  = WaterProps.k_from_Ph(w.P, w.h)
                w_rho = WaterProps.rho_from_Ph(w.P, w.h)

            if w_rho is not None and A_cold is not None:
                water_V = (w.mass_flow / (w_rho * A_cold)).to("m/s")
            else:
                water_V = None

            if w_rho is not None and w_mu is not None and water_V is not None:
                Re_water = (w_rho * water_V * Dh_cold / w_mu).to("").magnitude
            else:
                Re_water = float("nan")

            w_dP_fric = gp.w_dP_fric[i].to("Pa").magnitude
            w_dP_minor = gp.w_dP_minor[i].to("Pa").magnitude
            w_dP_tot = gp.w_dP_tot[i].to("Pa").magnitude

        Y = {sp: float(q.to("").magnitude) for sp, q in (g.comp or {}).items()}
        X = to_mole(Y)

        xH2O = X.get("H2O", 0.0)
        xCO2 = X.get("CO2", 0.0)

        P_Pa = g.P.to("Pa").magnitude
        pH2O = xH2O * P_Pa
        pCO2 = xCO2 * P_Pa

        Lb_m = (0.9 * Dh_hot).to("m").magnitude
        gas_eps = emissivity(
            g.T.to("K").magnitude,
            pH2O,
            pCO2,
            Lb_m,
        )

        x_local = gp.x[i].to("m")
        x_global = (stage_offsets[k_stage] + x_local).to("m")

        row = {
            "stage_name": gp.stage_name[i],
            "i": i,
            "x[m]": x_global.magnitude,
            "dx[m]": gp.dx[i].to("m").magnitude,
            "qprime[MW/m]": gp.qprime[i].to("MW/m").magnitude,
            "UA_prime[MW/K/m]": gp.UA_prime[i].to("MW/K/m").magnitude,
            "gas_P[Pa]": g.P.to("Pa").magnitude,
            "gas_T[°C]": g.T.to("degC").magnitude,
            "gas_h[kJ/kg]": g_h.to("kJ/kg").magnitude,
            "water_P[Pa]": w.P.to("Pa").magnitude,
            "water_T[°C]": Tw.to("degC").magnitude,
            "water_h[kJ/kg]": w.h.to("kJ/kg").magnitude,
            "gas_eps[-]": gas_eps,
            "water_x[-]": _mag_or_nan(xq, ""),
            "boiling": "true" if xq is not None else "false",
            "gas_V[m/s]": gas_V.to("m/s").magnitude,
            "Re_gas[-]": Re_gas,
            "h_gas[W/m^2/K]": gp.h_g[i].to("W/m^2/K").magnitude,
            "water_V[m/s]": (_mag_or_nan(water_V, "m/s") if isinstance(water_V, Q_) else float("nan")),
            "Re_water[-]": Re_water,
            "h_water[W/m^2/K]": gp.h_c[i].to("W/m^2/K").magnitude,
            "dP_fric[Pa]": gp.dP_fric[i].to("Pa").magnitude,
            "dP_minor[Pa]": gp.dP_minor[i].to("Pa").magnitude,
            "dP_total[Pa]": gp.dP_total[i].to("Pa").magnitude,
            "water_dP_fric[Pa]":  (w_dP_fric if disable_water_hydraulics else gp.w_dP_fric[i].to("Pa").magnitude),
            "water_dP_minor[Pa]": (w_dP_minor if disable_water_hydraulics else gp.w_dP_minor[i].to("Pa").magnitude),
            "water_dP_total[Pa]": (w_dP_tot if disable_water_hydraulics else gp.w_dP_tot[i].to("Pa").magnitude),
            "water_cp[kJ/kg/K]": _mag_or_nan(w_cp, "kJ/kg/K"),
            "water_mu[Pa*s]": _mag_or_nan(w_mu, "Pa*s"),
            "water_k[W/m/K]": _mag_or_nan(w_k, "W/m/K"),
            "water_rho[kg/m^3]": _mag_or_nan(w_rho, "kg/m^3"),
        }

        rows.append(row)

    return pd.DataFrame(rows)


def summary_from_profile(gp: "GlobalProfile", combustion: CombustionResult | None = None, drum_pressure: Q_ | None = None) -> tuple[list[dict], float, float]:
    rows = []
    Q_total = 0.0
    UA_total = 0.0
    Q_total_conv = 0.0
    Q_total_rad  = 0.0 
    dP_total_fric = 0.0
    dP_total_minor = 0.0
    dP_total_total = 0.0
    w_dP_tot_fric = 0.0
    w_dP_tot_minor = 0.0
    w_dP_tot_total = 0.0 
    stack_T_C = None
    feedwater_mdot_kg_s = None
    circulation_mdot_kg_s = None
    flue_mdot_kg_s = None
    boiler_water_in_P_Pa = None
    boiler_water_in_T_C = None
    boiler_water_out_T_C = None
    boiler_water_Tsat_C = None
    econ_out_h_Jkg = None
    feedwater_mdot_q = None


    import itertools
    for k, grp in itertools.groupby(range(len(gp.x)), key=lambda i: gp.stage_index[i]):
        disable_water_hydraulics = (k <= 4) 
        idxs = list(grp)
        name = gp.stage_name[idxs[0]]
        sr_stage = gp.stage_results[k]

        A_hot = sr_stage.hot_flow_A
        A_cold = sr_stage.cold_flow_A

        gas_V_sum = 0.0
        water_V_sum = 0.0
        n_steps = len(idxs)

        for i in idxs:
            g = gp.gas[i]
            w = gp.water[i]

            g_rho = _gas.rho(g.T, g.P, g.comp)
            gas_V = (g.mass_flow / (g_rho * A_hot)).to("m/s").magnitude
            gas_V_sum += gas_V

            if A_cold is not None:
                w_rho = WaterProps.rho_from_Ph(w.P, w.h)
                water_V = (w.mass_flow / (w_rho * A_cold)).to("m/s").magnitude
                water_V_sum += water_V

        gas_V_avg = gas_V_sum / max(n_steps, 1)
        if disable_water_hydraulics or A_cold is None:
            water_V_avg = float("nan")
        else:
            water_V_avg = water_V_sum / max(n_steps, 1)

        Q_stage = sum((gp.qprime[i] * gp.dx[i]).to("MW").magnitude for i in idxs)
        UA_stage = sum((gp.UA_prime[i] * gp.dx[i]).to("MW/K").magnitude for i in idxs)

        Q_stage_conv = sum((st.qprime_conv * st.dx).to("MW").magnitude for st in sr_stage.steps)
        Q_stage_rad  = sum((st.qprime_rad  * st.dx).to("MW").magnitude for st in sr_stage.steps)

        dP_fric = sum(gp.dP_fric[i].to("Pa").magnitude for i in idxs)
        dP_minor = sum(gp.dP_minor[i].to("Pa").magnitude for i in idxs)
        dP_total = sum(gp.dP_total[i].to("Pa").magnitude for i in idxs)
    
        w_dP_fric = sum(gp.w_dP_fric[i].to("Pa").magnitude for i in idxs)
        w_dP_minor = sum(gp.w_dP_minor[i].to("Pa").magnitude for i in idxs)
        w_dP_tot = sum(gp.w_dP_tot[i].to("Pa").magnitude for i in idxs) 

        g_in  = gp.gas[idxs[0]]
        g_out = gp.gas[idxs[-1]]

        gas_in_T  = g_in.T.to("degC").magnitude
        gas_out_T = g_out.T.to("degC").magnitude

        gas_in_P  = g_in.P.to("Pa").magnitude
        gas_out_P = g_out.P.to("Pa").magnitude

        gas_in_h  = _gas.h_sensible(g_in.T,  g_in.P,  g_in.comp).to("kJ/kg").magnitude
        gas_out_h = _gas.h_sensible(g_out.T, g_out.P, g_out.comp).to("kJ/kg").magnitude

        w_in  = gp.water[idxs[0]]
        w_out = gp.water[idxs[-1]]

        water_in_h  = w_in.h.to("kJ/kg").magnitude
        water_out_h = w_out.h.to("kJ/kg").magnitude

        water_in_P  = w_in.P.to("Pa").magnitude
        water_out_P = w_out.P.to("Pa").magnitude

        water_in_T  = WaterProps.T_from_Ph(w_in.P,  w_in.h).to("degC").magnitude
        water_out_T = WaterProps.T_from_Ph(w_out.P, w_out.h).to("degC").magnitude

        if flue_mdot_kg_s is None:
            flue_mdot_kg_s = g_in.mass_flow.to("kg/s").magnitude

        if k == 0:
            boiler_water_out_T_C = water_out_T

        if k == len(gp.stage_results) - 1:
            boiler_water_in_T_C = water_in_T
            boiler_water_in_P_Pa = water_in_P

            try:
                feedwater_mdot_q = gp.stage_results[k].steps[0].water.mass_flow.to("kg/s")
                feedwater_mdot_kg_s = feedwater_mdot_q.magnitude
            except Exception:
                feedwater_mdot_q = None
                feedwater_mdot_kg_s = None

            try:
                econ_out_h_Jkg = w_out.h.to("J/kg")
            except Exception:
                econ_out_h_Jkg = None



        row = {
            "stage_index": k,
            "stage_name": name,
            "stage_kind": gp.stage_results[k].stage_kind,
            "Q_stage[MW]": Q_stage,
            "UA_stage[MW/K]": UA_stage,
            "gas_V_avg[m/s]": gas_V_avg,
            "water_V_avg[m/s]": water_V_avg,
            "gas_in_P[Pa]": gas_in_P,
            "gas_in_T[°C]": gas_in_T,
            "gas_in_h[kJ/kg]": gas_in_h,
            "gas_out_P[Pa]": gas_out_P,
            "gas_out_T[°C]": gas_out_T,
            "gas_out_h[kJ/kg]": gas_out_h,
            "water_in_P[Pa]": water_in_P,
            "water_in_T[°C]": water_in_T,
            "water_in_h[kJ/kg]": water_in_h,
            "water_out_P[Pa]": water_out_P,
            "water_out_T[°C]": water_out_T,
            "water_out_h[kJ/kg]": water_out_h,
            "ΔP_stage_fric[Pa]": dP_fric,
            "ΔP_stage_minor[Pa]": dP_minor,
            "ΔP_stage_total[Pa]": dP_total,
            "ΔP_water_stage_fric[Pa]": (float("nan") if disable_water_hydraulics else w_dP_fric),
            "ΔP_water_stage_minor[Pa]": (float("nan") if disable_water_hydraulics else w_dP_minor),
            "ΔP_water_stage_total[Pa]": (float("nan") if disable_water_hydraulics else w_dP_tot),
            "Q_conv_stage[MW]": Q_stage_conv,
            "Q_rad_stage[MW]": Q_stage_rad,
            "steam_capacity[kg/s]": "",
            "steam_capacity[t/h]": "",
            "η_direct[-]": "",
            "η_indirect[-]": "",
            "Q_total_useful[MW]": "",
            "Q_in_total[MW]": "",
            "P_LHV[MW]": "",
            "LHV_mass[kJ/kg]": "",
            "flue_mdot[kg/s]": "",
            "boiler_water_in_T[°C]": "",
            "boiler_water_out_T[°C]": "",
            "boiler_water_P[Pa]": "",
            "boiler_water_Tsat[°C]": "",
        }
        
        rows.append(row)

        Q_total += Q_stage
        UA_total += UA_stage
        Q_total_conv += Q_stage_conv
        Q_total_rad  += Q_stage_rad
        dP_total_fric  += dP_fric
        dP_total_minor += dP_minor
        dP_total_total += dP_total
        w_dP_tot_fric  += w_dP_fric
        w_dP_tot_minor += w_dP_minor
        w_dP_tot_total += w_dP_tot
        stack_T_C = gas_out_T

    steam_capacity_total_kg_s = None
    steam_capacity_total_tph = None

    P_for_evap: Q_ | None = drum_pressure
    if P_for_evap is None and boiler_water_in_P_Pa is not None:
        P_for_evap = Q_(boiler_water_in_P_Pa, "Pa")

    if P_for_evap is not None:
        P_q = P_for_evap.to("Pa")
        boiler_water_Tsat_C = WaterProps.Tsat(P_q).to("degC").magnitude

        hf = WaterProps.h_f(P_q).to("J/kg")
        hg = WaterProps.h_g(P_q).to("J/kg")

        evap_stage_names = {f"HX_{i}" for i in range(1, 6)}
        Q_evap_W = 0.0
        for r in rows:
            if r.get("stage_name") in evap_stage_names and isinstance(r.get("Q_stage[MW]"), (int, float)):
                Q_evap_W += Q_(r["Q_stage[MW]"], "MW").to("W").magnitude
        Q_evap = Q_(Q_evap_W, "W")

        if feedwater_mdot_q is not None and econ_out_h_Jkg is not None:
            x_out = 1.0
            h_s = (hf + Q_(x_out, "") * (hg - hf)).to("J/kg")
            denom = (h_s - hf).to("J/kg")

            if denom.magnitude > 0:
                m_s_q = (Q_evap + feedwater_mdot_q * (econ_out_h_Jkg - hf)) / denom
                m_s_q = m_s_q.to("kg/s")
                steam_capacity_total_kg_s = m_s_q.magnitude
                steam_capacity_total_tph = m_s_q.to("tonne/hour").magnitude
            else:
                steam_capacity_total_kg_s = None
                steam_capacity_total_tph = None
        else:
            steam_capacity_total_kg_s = None
            steam_capacity_total_tph = None

        for r in rows:
            if r.get("stage_name") in evap_stage_names and isinstance(r.get("Q_stage[MW]"), (int, float)):
                Q_stage_W = Q_(r["Q_stage[MW]"], "MW").to("W")
                m_s_stage = (Q_stage_W / denom).to("kg/s")
                r["steam_capacity[kg/s]"] = m_s_stage.magnitude
                r["steam_capacity[t/h]"]  = m_s_stage.to("tonne/hour").magnitude

        if steam_capacity_total_kg_s is not None:
            steam_capacity_total_tph = Q_(steam_capacity_total_kg_s, "kg/s").to("tonne/hour").magnitude
        else:
            steam_capacity_total_tph = None


    Q_useful = Q_total

    Q_in_total = None
    P_LHV_W = None
    LHV_mass_kJkg = None
    eta_direct = None
    eta_indirect = None

    if combustion is not None:
        Q_in_total = combustion.Q_in.to("MW").magnitude

        if combustion.fuel_P_LHV is not None:
            P_LHV_W = combustion.fuel_P_LHV.to("MW").magnitude
        else:
            P_LHV_W = combustion.LHV.to("MW").magnitude

        if combustion.fuel_LHV_mass is not None:
            LHV_mass_kJkg = combustion.fuel_LHV_mass.to("kJ/kg").magnitude

        if P_LHV_W and P_LHV_W > 0.0:
            eta_direct = Q_useful / P_LHV_W

        if Q_in_total and Q_in_total > 0.0:
            eta_indirect = Q_useful / Q_in_total

    total_row = {
        "stage_index": "",
        "stage_name": "TOTAL_BOILER",
        "stage_kind": "",
        "Q_stage[MW]": Q_useful,
        "UA_stage[MW/K]": UA_total,
        "gas_V_avg[m/s]": "",
        "water_V_avg[m/s]": "",
        "gas_in_P[Pa]": "",
        "gas_in_T[°C]": "",
        "gas_in_h[kJ/kg]": "",
        "gas_out_P[Pa]": "",
        "gas_out_T[°C]": "",
        "gas_out_h[kJ/kg]": "",
        "water_in_P[Pa]": "",
        "water_in_T[°C]": "",
        "water_in_h[kJ/kg]": "",
        "water_out_P[Pa]": "",
        "water_out_T[°C]": "",
        "water_out_h[kJ/kg]": "",
        "ΔP_stage_fric[Pa]": dP_total_fric,
        "ΔP_stage_minor[Pa]": dP_total_minor,
        "ΔP_stage_total[Pa]": dP_total_total,
        "ΔP_water_stage_fric[Pa]": w_dP_tot_fric,
        "ΔP_water_stage_minor[Pa]": w_dP_tot_minor,
        "ΔP_water_stage_total[Pa]": w_dP_tot_total, 
        "stack_temperature[°C]": stack_T_C,
        "feedwater_mdot[kg/s]": feedwater_mdot_kg_s if feedwater_mdot_kg_s is not None else "",
        "circulation_mdot[kg/s]": circulation_mdot_kg_s if circulation_mdot_kg_s is not None else "",
        "Q_conv_stage[MW]": Q_total_conv,
        "Q_rad_stage[MW]": Q_total_rad,
        "steam_capacity[kg/s]": steam_capacity_total_kg_s,
        "steam_capacity[t/h]": steam_capacity_total_tph,
        "η_direct[-]": eta_direct if eta_direct is not None else "",
        "η_indirect[-]": eta_indirect if eta_indirect is not None else "",
        "Q_total_useful[MW]": Q_useful,
        "Q_in_total[MW]": Q_in_total if Q_in_total is not None else "",
        "P_LHV[MW]": P_LHV_W if P_LHV_W is not None else "",
        "LHV_mass[kJ/kg]": LHV_mass_kJkg if LHV_mass_kJkg is not None else "",
        "flue_mdot[kg/s]": flue_mdot_kg_s if flue_mdot_kg_s is not None else "",
        "boiler_water_in_T[°C]": boiler_water_in_T_C if boiler_water_in_T_C is not None else "",
        "boiler_water_out_T[°C]": boiler_water_out_T_C if boiler_water_out_T_C is not None else "",
        "boiler_water_P[Pa]": boiler_water_in_P_Pa if boiler_water_in_P_Pa is not None else "",
        "boiler_water_Tsat[°C]": boiler_water_Tsat_C if boiler_water_Tsat_C is not None else "",
    }


    rows.append(total_row)

    return rows, Q_total, UA_total
