from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Cassandra"
    VERSION: str = "7.0.0"
    DESCRIPTION: str = "Global Supply Chain Digital Twin - Physics Engine Upgrade"
    
    # Physics Constants
    DEFAULT_EFFICIENCY: float = 1.0
    DEFAULT_STORAGE_COST: float = 0.01  # Cost per unit per day

    # Systemic Risk (Hybrid Model)
    SYSTEMIC_RISK_UNMET_WEIGHT: float = 1.0
    SYSTEMIC_RISK_REVENUE_WEIGHT: float = 1.0
    SYSTEMIC_RISK_CHOKE_PENALTY: float = 50_000_000.0  # Fallback per blocked choke point per day
    SYSTEMIC_RISK_CHOKE_WEIGHTS: dict = {
        "choke_suez": 5.0,
        "choke_hormuz": 5.0,
        "choke_malacca": 4.0,
        "choke_panama": 3.0,
    }
    # Daily throughput impacts by choke (used when blocked). Values are in physical units.
    # These are policy-level defaults and can be tuned as new data arrives.
    SYSTEMIC_RISK_CHOKE_IMPACTS: dict = {
        # Approx. 20.9 million barrels per day through Hormuz in recent years.
        "choke_hormuz": {"oil_bpd": 20_900_000},
    }
    # Real-world flow fraction (0.0 = fully blocked, 1.0 = normal flow).
    # Set to reflect current conditions if desired.
    SYSTEMIC_RISK_CHOKE_FLOW_FRACTION: dict = {
        # Current flow fraction (e.g., 0.2 means ~20% of normal traffic still transiting).
        "choke_hormuz": 0.20,
    }
    # Macro multiplier to convert commodity value at risk into systemic economic impact.
    SYSTEMIC_RISK_CHOKE_MACRO_MULTIPLIER: float = 3.0
    
    class Config:
        case_sensitive = True

settings = Settings()
