import pytest
from app.schema.vessel import Vessel, VesselClass
from app.engines.logistics import LogisticsEngine

def test_waypoint_following():
    # Setup
    vlcc_class = VesselClass(
        name="VLCC",
        capacity=200000,
        speed=10.0,
        fuel_consumption_tonnes_per_day=50.0,
        daily_charter_rate=40000.0
    )
    
    start = {"lat": 0.0, "lng": 0.0}
    wp1 = {"lat": 1.0, "lng": 0.0} # 60nm away
    destination = {"lat": 1.0, "lng": 1.0} # another ~60nm away
    
    vessel = Vessel(
        id="v1", 
        name="Path Follower", 
        vessel_class=vlcc_class, 
        current_location=start,
        status="transit",
        destination_id="port_x",
        destination_location=destination,
        route_path=[wp1],
        distance_remaining=120.0 # Approx
    )
    
    # Tick 1: 3 hours at 10 knots = 30nm
    LogisticsEngine.tick_vessel(vessel, hours_per_tick=3.0)
    
    # Should be halfway to wp1
    assert 0.4 < vessel.current_location["lat"] < 0.6
    assert vessel.current_location["lng"] == 0.0
    assert len(vessel.route_path) == 1
    
    # Tick 2: another 3.1 hours = 31nm (total 61nm)
    LogisticsEngine.tick_vessel(vessel, hours_per_tick=3.1)
    
    # Should have reached wp1 and popped it
    assert vessel.current_location["lat"] == 1.0
    assert vessel.current_location["lng"] == 0.0
    assert len(vessel.route_path) == 0
    
    # Tick 3: another 3 hours = 30nm
    LogisticsEngine.tick_vessel(vessel, hours_per_tick=3.0)
    
    # Should be moving toward destination now
    assert vessel.current_location["lat"] == 1.0
    assert 0.4 < vessel.current_location["lng"] < 0.6
    
    # Tick 4: 10 hours = 100nm
    LogisticsEngine.tick_vessel(vessel, hours_per_tick=10.0)
    
    # Should have arrived
    assert vessel.status == "unloading"
    assert vessel.current_location == destination
    print("\nWaypoint Following Successful.")

def test_path_distance_calculation():
    sea_lanes = {
        "waypoints": [
            {"id": "A", "location": {"lat": 0, "lng": 0}},
            {"id": "B", "location": {"lat": 0, "lng": 1}},
            {"id": "C", "location": {"lat": 0, "lng": 2}}
        ],
        "edges": [
            {"source": "A", "target": "B", "distance": 60},
            {"source": "B", "target": "C", "distance": 60}
        ]
    }
    engine = LogisticsEngine(sea_lanes)
    dist = engine.calculate_path_distance(["A", "B", "C"])
    assert dist == 120.0
