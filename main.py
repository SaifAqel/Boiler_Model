import logging
from common.logging_utils import setup_logging
from common.units import Q_
from common.boiler_loop import run_boiler_case

def run_default_case() -> None:
    run_boiler_case(run_id="default_case")

def run_excess_air_sensitivity() -> None:
    ea_values = [1.00, 1.05, 1.10, 1.15, 1.20, 1.30]

    for ea in ea_values:
        logging.getLogger(__name__).info(f"Running case with excess_air_ratio={ea}")

        run_boiler_case(
            operation_overrides={"excess_air_ratio": Q_(ea, "")},
            tol_m=Q_(1e-3, "kg/s"),
            max_iter=20,
            write_csv=True,
            run_id=f"excess_air_{ea}",
        )

def run_water_pressure_sensitivity() -> None:
    Pbar_values = [4.0, 10.0, 16.0]

    for P_bar in Pbar_values:
        logging.getLogger(__name__).info(f"Running case with drum pressure={P_bar} bar")

        run_boiler_case(
            operation_overrides={"drum_pressure": Q_(P_bar, "bar")},
            tol_m=Q_(1e-3, "kg/s"),
            max_iter=20,
            write_csv=True,
            run_id=f"drum_pressure_{P_bar}bar",
        )


def run_fuel_flow_sensitivity() -> None:
    mdot_values = [0.20, 0.10, 0.075, 0.050, 0.025]  # kg/s

    for mdot in mdot_values:
        logging.getLogger(__name__).info(f"Running case with fuel mass_flow={mdot} kg/s")

        run_boiler_case(
            fuel_overrides={"mass_flow": Q_(mdot, "kg/s")},
            tol_m=Q_(1e-3, "kg/s"),
            max_iter=20,
            write_csv=True,
            run_id=f"fuel_flow_{mdot}kgs",
        )

def run_fouling_sensitivity() -> None:
    factors = [0.5, 1.0, 2.0]

    for f in factors:
        logging.getLogger(__name__).info(f"Running case with fouling_factor={f}")

        run_boiler_case(
            fouling_factor=f,
            tol_m=Q_(1e-3, "kg/s"),
            max_iter=20,
            write_csv=True,
            run_id=f"fouling_{f}",
        )

def main() -> None:
    setup_logging("INFO")



    run_default_case()
    run_excess_air_sensitivity()
    # run_water_pressure_sensitivity()
    # run_fuel_flow_sensitivity() 
    # run_fouling_sensitivity()



if __name__ == "__main__":
    main()
