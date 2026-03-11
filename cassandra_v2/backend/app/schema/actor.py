from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class ActorType(str, Enum):
    TRADER = "trader"         # Vitol, Glencore
    LOGISTICS = "logistics"   # Maersk, DHL
    PRODUCER = "producer"     # Rio Tinto, Aramco
    CONSUMER = "consumer"     # Tesla, Nestle
    STATE = "state"           # Government bodies
    FINANCIAL = "financial"   # Banks, Hedge Funds

class Actor(BaseModel):
    id: str
    name: str
    type: ActorType
    hq_country: str
    description: Optional[str] = None
    commodities: List[str] = [] # List of commodities they trade/produce
    risk_appetite: str = "medium" # low, medium, high
    assets: List[str] = [] # List of Node IDs they own (populated at runtime or loaded)
    
    # Financial/Geopolitical attributes
    market_cap: float = 0.0 # Billions USD
    compliance_score: float = 1.0 # 0.0 (Sanctioned) to 1.0 (Clean)
    
    attributes: Dict[str, Any] = Field(default_factory=dict)
