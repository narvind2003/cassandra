from pydantic import BaseModel, Field
from typing import Optional
from .commodity import CommodityGrade

class Cargo(BaseModel):
    id: str
    commodity: CommodityGrade
    quantity: float # Quantity in standard units (tonnes, barrels)
    owner_id: Optional[str] = None # For future Financial Engine
    value_per_unit: float = 0.0 # Snapshot of market value
    
    @property
    def total_value(self) -> float:
        return self.quantity * self.value_per_unit
