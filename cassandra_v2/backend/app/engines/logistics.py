import math
import networkx as nx
from typing import Dict, List, Optional
from ..schema.vessel import Vessel, VesselClass
from ..schema.cargo import Cargo
from ..schema.node import Node
from ..schema.infrastructure import Infrastructure

class LogisticsEngine:
    def __init__(self, sea_lanes: dict, infrastructure: List[Infrastructure] = []):
        self.G = nx.Graph()
        self.waypoints = {}
        self.infra_constraints = {} # {node_id: {max_draft, max_beam}}
        
        # Build Constraint Map
        # Map infra IDs to graph node IDs (Simple heuristic: "infra_suez" -> "choke_suez")
        for infra in infrastructure:
            if infra.type in ["canal", "strait"]:
                # Find matching graph node by location or ID similarity
                # Assuming ID convention infra_X matches choke_X
                key = infra.id.replace("infra_", "choke_")
                self.infra_constraints[key] = {
                    "max_draft": infra.max_draft,
                    "max_beam": infra.max_beam
                }

        for wp in sea_lanes.get("waypoints", []):
            self.G.add_node(wp["id"], **wp)
            self.waypoints[wp["id"]] = wp
        for edge in sea_lanes.get("edges", []):
            self.G.add_edge(edge["source"], edge["target"], weight=edge["distance"])

    @staticmethod
    def haversine_distance(pos1: Dict[str, float], pos2: Dict[str, float]) -> float:
        """
        Calculates the great-circle distance between two points on the Earth 
        in nautical miles.
        """
        R = 3440.065 # Earth radius in nautical miles
        
        # Helper to get longitude
        def get_lon(pos):
            return pos.get("lon", pos.get("lng", 0.0))
            
        lat1, lon1 = math.radians(pos1["lat"]), math.radians(get_lon(pos1))
        lat2, lon2 = math.radians(pos2["lat"]), math.radians(get_lon(pos2))
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c

    def get_nearest_waypoint(self, pos: Dict[str, float]) -> str:
        """Finds the ID of the waypoint closest to a given lat/lng."""
        best_id = None
        min_dist = float('inf')
        for wp_id, wp in self.waypoints.items():
            d = self.haversine_distance(pos, wp["location"])
            if d < min_dist:
                min_dist = d
                best_id = wp_id
        return best_id

    def find_path(self, start_wp_id: str, end_wp_id: str, blocked_nodes: List[str] = [], vessel: Optional[Vessel] = None) -> List[str]:
        """Finds shortest path in sea lanes, avoiding blocked choke points and physical constraints."""
        try:
            # Determine physically impassable nodes for this vessel
            physically_blocked = []
            if vessel:
                v_class = vessel.vessel_class
                for node_id, constraints in self.infra_constraints.items():
                    if constraints["max_draft"] and v_class.max_draft > constraints["max_draft"]:
                        physically_blocked.append(node_id)
                    elif constraints["max_beam"] and v_class.beam > constraints["max_beam"]:
                        physically_blocked.append(node_id)

            # Combined Blocked List
            all_blocked = set(blocked_nodes + physically_blocked)
            
            active_nodes = [n for n in self.G.nodes if n not in all_blocked]
            sub_G = self.G.subgraph(active_nodes)
            
            if start_wp_id not in sub_G or end_wp_id not in sub_G:
                return []
                
            return nx.shortest_path(sub_G, source=start_wp_id, target=end_wp_id, weight="weight")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def calculate_path_distance(self, path_ids: List[str]) -> float:
        """Calculates total distance of a path of waypoint IDs."""
        total = 0.0
        for i in range(len(path_ids) - 1):
            if self.G.has_edge(path_ids[i], path_ids[i+1]):
                total += self.G[path_ids[i]][path_ids[i+1]]["weight"]
            else:
                # Fallback to haversine if edge missing for some reason
                p1 = self.waypoints[path_ids[i]]["location"]
                p2 = self.waypoints[path_ids[i+1]]["location"]
                total += self.haversine_distance(p1, p2)
        return total

    @staticmethod
    def calculate_route_cost(
        vessel: Vessel, 
        distance: float, 
        fuel_price: float, 
        canal_fees: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculates total cost and duration of a transit.
        """
        v_class = vessel.vessel_class
        
        # Duration in days
        # speed is in knots (nautical miles per hour)
        duration_days = (distance / v_class.speed) / 24.0
        
        fuel_cost = duration_days * v_class.fuel_consumption_tonnes_per_day * fuel_price
        charter_cost = duration_days * v_class.daily_charter_rate
        
        total_cost = fuel_cost + charter_cost + canal_fees
        
        return {
            "total_cost": total_cost,
            "duration_days": duration_days,
            "fuel_cost": fuel_cost,
            "charter_cost": charter_cost,
            "canal_fees": canal_fees
        }

    @staticmethod
    def ship_to_ship_transfer(
        vessel_a: Vessel, 
        vessel_b: Vessel, 
        quantity: float
    ) -> bool:
        """
        Transformation in Space: STS Transfer.
        Moves cargo from Vessel A to Vessel B.
        Used for ship-to-ship or origin obscuring.
        """
        if not vessel_a.cargo or vessel_a.cargo.quantity < quantity:
            return False
            
        remaining_capacity = vessel_b.vessel_class.capacity - (vessel_b.cargo.quantity if vessel_b.cargo else 0)
        
        if quantity > remaining_capacity:
            return False # Overload
            
        # Perform Transfer
        if not vessel_b.cargo:
            # First time cargo for B
            vessel_b.cargo = Cargo(
                id=f"sts_{vessel_a.cargo.id}",
                commodity=vessel_a.cargo.commodity,
                quantity=quantity,
                owner_id=vessel_a.cargo.owner_id,
                value_per_unit=vessel_a.cargo.value_per_unit
            )
        else:
            vessel_b.cargo.quantity += quantity
            
        vessel_a.cargo.quantity -= quantity
        
        if vessel_a.cargo.quantity <= 0:
            vessel_a.cargo = None
            
        return True

    def tick(self, vessels: List[Vessel], hours_per_tick: float = 24.0):
        """
        Processes a time step for all vessels.
        """
        for vessel in vessels:
            self.tick_vessel(vessel, hours_per_tick)

    @staticmethod
    def tick_vessel(vessel: Vessel, hours_per_tick: float = 24.0):
        """
        Moves the vessel along its path based on its speed and time elapsed.
        Follows route_path waypoints if available (Sprint 2).
        """
        if vessel.status != "transit":
            return

        # Determine current target
        target_location = None
        if vessel.route_path:
            target_location = vessel.route_path[0]
        else:
            target_location = vessel.destination_location

        if not target_location:
            return

        speed = vessel.current_speed
        dist_covered = speed * hours_per_tick
        
        # Calculate distance to current segment target
        dist_to_target = LogisticsEngine.haversine_distance(vessel.current_location, target_location)

        if dist_covered >= dist_to_target:
            # Reached current waypoint or destination
            vessel.current_location = target_location
            remaining_after_arrival = dist_covered - dist_to_target
            
            if vessel.route_path:
                vessel.route_path.pop(0)
                if vessel.route_path_ids:
                    vessel.route_path_ids.pop(0)
                # If there's more path or a destination, recursively continue movement with remaining time
                # For simplicity in this tick, we just stop at the waypoint and will continue next tick
                # or we can recurse. Let's recurse if there is more path.
                if vessel.route_path or (vessel.destination_location and vessel.current_location != vessel.destination_location):
                    vessel.distance_remaining -= dist_to_target
                    # We don't recurse to avoid infinite loops, just wait for next tick or use a loop
            else:
                # Arrived at final destination
                vessel.distance_remaining = 0
                vessel.status = "unloading"
                return
        else:
            # Move along the vector to current target
            pct = dist_covered / (dist_to_target + 0.000001)
            
            lat_start = vessel.current_location["lat"]
            lng_start = vessel.current_location.get("lng", vessel.current_location.get("lon", 0.0))
            
            lat_end = target_location["lat"]
            lng_end = target_location.get("lng", target_location.get("lon", 0.0))
            
            vessel.current_location = {
                "lat": lat_start + (lat_end - lat_start) * pct,
                "lng": lng_start + (lng_end - lng_start) * pct
            }
            vessel.distance_remaining -= dist_covered
