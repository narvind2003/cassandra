import pytest
from app.schema.vessel import Vessel, VesselClass
from app.schema.cargo import Cargo
from app.schema.commodity import CommodityGrade
from app.engines.logistics import LogisticsEngine

def test_distance_calculation():
    # London to New York (approx)
    london = {"lat": 51.5074, "lon": -0.1278}
    new_york = {"lat": 40.7128, "lon": -74.0060}
    
    dist = LogisticsEngine.haversine_distance(london, new_york)
    # Approx 3000 nautical miles
    assert 2900 < dist < 3100

def test_vessel_cost_efficiency():
    # Setup Vessel Classes
    vlcc_class = VesselClass(
        name="VLCC",
        capacity=300000,
        speed=13.0,
        fuel_consumption_tonnes_per_day=60.0,
        daily_charter_rate=50000.0
    )
    
    aframax_class = VesselClass(
        name="Aframax",
        capacity=100000,
        speed=14.0,
        fuel_consumption_tonnes_per_day=40.0,
        daily_charter_rate=30000.0
    )
    
    v_vlcc = Vessel(id="v1", name="Giant Tanker", vessel_class=vlcc_class, current_location={"lat":0,"lon":0})
    v_aframax = Vessel(id="v2", name="Small Tanker", vessel_class=aframax_class, current_location={"lat":0,"lon":0})
    
    dist = 5000.0 # Nautical miles
    fuel_price = 600.0 # USD/tonne
    
    vlcc_data = LogisticsEngine.calculate_route_cost(v_vlcc, dist, fuel_price)
    aframax_data = LogisticsEngine.calculate_route_cost(v_aframax, dist, fuel_price)
    
    vlcc_cost_per_tonne = vlcc_data["total_cost"] / vlcc_class.capacity
    aframax_cost_per_tonne = aframax_data["total_cost"] / aframax_class.capacity
    
    # VLCC should be more efficient (Economy of Scale)
    assert vlcc_cost_per_tonne < aframax_cost_per_tonne
    print(f"\nVLCC Cost/Tonne: ${vlcc_cost_per_tonne:.2f}")
    print(f"Aframax Cost/Tonne: ${aframax_cost_per_tonne:.2f}")

def test_sts_transfer():
    vlcc_class = VesselClass(name="V", capacity=300000, speed=10, fuel_consumption_tonnes_per_day=50, daily_charter_rate=40000)
    aframax_class = VesselClass(name="A", capacity=100000, speed=10, fuel_consumption_tonnes_per_day=30, daily_charter_rate=20000)
    
    grade = CommodityGrade(name="Crude Oil", category="Energy")
    cargo = Cargo(id="c1", commodity=grade, quantity=250000) # Big load
    
    v_vlcc = Vessel(id="v1", name="VLCC", vessel_class=vlcc_class, current_location={"lat":0,"lon":0}, cargo=cargo)
    v_aframax = Vessel(id="v2", name="Aframax", vessel_class=aframax_class, current_location={"lat":0,"lon":0})
    
    # Try to transfer 50,000 tonnes
    success = LogisticsEngine.ship_to_ship_transfer(v_vlcc, v_aframax, 50000)
    
    assert success is True
    assert v_aframax.cargo.quantity == 50000
    assert v_vlcc.cargo.quantity == 200000
    
    # Try to overload Aframax (remaining 50k capacity)
    success_overload = LogisticsEngine.ship_to_ship_transfer(v_vlcc, v_aframax, 60000)
    assert success_overload is False
