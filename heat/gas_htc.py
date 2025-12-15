from __future__ import annotations
from typing import Dict, Any, Tuple
import numpy as np
from common.units import Q_
from common.models import GasStream
from common.props import GasProps
from combustion.mass_mole import to_mole

_gas = GasProps(mech_path="config/flue_cantera.yaml", phase="gas_mix")

def cp_gas(g: GasStream) -> Q_:
    return _gas.cp(g.T, g.P, g.comp or {})

def _gas_partials(g):
    P = g.P.to("Pa").magnitude
    Y = {k: v.to("").magnitude for k,v in (g.comp or {}).items()}
    X = to_mole(Y)
    xH2O = X.get("H2O", 0.0)
    xCO2 = X.get("CO2", 0.0)
    return xH2O * P, xCO2 * P

_A = np.array([0.434, 0.313, 0.180, 0.073])
_K = np.array([0.0, 2.3, 11.6, 30.4])

def _mean_beam_length(spec: dict) -> Q_:
    if "rad_Lb" in spec:
        return spec["rad_Lb"].to("m")
    Dh = spec["hot_Dh"].to("m")
    return (0.9 * Dh).to("m")

def emissivity(T_K: float, pH2O_Pa: float, pCO2_Pa: float, L_m: float, *, Texp: float = 0.65) -> float:
    T = float(np.clip(T_K, 300.0, 3000.0))
    scale_T = (T / 1000.0) ** Texp

    p_ratio = (pH2O_Pa + pCO2_Pa) / 101325.0
    tau = (_K * scale_T) * p_ratio * L_m

    eps = 1.0 - float(np.sum(_A * np.exp(-tau)))
    return float(np.clip(eps, 0.0, 1.0))

def h_rad(Tfilm_K: float, eps_g: float, F: float = 1.0) -> float:
    sigma = 5.670374419e-8
    return 4.0 * sigma * F * eps_g * Tfilm_K**3

def h_gas_rad_smith(T_K: float, pH2O_Pa: float, pCO2_Pa: float, L_m: float, Twall_K: float, F: float = 1.0, *, Texp: float = 0.65) -> float:
    eps = emissivity(T_K, pH2O_Pa, pCO2_Pa, L_m, Texp=Texp)
    Tfilm = 0.5 * (T_K + Twall_K)
    return h_rad(Tfilm, eps, F)

def _h_rad(g: GasStream, spec: Dict[str, Any], Tgw: Q_) -> Q_:
    Tg = g.T
    pH2O, pCO2 = _gas_partials(g)
    Lb = _mean_beam_length(spec).to("m").magnitude
    F = float(spec.get("rad_F", 1.0))
    Texp = float(spec.get("rad_Texp", 0.65))
    h_val = h_gas_rad_smith(Tg.to("K").magnitude, pH2O, pCO2, Lb, Tgw.to("K").magnitude, F, Texp=Texp)
    return Q_(max(h_val, 0.0), "W/m^2/K")

def _reynolds(rho: Q_, V: Q_, D: Q_, mu: Q_) -> float:
    Re = (rho * V * D / mu).to("").magnitude
    return max(Re, 1e-12)

def _prandtl(cp: Q_, mu: Q_, k: Q_) -> float:
    Pr = (cp * mu / k).to("").magnitude
    return max(Pr, 1e-12)

def _vel_internal(g: GasStream, A: Q_) -> Q_:
    rho = _gas.rho(g.T, g.P, g.comp)
    return (g.mass_flow / (rho * A)).to("m/s")

def _vel_external(g: GasStream, A_bulk: Q_, umax_factor: Q_ | float | None) -> Q_:
    rho = _gas.rho(g.T, g.P, g.comp)
    V_bulk = (g.mass_flow / (rho * A_bulk)).to("m/s")
    if umax_factor is None:
        return V_bulk
    f = umax_factor if isinstance(umax_factor, (int, float)) else umax_factor.to("").magnitude
    return (max(f, 1.0) * V_bulk).to("m/s")

def _nu_internal(Re: float, Pr: float, D: Q_, L: Q_) -> float:
    if Re < 2300.0:
        Gz = Re * Pr * (D.to("m").magnitude / max(L.to("m").magnitude, 1e-12))
        return 3.66 + 0.0668 * Gz / (1.0 + 0.04 * (Gz ** (2.0/3.0)))
    f = (0.79 * np.log(Re) - 1.64) ** -2
    num = (f/8.0) * (Re - 1000.0) * Pr
    den = 1.0 + 12.7 * np.sqrt(f/8.0) * ((Pr ** (2.0/3.0)) - 1.0)
    return max(num / max(den, 1e-12), 1e-12)

