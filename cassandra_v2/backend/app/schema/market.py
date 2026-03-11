from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .cargo import Cargo

class Trader(BaseModel):
    id: str
    name: str
    cash: float = 0.0
    credit_limit: float = 0.0
    collateral_value: float = 0.0 # Value of non-cash assets used for margin
    inventory: List[Cargo] = Field(default_factory=list)
    margin_requirement: float = 0.0 # Current margin call total
    is_bankrupt: bool = False

class PricePoint(BaseModel):
    commodity_name: str
    price: float
    timestamp: int # Simulation tick
    volatility: float = 0.05
