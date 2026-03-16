from dataclasses import dataclass

@dataclass
class DetectionObject:
    id: int
    class_name: str
    confidence: float
    bbox: tuple[int, int, int, int]
    polygon: list[tuple[int, int]]

@dataclass
class Space(DetectionObject):
    pass

@dataclass 
class Sign(DetectionObject):
    pass

@dataclass
class Door(DetectionObject):
    center: tuple[int, int]
    orientation_deg: float

    space_id_a: int | None
    space_id_b: int | None

    is_external: bool = False
    is_emergency_exit: bool = False