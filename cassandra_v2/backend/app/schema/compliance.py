from pydantic import BaseModel
from typing import List, Optional

class Sanction(BaseModel):
    target_id: str # The entity ID being sanctioned (e.g., "russia", "company_x")
    sanctioning_body: str # e.g., "OFAC", "EU"
    description: str

class ComplianceProfile(BaseModel):
    entity_id: str
    jurisdiction: str # e.g., "US", "CN", "EU"
    sanctioned_by: List[str] = [] # List of jurisdictions sanctioning this entity
    internal_watch_list: List[str] = [] # Entities this actor refuses to trade with
    
class CertificateOfOrigin(BaseModel):
    origin_node_id: str
    country_of_origin: str
    is_blended: bool = False
    trace_log: List[str] = [] # History of vessel transfers (STS)
