from common.units import ureg, Q_
from common.models import GasStream
from scipy.optimize import root_scalar
from common.props import GasProps
import cantera as ct
from combustion.mass_mole import to_mole, molar_flow
from combustion.flue import from_fuel_and_air


def adiabatic_flame_T(air: GasStream, fuel: GasStream) -> GasStream:
    P_Pa   = air.P.to("Pa").magnitude
    T_air  = air.T.to("K").magnitude
    T_fuel = fuel.T.to("K").magnitude

    m_air  = air.mass_flow.to("kg/s").magnitude
    m_fuel = fuel.mass_flow.to("kg/s").magnitude
    m_tot  = m_air + m_fuel
    if m_tot <= 0.0:
        raise ValueError("adiabatic_flame_T: total mass flow must be > 0")

    X_air  = to_mole({k: v.to("").magnitude for k, v in (air.comp  or {}).items() if v.to("").magnitude > 0})
    X_fuel = to_mole({k: v.to("").magnitude for k, v in (fuel.comp or {}).items() if v.to("").magnitude > 0})

    gas_air  = ct.Solution("config/flue_cantera.yaml", "gas_mix")
    gas_fuel = ct.Solution("config/flue_cantera.yaml", "gas_mix")
    gas_mix  = ct.Solution("config/flue_cantera.yaml", "gas_mix")

    gas_air.TPX  = T_air,  P_Pa, X_air
    gas_fuel.TPX = T_fuel, P_Pa, X_fuel

    Hdot_react = m_air * gas_air.enthalpy_mass + m_fuel * gas_fuel.enthalpy_mass
    h_target   = Hdot_react / m_tot

    n_air  = molar_flow(air.comp,  air.mass_flow)
    n_fuel = molar_flow(fuel.comp, fuel.mass_flow)

    def _mol_rate(X, n_tot): return {k: n_tot * float(x) for k, x in X.items()}
    n_dot_sp = {}
    for d in (_mol_rate(X_air, n_air), _mol_rate(X_fuel, n_fuel)):
        for k, v in d.items():
            n_dot_sp[k] = n_dot_sp.get(k, 0.0) + v
    n_sum = sum(n_dot_sp.values())
    if n_sum <= 0.0:
        raise ValueError("adiabatic_flame_T: empty reactant composition")
    X_react = {k: v / n_sum for k, v in n_dot_sp.items()}

    gas_mix.TPX = 300.0, P_Pa, X_react
    gas_mix.HP  = h_target, P_Pa
    gas_mix.equilibrate("HP")

    Y_eq = gas_mix.Y
    comp_eq = {sp: Q_(float(Y_eq[i]), "") for i, sp in enumerate(gas_mix.species_names) if Y_eq[i] > 1e-15}

    return GasStream(
        mass_flow=Q_(m_tot, "kg/s"),
        T=Q_(gas_mix.T, "K"),
        P=air.P,
        comp=comp_eq,
    )

def adiabatic_flame_T_no_dissociation(air: GasStream, fuel: GasStream) -> GasStream:
    m_air  = air.mass_flow.to("kg/s").magnitude
    m_fuel = fuel.mass_flow.to("kg/s").magnitude
    m_tot  = m_air + m_fuel
    if m_tot <= 0.0:
        raise ValueError("adiabatic_flame_T_no_dissociation: total mass flow must be > 0")

    gasprops = GasProps()

    h_air  = gasprops.h(air.T,  air.P,  air.comp).to("J/kg").magnitude
    h_fuel = gasprops.h(fuel.T, fuel.P, fuel.comp).to("J/kg").magnitude

    Hdot_react = m_air * h_air + m_fuel * h_fuel
    h_target   = Hdot_react / m_tot

    mass_comp_burnt, m_dot_flue = from_fuel_and_air(fuel, air)
    comp_prod = {sp: Q_(float(y), "") for sp, y in mass_comp_burnt.items() if float(y) > 1e-15}

    def f(T_K: float) -> float:
        hP = gasprops.h(Q_(T_K, "K"), air.P, comp_prod).to("J/kg").magnitude
        return hP - h_target

    T_lo, T_hi = 250.0, 3500.0
    f_lo, f_hi = f(T_lo), f(T_hi)
    if f_lo * f_hi > 0.0:
        T_hi = 4500.0
        f_hi = f(T_hi)
        if f_lo * f_hi > 0.0:
            raise RuntimeError(
                "adiabatic_flame_T_no_dissociation: could not bracket root for Tad "
                f"(f({T_lo})={f_lo:.3e}, f({T_hi})={f_hi:.3e})"
            )

    sol = root_scalar(f, bracket=(T_lo, T_hi), method="brentq", xtol=1e-6, rtol=1e-8)
    if not sol.converged:
        raise RuntimeError("adiabatic_flame_T_no_dissociation: root solve did not converge")

    Tad = float(sol.root)

    return GasStream(
        mass_flow=m_dot_flue.to("kg/s"),
        T=Q_(Tad, "K"),
        P=air.P,
        comp=comp_prod,
    )
