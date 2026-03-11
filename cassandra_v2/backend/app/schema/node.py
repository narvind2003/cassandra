from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from .cargo import Cargo

class Recipe(BaseModel):
    name: str
    inputs: Dict[str, float] # {"Bauxite": 2.0} ratio
    outputs: Dict[str, float] # {"Alumina": 1.0} ratio
    energy_cost: float = 0.0
    processing_time: int = 1 # Days

class NodeSpec(BaseModel):
    max_inventory: float = 10000.0
    processing_capacity: float = 1000.0 # Units per day
    production_rate: float = 1000.0 # Units generated per day (for resources)
    berth_capacity: int = 10 # Max ships that can unload/load per day (v6.1 Tuning)
    storage_cost_per_unit_day: float = 0.1 # Cost to hold 1 unit for 1 day
    is_benchmark_hub: bool = False # e.g. Cushing, Rotterdam, Henry Hub
    allowed_inputs: List[str] = [] # List of allowed commodity categories or names
    constraints: Dict[str, Dict[str, float]] = {} 

class Node(BaseModel):
    id: str
    label: str
    type: str # resource, transformation, logistic, retail
    subtype: Optional[str] = None 
    location: Dict[str, float]
    
    # Ownership & Governance (v7.0)
    owner_id: Optional[str] = None
    operator_id: Optional[str] = None
    
    # Geopolitical context (v7.0 Sprint 3)
    jurisdiction: str = "International" # ISO Country or "High Seas"
    risk_level: float = 0.0 # 0.0 to 1.0 (Low to High Risk)
    is_sanctioned: bool = False
    conflict_zone: bool = False
    
    # Physics State
    inventory: Dict[str, float] = Field(default_factory=dict)
    specs: NodeSpec = Field(default_factory=NodeSpec)
    recipes: List[Recipe] = []
    
    # Legacy fields
    tension_score: int = 0
    state: str = "baseline"
    revenue_per_day: float = 0.0
    base_demand: float = 0.0
    commodity: str = "Unknown"
    category: str = "Unknown"

class Edge(BaseModel):
    source_id: str
    target_id: str
    commodity: str = "Unknown"
    
    # Logistics
    carrier_id: Optional[str] = None
    infrastructure_id: Optional[str] = None # Link to Infrastructure (Pipe/Rail/Canal)
    transport_mode: str = "sea"
    distance_km: float = 0.0
    transit_time_days: int = 1
    cost_per_ton: float = 0.0
    
    # Geopolitical / Risk (v7.0 Sprint 3)
    risk_level: float = 0.0
    is_secure_route: bool = True
    active_threats: List[str] = [] # ["piracy", "war_zone", "storm"]
    
    # Status
    status: str = "active"
    flow_volume: float = 0.0
