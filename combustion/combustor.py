from combustion.adiabatic_flame_temperature import adiabatic_flame_T
from combustion.heat import total_input_heat, compute_LHV_HHV
from combustion.flue import air_flow_rates, from_fuel_and_air
from common.results import CombustionResult
from common.models import GasStream
from common.units import Q_

class Combustor:
    def __init__(self, air: GasStream, fuel: GasStream, excess_air_ratio: Q_):
        self.air = air
        self.fuel = fuel
        self.excess_air_ratio = excess_air_ratio

    def run(self) -> CombustionResult:
        air = self.air
        fuel = self.fuel

        air.mass_flow = air_flow_rates(air, fuel, self.excess_air_ratio)

        power_LHV, Q_in = total_input_heat(fuel, air)
        HHV_mass, LHV_mass, P_HHV, P_LHV = compute_LHV_HHV(fuel, air)

        flue_ad = adiabatic_flame_T(air, fuel)
        T_ad = flue_ad.T

        mass_comp_burnt, m_dot_flue = from_fuel_and_air(fuel, air)

        flue_boiler = GasStream(
            mass_flow = Q_(m_dot_flue, "kg/s"),
            T         = T_ad,
            P         = air.P,
            comp      = {sp: Q_(y, "") for sp, y in mass_comp_burnt.items()},
        )

        return CombustionResult(
            LHV            = power_LHV,
            Q_in           = Q_in,
            T_ad           = T_ad,
            flue           = flue_boiler,
            flue_ad        = flue_ad,
            fuel_LHV_mass  = LHV_mass,
            fuel_P_LHV     = P_LHV,
            fuel_mass_flow = fuel.mass_flow,
            excess_air_ratio=self.excess_air_ratio,
            air_mass_flow  = air.mass_flow,
        )

