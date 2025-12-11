from common.units import ureg, Q_
from common.models import GasStream
from scipy.optimize import root_scalar
from common.props import GasProps
import cantera as ct
from combustion.mass_mole import to_mole, molar_flow


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
