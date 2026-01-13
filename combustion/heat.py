from common.units import Q_
import re
import cantera as ct
from common.props import WaterProps, GasProps
from common.models import GasStream
from combustion.mass_mole import to_mole
from common.constants import molar_masses, T_ref, P_ref, O2_per_mol

_gasprops = GasProps()

def parse_CH(s: str):
    m = re.fullmatch(r'C(\d*)H(\d+)', s)
    if not m: return None, None
    C = int(m.group(1)) if m.group(1) else 1
    H = int(m.group(2))
    return C, H

def compute_LHV_HHV(fuel: GasStream, air: GasStream) -> tuple[Q_, Q_, Q_, Q_]:
    gas = ct.Solution("config/flue_cantera.yaml", "gas_mix")

    fuel_x = to_mole({k: float(v.to("").magnitude) for k, v in (fuel.comp or {}).items()
                      if float(v.to("").magnitude) > 0.0})
    if not fuel_x:
        raise ValueError("compute_LHV_HHV: empty fuel composition")

    air_x = to_mole({k: float(v.to("").magnitude) for k, v in (air.comp or {}).items()
                     if float(v.to("").magnitude) > 0.0})
    if not air_x or air_x.get("O2", 0.0) <= 0.0:
        raise ValueError("compute_LHV_HHV: air composition missing O2")

    def xf(sp: str) -> float:
        return float(fuel_x.get(sp, 0.0))

    def xa(sp: str) -> float:
        return float(air_x.get(sp, 0.0))

    O2_req = 0.0
    for sp, x in fuel_x.items():
        req = O2_per_mol.get(sp, Q_(0.0, "")).to("").magnitude
        O2_req += float(x) * float(req)

    n_air = O2_req / max(xa("O2"), 1e-30)

    n_react = {}
    for sp, x in fuel_x.items():
        if x > 0.0:
            n_react[sp] = n_react.get(sp, 0.0) + x

    for sp, x in air_x.items():
        if x > 0.0:
            n_react[sp] = n_react.get(sp, 0.0) + n_air * x

    nR_tot = sum(n_react.values())
    X_react = {sp: n / nR_tot for sp, n in n_react.items() if n > 0.0}

    n_CO2 = n_air * xa("CO2") + xf("CO2") + (xf("CH4") + 2*xf("C2H6") + 3*xf("C3H8") + 4*xf("C4H10"))
    n_H2O = n_air * xa("H2O") + xf("H2O") + (2*xf("CH4") + 3*xf("C2H6") + 4*xf("C3H8") + 5*xf("C4H10")) + xf("H2S")
    n_SO2 = xf("H2S")
    n_O2  = n_air * xa("O2") - O2_req
    n_N2  = n_air * xa("N2") + xf("N2")
    n_Ar  = n_air * xa("Ar")

    n_prod = {
        "CO2": n_CO2,
        "H2O": n_H2O,
        "SO2": n_SO2,
        "O2":  n_O2,
        "N2":  n_N2,
        "Ar":  n_Ar,
    }
    for k in list(n_prod.keys()):
        if n_prod[k] < 0.0 and abs(n_prod[k]) < 1e-12:
            n_prod[k] = 0.0

    nP_tot = sum(v for v in n_prod.values() if v > 0.0)
    if nP_tot <= 0.0:
        raise ValueError("compute_LHV_HHV: empty products")

    X_prod = {sp: n / nP_tot for sp, n in n_prod.items() if n > 0.0}

    T0 = T_ref.to("K").magnitude
    P0 = P_ref.to("Pa").magnitude

    gas.TPX = T0, P0, X_react
    hR_molar = gas.enthalpy_mole

    gas.TPX = T0, P0, X_prod
    hP_molar = gas.enthalpy_mole

    HR = hR_molar * (nR_tot / 1000.0)
    HP = hP_molar * (nP_tot / 1000.0)

    LHV_mol_J = HR - HP
    if LHV_mol_J <= 0.0:
        raise ValueError(f"compute_LHV_HHV: non-positive LHV ({LHV_mol_J} J/mol basis)")

    M_mix = Q_(0.0, "kg/mol")
    for sp, x in fuel_x.items():
        M_mix = M_mix + Q_(float(x), "") * molar_masses[sp].to("kg/mol")

    if M_mix.to("kg/mol").magnitude <= 0.0:
        raise ValueError("compute_LHV_HHV: invalid fuel mixture molar mass")

    LHV_mol = Q_(float(LHV_mol_J), "J/mol")

    LHV_kg = (LHV_mol / M_mix).to("kJ/kg")

    latent = (WaterProps.h_g(P_ref) - WaterProps.h_f(P_ref)).to("J/kg")
    h_fg_mol = (latent * molar_masses["H2O"].to("kg/mol")).to("J/mol")

    HHV_mol = (LHV_mol + Q_(float(n_H2O), "") * h_fg_mol).to("J/mol")
    HHV_kg = (HHV_mol / M_mix).to("kJ/kg")

    P_LHV = (LHV_kg.to("J/kg") * fuel.mass_flow).to("kW")
    P_HHV = (HHV_kg.to("J/kg") * fuel.mass_flow).to("kW")

    return HHV_kg, LHV_kg, P_HHV, P_LHV

def sensible_heat(stream: GasStream) -> Q_:
    s = stream
    h_sens = _gasprops.h_sensible(s.T, s.P, s.comp, Tref=T_ref).to("J/kg")
    return (s.mass_flow * h_sens).to("kW")

def total_input_heat(fuel, air) -> Q_:
    _, _, _, power_LHV = compute_LHV_HHV(fuel, air)
    fuel_sens = sensible_heat(fuel)
    air_sens  = sensible_heat(air)
    Q_in = (power_LHV.to("kW") + fuel_sens.to("kW") + air_sens.to("kW")).to("kW")
    return power_LHV, Q_in
