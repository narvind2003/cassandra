import pytest
from app.schema.commodity import CommodityGrade
from app.schema.cargo import Cargo
from app.schema.node import Node, NodeSpec, Recipe
from app.engines.physics import PhysicsEngine

def test_copper_smelter_rejection():
    # 1. Define Smelter with Arsenic constraint
    smelter_spec = NodeSpec(
        allowed_inputs=["Copper Concentrate"],
        constraints={"arsenic": {"max": 0.1}}
    )
    smelter = Node(
        id="chile_smelter_01",
        label="Antofagasta Smelter",
        type="transformation",
        subtype="smelter",
        location={"lat": -23.65, "lon": -70.40},
        specs=smelter_spec
    )

    # 2. High-Arsenic Cargo (Toxic)
    toxic_grade = CommodityGrade(
        name="Copper Concentrate High Arsenic",
        category="Copper Concentrate",
        properties={"arsenic": 0.5, "copper": 0.28}
    )
    toxic_cargo = Cargo(id="cargo_toxic", commodity=toxic_grade, quantity=100)

    # 3. Clean Cargo
    clean_grade = CommodityGrade(
        name="Copper Concentrate Clean",
        category="Copper Concentrate",
        properties={"arsenic": 0.02, "copper": 0.30}
    )
    clean_cargo = Cargo(id="cargo_clean", commodity=clean_grade, quantity=100)

    # 4. Validation Tests
    # Should reject toxic cargo
    assert PhysicsEngine.validate_constraints(smelter, toxic_cargo) is False
    
    # Should accept clean cargo
    assert PhysicsEngine.validate_constraints(smelter, clean_cargo) is True

def test_blending_for_compliance():
    # Define Smelter constraint: arsenic max 0.1
    smelter_spec = NodeSpec(constraints={"arsenic": {"max": 0.1}})
    smelter = Node(id="s1", label="Smelter", type="t", location={"lat":0,"lon":0}, specs=smelter_spec)

    # Cargo A: 100 units at 0.5 arsenic (Toxic)
    grade_a = CommodityGrade(name="A", category="C", properties={"arsenic": 0.5})
    cargo_a = Cargo(id="a", commodity=grade_a, quantity=100)

    # Cargo B: 400 units at 0.02 arsenic (Clean)
    grade_b = CommodityGrade(name="B", category="C", properties={"arsenic": 0.02})
    cargo_b = Cargo(id="b", commodity=grade_b, quantity=400)

    # Blend them: (100*0.5 + 400*0.02) / 500 = (50 + 8) / 500 = 58 / 500 = 0.116
    # 0.116 is still > 0.1, should be rejected
    blended_cargo_1 = PhysicsEngine.blend([cargo_a, cargo_b], "blend_1")
    assert blended_cargo_1.commodity.properties["arsenic"] == 0.116
    assert PhysicsEngine.validate_constraints(smelter, blended_cargo_1) is False

    # Cargo C: 900 units at 0.02 arsenic (Clean)
    cargo_c = Cargo(id="c", commodity=grade_b, quantity=900)
    # Blend A and C: (100*0.5 + 900*0.02) / 1000 = (50 + 18) / 1000 = 68 / 1000 = 0.068
    # 0.068 < 0.1, should be accepted
    blended_cargo_2 = PhysicsEngine.blend([cargo_a, cargo_c], "blend_2")
    assert blended_cargo_2.commodity.properties["arsenic"] == 0.068
    assert PhysicsEngine.validate_constraints(smelter, blended_cargo_2) is True

def test_recipe_transformation():
    # 1. Define a Smelter Recipe: 2.0 Copper Concentrate -> 1.0 Copper Cathode
    recipe = Recipe(
        name="Smelting",
        inputs={"Copper Concentrate": 2.0},
        outputs={"Copper Cathode": 1.0}
    )
    smelter = Node(
        id="s1", label="Smelter", type="transformation", 
        location={"lat":0,"lon":0}, recipes=[recipe]
    )

    # 2. Input Cargo: 500 units of Copper Concentrate
    grade = CommodityGrade(name="Copper Concentrate", category="Concentrate")
    cargo = Cargo(id="c1", commodity=grade, quantity=500)

    # 3. Process
    outputs = PhysicsEngine.process(smelter, [cargo])

    # 4. Verify: 500 / 2.0 = 250 units of Copper Cathode
    assert len(outputs) == 1
    assert outputs[0].commodity.name == "Copper Cathode"
    assert outputs[0].quantity == 250.0
