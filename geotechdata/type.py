from dataclasses import dataclass, field
from typing import Optional, Tuple
from .borehole import BoreholeData
from .labtest import LabTestData

@dataclass
class Point:
    id: str
    coordinates: Tuple[float, float]
    description: str = ""
    borehole_data: Optional['BoreholeData'] = field(default=None)
    lab_test_data: Optional['LabTestData'] = field(default=None)