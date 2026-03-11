from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from .cargo import Cargo

class VesselClass(BaseModel):
    name: str # e.g., "VLCC", "Aframax", "Suezmax"
    type: str # "tanker", "bulker", "container", "gas"
    capacity: float # tonnes or barrels
    speed: float # knots
    fuel_consumption_tonnes_per_day: float
    daily_charter_rate: float # USD per day
    max_draft: float = 20.0 # meters (Suez is ~20m)
    beam: float = 50.0 # meters (Panamax is ~32m)

class Vessel(BaseModel):
    id: str
    name: str
    vessel_class: VesselClass
    current_location: Dict[str, float] # {"lat": 0.0, "lng": 0.0}
    cargo: Optional[Cargo] = None
    status: str = "idle" # idle, loading, transit, unloading, queued, floating_storage
    is_floating_storage: bool = False
    storage_start_tick: Optional[int] = None
    
    # v4.0 Deterministic Fields
    destination_id: Optional[str] = None
    destination_location: Optional[Dict[str, float]] = None
    distance_remaining: float = 0.0 # nautical miles
    speed_knots: Optional[float] = None # Override for slow-steaming
    target_commodity: Optional[str] = None # Logic helper
    route_path: List[Dict[str, float]] = Field(default_factory=list) # Waypoints (Coords)
    route_path_ids: List[str] = Field(default_factory=list) # Waypoints (IDs) for rerouting checks
    
    @property
    def current_speed(self) -> float:
        return self.speed_knots if self.speed_knots is not None else self.vessel_class.speed

    @property
    def is_full(self) -> bool:
        if not self.cargo:
            return False
        return self.cargo.quantity >= self.vessel_class.capacity