def _nu_churchill_bernstein(Re: float, Pr: float) -> float:
    a = 0.3
    b = (0.62 * Re**0.5 * Pr**(1/3.0)) / ((1.0 + (0.4/Pr)**(2.0/3.0)) ** 0.25)
    c = (1.0 + (Re / 282000.0) ** (5.0/8.0)) ** (4.0/5.0)
    return max(a + b * c, 1e-12)

def _nu_zukauskas(Re: float, Pr: float, arrangement: str) -> float | None:
    bands = [
        (1e3, 2e3, {"inline": (0.90, 0.40), "staggered": (1.04, 0.40)}),
        (2e3, 4e3, {"inline": (0.52, 0.50), "staggered": (0.71, 0.50)}),
        (4e3, 1e5, {"inline": (0.27, 0.63), "staggered": (0.35, 0.60)}),
        (1e5, 2e6, {"inline": (0.021, 0.84), "staggered": (0.022, 0.84)}),
    ]
    C = m = None
    arr = "staggered" if arrangement == "staggered" else "inline"
    for Re_min, Re_max, table in bands:
        if Re_min <= Re < Re_max:
            C, m = table[arr]
            break
    if C is None:
        return None
    n = 0.36 if Pr <= 10.0 else 0.25
    return max(C * (Re**m) * (Pr**n), 1e-12)

def _h_from_Nu(Nu: float, k: Q_, D: Q_) -> Q_:
    return (Q_(Nu, "") * k / D).to("W/m^2/K")

def _h_conv_internal(g: GasStream, spec: dict) -> Q_:
    D = spec["inner_diameter"].to("m")
    L = spec["inner_length"].to("m")
    A = spec["hot_flow_A"].to("m^2")

    V   = _vel_internal(g, A)
    rho = _gas.rho(g.T, g.P, g.comp)
    mu  = _gas.mu(g.T, g.P, g.comp)
    k   = _gas.k(g.T, g.P, g.comp)
    cp  = _gas.cp(g.T, g.P, g.comp)

    Re = _reynolds(rho, V, D, mu)
    Pr = _prandtl(cp, mu, k)

    Nu = _nu_internal(Re, Pr, D, L)
    return _h_from_Nu(Nu, k, D)

def _h_conv_economiser_external(g: GasStream, spec: dict) -> Q_:
    D = spec["outer_diameter"].to("m")
    A_bulk = spec["hot_flow_A"].to("m^2")
    umax = spec.get("umax_factor", None)

    V   = _vel_external(g, A_bulk, umax)
    rho = _gas.rho(g.T, g.P, g.comp)
    mu  = _gas.mu(g.T, g.P, g.comp)
    k   = _gas.k(g.T, g.P, g.comp)
    cp  = _gas.cp(g.T, g.P, g.comp)

    Re = _reynolds(rho, V, D, mu)
    Pr = _prandtl(cp, mu, k)

    arrangement = spec.get("arrangement", "inline")
    Nu_z = _nu_zukauskas(Re, Pr, arrangement)
    if Nu_z is None:
        Nu_z = _nu_churchill_bernstein(Re, Pr)
    return _h_from_Nu(Nu_z, k, D)

def gas_htc_parts(g: GasStream, spec: dict, Tgw: Q_, *, stage_kind: str | None = None) -> Tuple[Q_, Q_]:
    kind = (stage_kind or spec.get("stage_kind") or "single_tube").lower()

    if kind in ("single_tube", "reversal_chamber", "tube_bank"):
        h_conv = _h_conv_internal(g, spec)
    elif kind == "economiser":
        h_conv = _h_conv_economiser_external(g, spec)
    else:
        h_conv = _h_conv_internal(g, spec)

    h_rad = _h_rad(g, spec, Tgw)
    return h_conv.to("W/m^2/K"), h_rad.to("W/m^2/K")

def gas_htc(g: GasStream, spec: dict, Tgw: Q_, *, stage_kind: str | None = None) -> Q_:
    h_conv, h_rad = gas_htc_parts(g, spec, Tgw, stage_kind=stage_kind)
    return (h_conv + h_rad).to("W/m^2/K")
