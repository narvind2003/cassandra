import json
import os
from typing import List, Tuple, Dict
from ..schema.node import Node, NodeSpec, Recipe
from ..schema.commodity import CommodityGrade
from ..schema.actor import Actor
from ..schema.infrastructure import Infrastructure
from ..core.config import settings

class UniversalLoader:
    @staticmethod
    def load_actors(data_dir: str = "data/actors") -> List[Actor]:
        actors = []
        if not os.path.exists(data_dir):
            data_dir = "cassandra_v2/backend/" + data_dir
            
        if not os.path.exists(data_dir):
            print(f"Warning: {data_dir} not found. No actors loaded.")
            return []
            
        for root, dirs, files in os.walk(data_dir):
            for filename in files:
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(root, filename), 'r') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                for item in data:
                                    actors.append(Actor(**item))
                            else:
                                print(f"Warning: {filename} does not contain a list of actors.")
                    except Exception as e:
                        print(f"Error loading actors from {filename}: {e}")
        
        print(f"Loaded {len(actors)} global actors.")
        return actors

    @staticmethod
    def load_infrastructure(data_dir: str = "data/logistics/infrastructure.json") -> List[Infrastructure]:
        infra = []
        if not os.path.exists(data_dir):
            data_dir = "cassandra_v2/backend/" + data_dir
            
        if not os.path.exists(data_dir):
            print(f"Warning: {data_dir} not found. No infrastructure loaded.")
            return []
            
        try:
            with open(data_dir, 'r') as f:
                data = json.load(f)
                for item in data:
                    infra.append(Infrastructure(**item))
        except Exception as e:
            print(f"Error loading infrastructure: {e}")
            
        print(f"Loaded {len(infra)} infrastructure items.")
        return infra

    @staticmethod
    def load_world(data_dir: str = "data/topology") -> Tuple[List[Node], List[dict]]:
        all_nodes = []
        all_edges = []
        
        # Adjust path relative to backend root if needed
        # Assuming run from backend/ directory
        if not os.path.exists(data_dir):
            # Fallback for when running from root
            data_dir = "cassandra_v2/backend/" + data_dir
            
        if not os.path.exists(data_dir):
            print(f"Warning: {data_dir} not found.")
            return [], []

        for root, dirs, files in os.walk(data_dir):
            for filename in files:
                if filename.endswith(".json"):
                    try:
                        # Determine category from directory name
                        dir_name = os.path.basename(root)
                        category = "Unknown"
                        if dir_name == "food":
                            category = "Food"
                        elif dir_name == "non_food":
                            category = "Non-Food"
                        
                        filepath = os.path.join(root, filename)
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            commodity_name = data.get('commodity', 'Unknown')
                            prefix = "".join([c if c.isalnum() else "_" for c in commodity_name]).lower()
                            
                            for n in data.get('nodes', []):
                                original_id = n['id']
                                new_id = f"{prefix}_{original_id}"
                                
                                # Map old JSON to new Node Schema
                                # Default specs for now
                                specs = NodeSpec()
                                
                                # v5.1 Fix: Ensure all port/hub keywords are forced to 'logistic' type
                                node_type = n['type']
                                lid = original_id.lower()
                                if any(k in lid for k in ["port", "hub", "log", "choke", "term", "airport", "border", "silo"]):
                                    node_type = "logistic"

                                recipes = []
                                if 'recipes' in n:
                                    for r in n['recipes']:
                                        recipes.append(Recipe(**r))
                                
                                # v6.0 Stability: JIT Inventory + Warm-up Loop
                                revenue = n.get('revenue_per_day', 0.0)
                                demand = n.get('base_demand', revenue / 10.0)
                                # Start with 14 days of buffer (fragile)
                                safety_stock = max(1000.0, demand * 14.0)

                                node = Node(
                                    id=new_id,
                                    label=n['label'],
                                    type=node_type,
                                    location=n['location'],
                                    specs=specs,
                                    recipes=recipes,
                                    # Ownership (v7.0)
                                    owner_id=n.get('owner_id'),
                                    operator_id=n.get('operator_id'),
                                    # Geopolitical (v7.0 Sprint 3)
                                    jurisdiction=n.get('jurisdiction', 'International'),
                                    risk_level=n.get('risk_level', 0.0),
                                    is_sanctioned=n.get('is_sanctioned', False),
                                    conflict_zone=n.get('conflict_zone', False),
                                    # Legacy fields mapping
                                    inventory={commodity_name: n.get('inventory', safety_stock)},
                                    revenue_per_day=revenue,
                                    base_demand=demand,
                                    commodity=commodity_name,
                                    category=category
                                )
                                
                                # v5.0 Fix: Seed recipe inputs
                                for r in recipes:
                                    for input_comm, qty in r.inputs.items():
                                        # Seed 90 days of input supply? 
                                        # Assume 1 batch per day * 90 days?
                                        # Or just a flat 5000 buffer.
                                        node.inventory[input_comm] = 5000.0
                                
                                all_nodes.append(node)
                            
                            for e in data.get('edges', []):
                                # Load Full Edge Metadata (v7.0)
                                all_edges.append({
                                    "source_id": f"{prefix}_{e['source']}",
                                    "target_id": f"{prefix}_{e['target']}",
                                    "lag_days": e.get('lag', 1),
                                    "capacity": e.get('capacity', 100.0),
                                    "carrier_id": e.get('carrier_id'),
                                    "transport_mode": e.get('transport_mode', 'sea'),
                                    "infrastructure_id": e.get('infrastructure_id')
                                })
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
        
        # Load Sea Lane Waypoints as Nodes (for visualization)
        sea_lanes = UniversalLoader.load_sea_lanes()
        for wp in sea_lanes.get("waypoints", []):
            # Check if node already exists (some hubs might be duplicated)
            if not any(n.id == wp["id"] for n in all_nodes):
                node = Node(
                    id=wp["id"],
                    label=wp["label"],
                    type="logistic",
                    subtype="waypoint",
                    location=wp["location"],
                    commodity="Logistics",
                    category="Infrastructure",
                    specs=NodeSpec(),
                    inventory={"Logistics": 10000.0},
                    revenue_per_day=0.0
                )
                all_nodes.append(node)

        print(f"Loaded {len(all_nodes)} nodes and {len(all_edges)} edges.")
        return all_nodes, all_edges

    @staticmethod
    def get_commodity_grade(name: str) -> CommodityGrade:
        """Utility to create or fetch a CommodityGrade object by name."""
        # In the future, this should look up properties in a master manifest.
        # For now, it returns a generic grade.
        return CommodityGrade(
            name=name,
            category="General",
            properties={}
        )

    @staticmethod
    def load_sea_lanes(filepath: str = "data/logistics/sea_lanes.json") -> dict:
        """Loads sea lane waypoints and edges."""
        if not os.path.exists(filepath):
            filepath = "cassandra_v2/backend/" + filepath
        
        if not os.path.exists(filepath):
            return {"waypoints": [], "edges": []}
            
        with open(filepath, 'r') as f:
            return json.load(f)
