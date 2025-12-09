import logging
from common.logging_utils import setup_logging
from common.units import Q_
from boiler_loop import run_boiler_case

def run_default_case() -> None:
    run_boiler_case(run_id="default_case")

def run_excess_air_sensitivity() -> None:
    ea_values = [1.0, 1.1, 1.2, 1.3]

    for ea in ea_values:
        logging.getLogger(__name__).info(f"Running case with excess_air_ratio={ea}")

        run_boiler_case(
            operation_overrides={"excess_air_ratio": Q_(ea, "")},
            eta_guess=Q_(0.90, ""),
            tol_m=Q_(1e-3, "kg/s"),
            max_iter=20,
            write_csv=True,
            run_id=f"excess_air_{ea}",
        )

def run_water_pressure_sensitivity() -> None:
    """
    Sensitivity analysis on feedwater pressure.
    Pressures in bar (absolute): 4, 10, 16.
    Everything else remains from the default YAMLs.
    """
    Pbar_values = [4.0, 10.0, 16.0]

    for P_bar in Pbar_values:
        logging.getLogger(__name__).info(f"Running case with water pressure={P_bar} bar")

        run_boiler_case(
            water_overrides={"P": Q_(P_bar, "bar")},
            eta_guess=Q_(0.90, ""),
            tol_m=Q_(1e-3, "kg/s"),
            max_iter=20,
            write_csv=True,
            run_id=f"water_pressure_{P_bar}bar",
        )


def run_fuel_flow_sensitivity() -> None:
    """
    Sensitivity analysis on fuel mass flow rate.
    Uses 0.1, 0.075, 0.05, 0.025 kg/s.
    Everything else remains from the default YAMLs.
    """
    mdot_values = [0.10, 0.075, 0.050, 0.025]  # kg/s

    for mdot in mdot_values:
        logging.getLogger(__name__).info(f"Running case with fuel mass_flow={mdot} kg/s")

        run_boiler_case(
            fuel_overrides={"mass_flow": Q_(mdot, "kg/s")},
            eta_guess=Q_(0.90, ""),
            tol_m=Q_(1e-3, "kg/s"),
            max_iter=20,
            write_csv=True,
            run_id=f"fuel_flow_{mdot}kgs",
        )




def main() -> None:
    setup_logging("INFO")


    
    run_default_case()
    # run_excess_air_sensitivity()
    # run_water_pressure_sensitivity()
    # run_fuel_flow_sensitivity()



if __name__ == "__main__":
    main()
