from pydantic import BaseModel
from typing import List, Dict, Optional

class Injection(BaseModel):
    target_id: str
    type: str # "blockage", "strike", "embargo"
    severity: float = 1.0

class Scenario(BaseModel):
    id: str
    type: str # "blockage", "strike", "tariff", "embargo"
    target_id: str # Node ID or Waypoint ID
    commodity: Optional[str] = None # For embargo/tariff
    start_tick: int
    end_tick: int
    severity: float = 1.0 # 1.0 = fully blocked / 100% strike

class ScenarioEngine:
    def __init__(self):
        self.active_scenarios: List[Scenario] = []

    def inject(self, scenario: Scenario):
        self.active_scenarios.append(scenario)

    def get_blocked_nodes(self, current_tick: int) -> List[str]:
        """Returns IDs of nodes/waypoints currently under blockage."""
        return [
            s.target_id for s in self.active_scenarios 
            if s.start_tick <= current_tick <= s.end_tick and s.type == "blockage"
        ]

    def get_blockage_severity(self, node_id: str, current_tick: int) -> float:
        """Returns the max blockage severity for a node at a given tick."""
        severities = [
            s.severity for s in self.active_scenarios
            if s.start_tick <= current_tick <= s.end_tick
            and s.type == "blockage"
            and s.target_id == node_id
        ]
        return max(severities) if severities else 0.0

    def is_embargoed(self, node_id: str, commodity: str, current_tick: int) -> bool:
        """Checks if a commodity is under embargo at a specific node."""
        for s in self.active_scenarios:
            if s.start_tick <= current_tick <= s.end_tick and s.type == "embargo":
                if s.target_id == node_id and (s.commodity is None or s.commodity == commodity):
                    return True
        return False

    def get_capacity_factor(self, node_id: str, current_tick: int) -> float:
        """Returns current operational capacity (0.0 to 1.0)."""
        factor = 1.0
        for s in self.active_scenarios:
            if s.start_tick <= current_tick <= s.end_tick and s.target_id == node_id and s.type == "strike":
                factor *= (1.0 - s.severity)
        return max(0.0, factor)
