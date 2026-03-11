from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class InfrastructureType(str, Enum):
    PIPELINE = "pipeline"
    RAIL_LINE = "rail_line"
    CANAL = "canal"
    STRAIT = "strait"
    SEA_LANE = "sea_lane"
    HIGHWAY = "highway"

class Infrastructure(BaseModel):
    id: str
    name: str
    type: InfrastructureType
    capacity_bpd: Optional[float] = None # Barrels per day (for pipes)
    capacity_tpy: Optional[float] = None # Tonnes per year (for rail)
    max_draft: Optional[float] = None # meters (for canals/straits)
    max_beam: Optional[float] = None # meters (for canals)
    length_km: float = 0.0
    start_location: Optional[Dict[str, float]] = None # {lat, lng}
    end_location: Optional[Dict[str, float]] = None # {lat, lng}
    waypoints: List[Dict[str, float]] = [] # For drawing the line
    owner_id: Optional[str] = None # e.g. "actor_transneft"
    status: str = "active" # active, maintenance, attacked, closed
    description: str = ""
