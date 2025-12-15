from __future__ import annotations
from typing import Tuple, List, Dict, Any
import yaml
from common.units import Q_
from common.models import HXStage, GasStream, WaterStream, Drum

def _q(node: Any) -> Q_:
    if isinstance(node, dict) and "value" in node and "unit" in node:
        return Q_(node["value"], str(node["unit"]))
    raise ValueError(f"Invalid quantity format: {node!r}")

def _get(d: Dict[str, Any] | None, key: str, default=None):
    return d.get(key, default) if isinstance(d, dict) else default

def _wall_to_spec(wall: Dict[str, Any] | None, spec: Dict[str, Q_]):
    if not wall:
        return
    if _get(wall, "thickness"):    spec["wall_t"] = _q(_get(wall, "thickness"))
    if _get(wall, "conductivity"): spec["wall_k"] = _q(_get(wall, "conductivity"))

    surf_in = _get(_get(wall, "surfaces"), "inner") or {}
    if _get(surf_in, "roughness"):            spec["roughness_in"] = _q(_get(surf_in, "roughness"))
    if _get(surf_in, "emissivity"):           spec["eps_in"] = _q(_get(surf_in, "emissivity"))
    if _get(surf_in, "fouling_thickness"):    spec["foul_t_in"] = _q(_get(surf_in, "fouling_thickness"))
    if _get(surf_in, "fouling_conductivity"): spec["foul_k_in"] = _q(_get(surf_in, "fouling_conductivity"))

    surf_out = _get(_get(wall, "surfaces"), "outer") or {}
    if _get(surf_out, "roughness"):            spec["roughness_out"] = _q(_get(surf_out, "roughness"))
    if _get(surf_out, "emissivity"):           spec["eps_out"] = _q(_get(surf_out, "emissivity"))
    if _get(surf_out, "fouling_thickness"):    spec["foul_t_out"] = _q(_get(surf_out, "fouling_thickness"))
    if _get(surf_out, "fouling_conductivity"): spec["foul_k_out"] = _q(_get(surf_out, "fouling_conductivity"))

def _map_K(node: Dict[str, Any], spec: Dict[str, Q_]):
    K_node = _get(node, "K") or {}
    if not isinstance(K_node, dict):
        return

    mapping = {
        "hot_inlet": "K_hot_inlet",
        "hot_outlet": "K_hot_outlet",
        "hot_bend": "K_hot_bend",
        "cold_inlet": "K_cold_inlet",
        "cold_outlet": "K_cold_outlet",
        "cold_bend": "K_cold_bend",
    }

    for yaml_key, spec_key in mapping.items():
        v = _get(K_node, yaml_key)
        if v is not None:
            spec[spec_key] = Q_(float(v), "dimensionless")

def load_air(path: str) -> Dict[str, Any]:
    doc = yaml.safe_load(open(path, "r", encoding="utf-8"))
    comp = {k: _q(v) for k, v in (doc.get("composition") or {}).items()}
    return GasStream(
        mass_flow=Q_(0, "kg/s"),
        T=_q(doc["T"]),
        P=_q(doc["P"]),
        comp=comp
    )

def load_fuel(path: str) -> GasStream:
    doc = yaml.safe_load(open(path, "r", encoding="utf-8"))
    comp = {k: _q(v) for k, v in (doc.get("composition") or {}).items()}
    return GasStream(
        mass_flow=_q(doc["mass_flow"]),
        T=_q(doc["T"]),
        P=_q(doc["P"]),
        comp=comp
    )

def load_drum(path: str) -> Drum:
    doc = yaml.safe_load(open(path, "r", encoding="utf-8"))
    return Drum(Di=_q(doc["inner_diameter"]).to("m"),
                L=_q(doc["length"]).to("m"))

def load_stages(path: str) -> List[HXStage]:
    sdoc = yaml.safe_load(open(path, "r", encoding="utf-8"))
    stages: List[HXStage] = []

    for name, node in sdoc.items():

        spec: Dict[str, Q_] = {
            "inner_diameter": _q(node["inner_diameter"]),
        }
        if "inner_length" in node:          spec["inner_length"]     = _q(node["inner_length"]) 
        if "pool_boiling" in node:         spec["pool_boiling"]     = bool(node["pool_boiling"])
        if "curvature_radius" in node:     spec["curvature_radius"] = _q(node["curvature_radius"])
        if "tubes_number" in node:         spec["tubes_number"]     = _q(node["tubes_number"])
        if "ST" in node:                   spec["ST"]               = _q(node["ST"])
        if "SL" in node:                   spec["SL"]               = _q(node["SL"])
        if "arrangement" in node:          spec["arrangement"]      = str(node["arrangement"])
        if "N_rows" in node:               spec["N_rows"]           = _q(node["N_rows"])
        if "baffle_spacing" in node:       spec["baffle_spacing"]   = _q(node["baffle_spacing"])
        if "shell_inner_diameter" in node: spec["shell_inner_diameter"] = _q(node["shell_inner_diameter"])
        if "baffle_cut" in node:           spec["baffle_cut"]       = _q(node["baffle_cut"])
        if "bundle_clearance" in node:     spec["bundle_clearance"] = _q(node["bundle_clearance"])
        if "n_tubes" in node:              spec["n_tubes"]      = _q(node["n_tubes"])
        if "n_circuits" in node:           spec["n_circuits"]   = _q(node["n_circuits"])
        if "tube_length" in node:          spec["tube_length"]  = _q(node["tube_length"])


        _wall_to_spec(_get(node, "wall"), spec)
        _map_K(node, spec)

        stages.append(HXStage(name=name, kind=str(node["kind"]), spec=spec))

    return stages

def load_operation(path: str) -> Dict[str, Q_]:
    doc = yaml.safe_load(open(path, "r", encoding="utf-8"))

    out: Dict[str, Q_] = {
        "excess_air_ratio": _q(doc["excess_air_ratio"]),
    }

    if "drum_pressure" in doc:
        out["drum_pressure"] = _q(doc["drum_pressure"])

    return out

def load_water_stream(path: str) -> WaterStream:
    doc = yaml.safe_load(open(path, "r", encoding="utf-8"))
    h = _q(doc["enthalpy"])

    P_node = doc.get("pressure", None)
    if P_node is not None:
        P = _q(P_node)
    else:
        P = Q_(1.0, "megapascal")

    return WaterStream(
        mass_flow=Q_(0, "kg/s"),
        h=h,
        P=P,
    )

def load_all(
    stages_path: str,
    water_path: str,
    drum_path: str,
    air_path: str,
    fuel_path: str,
    operation_path: str,
) -> Tuple[List[HXStage], GasStream, GasStream, WaterStream, Drum, Dict[str, Q_]]:
    stages = load_stages(stages_path) if stages_path else None
    water = load_water_stream(water_path) if water_path else None
    drum  = load_drum(drum_path) if drum_path else None
    air  = load_air(air_path) if air_path else None
    fuel = load_fuel(fuel_path) if fuel_path else None
    operation = load_operation(operation_path) if operation_path else None
    return stages, air, fuel, water, drum, operation
