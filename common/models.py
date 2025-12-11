from dataclasses import dataclass
from typing import Dict, Any
from common.units import Q_

@dataclass
class GasStream:
    mass_flow: Q_
    T: Q_
    P: Q_
    comp: Dict[str, Q_]

@dataclass
class WaterStream:
    mass_flow: Q_
    h: Q_
    P: Q_

@dataclass
class HXStage:
    name: str
    kind: str
    spec: Dict[str, Any]

@dataclass
class Drum:
    Di: Q_
    L: Q_     