from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class Property(BaseModel):
    name: str
    value: float
    unit: str

class CommodityGrade(BaseModel):
    name: str  # e.g., "Brent Crude", "Copper Concentrate High Arsenic"
    category: str # e.g., "Energy", "Metal"
    properties: Dict[str, float] = Field(default_factory=dict) # e.g., {"sulfur": 0.5, "density": 0.85}
    
    def get_property(self, name: str) -> float:
        return self.properties.get(name, 0.0)
