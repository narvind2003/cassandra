import pytest
from app.schema.market import Trader
from app.schema.cargo import Cargo
from app.schema.commodity import CommodityGrade
from app.schema.compliance import ComplianceProfile
from app.engines.compliance import ComplianceEngine

def test_sanctions_blocking():
    # US Buyer
    buyer = Trader(id="us_buyer", name="Western Corp")
    buyer_profile = ComplianceProfile(entity_id="us_buyer", jurisdiction="US")
    
    # Sanctioned Entity (e.g., specific sanctioned entity)
    seller = Trader(id="sanctioned_entity", name="Sanctioned Co")
    seller_profile = ComplianceProfile(
        entity_id="sanctioned_entity", 
        jurisdiction="RU", 
        sanctioned_by=["US", "EU"]
    )
    
    cargo = Cargo(id="c1", commodity=CommodityGrade(name="Oil", category="Energy"), quantity=100)
    
    # Check Compliance
    result = ComplianceEngine.check_trade_compliance(buyer, seller, cargo, buyer_profile, seller_profile)
    
    assert result["allowed"] is False
    assert "Sanctioned" in result["reason"]

def test_sts_risk_flagging():
    # EU Buyer (Strict)
    buyer = Trader(id="eu_buyer", name="Euro Utility")
    buyer_profile = ComplianceProfile(entity_id="eu_buyer", jurisdiction="EU")
    
    # Neutral Seller
    seller = Trader(id="neutral_trader", name="Global Trading")
    seller_profile = ComplianceProfile(entity_id="neutral_trader", jurisdiction="SG")
    
    # Cargo with STS history (simulated by ID for MVP)
    grade = CommodityGrade(name="Diesel", category="Energy")
    risky_cargo = Cargo(id="sts_transfer_123", commodity=grade, quantity=1000)
    
    result = ComplianceEngine.check_trade_compliance(buyer, seller, risky_cargo, buyer_profile, seller_profile)
    
    assert result["allowed"] is False
    assert "STS Transfer detected" in result["reason"]

def test_allowed_trade():
    buyer = Trader(id="cn_buyer", name="Eastern Corp")
    buyer_profile = ComplianceProfile(entity_id="cn_buyer", jurisdiction="CN")
    
    seller = Trader(id="ru_seller", name="Siberian Oil")
    seller_profile = ComplianceProfile(entity_id="ru_seller", jurisdiction="RU", sanctioned_by=["US"])
    
    # CN does not sanction RU, so trade should flow
    cargo = Cargo(id="c2", commodity=CommodityGrade(name="Oil", category="Energy"), quantity=100)
    
    result = ComplianceEngine.check_trade_compliance(buyer, seller, cargo, buyer_profile, seller_profile)
    
    assert result["allowed"] is True
