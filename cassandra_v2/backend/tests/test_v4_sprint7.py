import pytest
from app.schema.node import Node, Recipe, NodeSpec
from app.engines.physics import PhysicsEngine
from app.engines.finance import FinanceEngine

def test_demand_destruction():
    base_demand = 1000.0
    # Price = $100 (No change)
    d1 = FinanceEngine.calculate_demand(base_demand, 100.0)
    assert d1 == 1000.0
    
    # Price = $400 (4x price, demand should drop significantly)
    # With elasticity 0.5: 1000 / (4^0.5) = 1000 / 2 = 500
    d2 = FinanceEngine.calculate_demand(base_demand, 400.0, price_elasticity=0.5)
    assert d2 == 500.0
    print("\nDemand Destruction Logic Validated.")

def test_substitution_logic():
    # Setup node with 2 recipes: 1 preferred (Gas), 1 fallback (Coal)
    r1 = Recipe(name="Primary", inputs={"Natural Gas": 1.0}, outputs={"Power": 1.0})
    r2 = Recipe(name="Secondary", inputs={"Coal": 2.0}, outputs={"Power": 1.0})
    
    node = Node(
        id="power_plant",
        label="Dual-Fuel Plant",
        type="transformation",
        location={"lat": 0, "lng": 0},
        recipes=[r1, r2]
    )
    
    # Test 1: Only Coal available -> Should use r2
    from app.schema.cargo import Cargo
    from app.schema.commodity import CommodityGrade
    
    coal_cargo = Cargo(
        id="c1", 
        commodity=CommodityGrade(name="Coal", category="Energy", properties={}),
        quantity=10.0
    )
    
    outputs = PhysicsEngine.process(node, [coal_cargo])
    
    # Should produce 5 batches of Power (10/2)
    power_output = next(o for o in outputs if o.commodity.name == "Power")
    assert power_output.quantity == 5.0
    print("\nSubstitution (Fallback) Logic Validated.")
    
    # Test 2: Both available -> Should use preferred r1 (Gas)
    gas_cargo = Cargo(
        id="g1", 
        commodity=CommodityGrade(name="Natural Gas", category="Energy", properties={}),
        quantity=10.0
    )
    
    # Pass both
    outputs_dual = PhysicsEngine.process(node, [coal_cargo, gas_cargo])
    # Should produce 10 batches of Power from Gas (r1 is prioritized)
    power_dual = next(o for o in outputs_dual if o.commodity.name == "Power")
    assert power_dual.quantity == 10.0
    print("\nPriority Recipe Logic Validated.")

