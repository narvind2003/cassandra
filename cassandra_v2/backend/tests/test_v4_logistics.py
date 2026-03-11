import pytest
from app.schema.vessel import Vessel, VesselClass
from app.engines.logistics import LogisticsEngine

def test_the_long_haul():
    # 1. Setup VLCC: 13 knots
    vlcc_class = VesselClass(
        name="VLCC",
        capacity=200000,
        speed=13.0,
        fuel_consumption_tonnes_per_day=50.0,
        daily_charter_rate=40000.0
    )
    
    # 2. Brazil to China
    brazil = {"lat": -25.5, "lng": -42.8}
    china = {"lat": 29.98, "lng": 121.82}
    
    distance = LogisticsEngine.haversine_distance(brazil, china)
    # Approx 10,000 - 11,000 nm
    assert distance > 9000
    
    vessel = Vessel(
        id="v1", 
        name="Long Hauler", 
        vessel_class=vlcc_class, 
        current_location=brazil,
        status="transit",
        destination_id="port_zhoushan",
        destination_location=china,
        distance_remaining=distance
    )
    
    # 3. Simulate Ticks
    days = 0
    while vessel.status == "transit" and days < 100:
        LogisticsEngine.tick_vessel(vessel)
        days += 1
        
    # Expected: ~35 days
    assert 30 < days < 45
    assert vessel.status == "unloading"
    assert vessel.current_location["lat"] == china["lat"]
    assert vessel.current_location["lng"] == china["lng"]
    print(f"\nLong Haul Completed in {days} days.")

def test_suez_blockage_rerouting():
    sea_lanes = {
        "waypoints": [
            {"id": "rotterdam", "location": {"lat": 51.9, "lng": 4.0}},
            {"id": "gibraltar", "location": {"lat": 35.9, "lng": -5.5}},
            {"id": "suez", "location": {"lat": 30.5, "lng": 32.2}},
            {"id": "cape", "location": {"lat": -34.3, "lng": 18.4}},
            {"id": "singapore", "location": {"lat": 1.2, "lng": 103.8}}
        ],
        "edges": [
            {"source": "rotterdam", "target": "gibraltar", "distance": 1300},
            {"source": "gibraltar", "target": "suez", "distance": 1900},
            {"source": "suez", "target": "singapore", "distance": 5000},
            {"source": "gibraltar", "target": "cape", "distance": 5000},
            {"source": "cape", "target": "singapore", "distance": 6000}
        ]
    }
    engine = LogisticsEngine(sea_lanes)
    
    # 1. Normal Path: Suez
    path_normal = engine.find_path("rotterdam", "singapore")
    assert "suez" in path_normal
    
    # 2. Blocked Path: Cape
    path_blocked = engine.find_path("rotterdam", "singapore", blocked_nodes=["suez"])
    assert "suez" not in path_blocked
    assert "cape" in path_blocked
    print("\nSuez Blockage Reroute Successful.")

