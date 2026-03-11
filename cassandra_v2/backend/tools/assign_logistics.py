import json
import os
import random

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BACKEND_ROOT, "data/topology")

# Carriers
OIL_TANKERS = ["actor_frontline", "actor_euronav", "actor_cosco", "actor_maersk"] # Maersk has tankers too
LNG_CARRIERS = ["actor_teekay", "actor_frontline"] # Simplified
DRY_BULK = ["actor_star_bulk", "actor_golden_ocean", "actor_cosco"]
CONTAINER = ["actor_maersk", "actor_msc", "actor_cosco"]

# Pipelines
PIPE_RU = "actor_transneft"
PIPE_US = "actor_colonial"
PIPE_CA = "actor_tc_energy"

# Rail
RAIL_RU = "actor_rzd"
RAIL_US = "actor_bnsf"
RAIL_CA = "actor_cn_rail"
RAIL_AU = "actor_aurizon"

def assign_logistics():
    count = 0
    updated_files = 0
    
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                commodity = data.get("commodity", "Unknown")
                nodes = {n['id']: n for n in data.get('nodes', [])}
                file_changed = False
                
                # Determine Commodity Type for Sea Transport
                sea_carriers = CONTAINER # Default
                if commodity in ["Crude Oil", "Diesel", "Gasoline"]:
                    sea_carriers = OIL_TANKERS
                elif commodity in ["Natural Gas (LNG)"]:
                    sea_carriers = LNG_CARRIERS
                elif commodity in ["Coal", "Iron Ore", "Wheat", "Corn (Maize)", "Soybeans", "Bauxite"]:
                    sea_carriers = DRY_BULK
                
                for edge in data.get('edges', []):
                    mode = edge.get('transport_mode', 'sea')
                    
                    # Current carrier
                    current_carrier = edge.get('carrier_id')
                    new_carrier = current_carrier

                    # Resolve Region
                    src_node = nodes.get(edge['source'])
                    region = "International"
                    if src_node:
                        region = src_node.get('jurisdiction', 'International')
                    
                    if mode == "sea":
                        # If generic or empty, assign specific
                        if not current_carrier or current_carrier == "actor_maersk": # Maersk was default
                            new_carrier = random.choice(sea_carriers)
                    
                    elif mode == "rail":
                        if "Russia" in region: new_carrier = RAIL_RU
                        elif "USA" in region: new_carrier = RAIL_US
                        elif "Canada" in region: new_carrier = RAIL_CA
                        elif "Australia" in region: new_carrier = RAIL_AU
                        else: new_carrier = RAIL_US # Default to BNSF style if unknown
                    
                    elif mode == "pipe":
                        if "Russia" in region: new_carrier = PIPE_RU
                        elif "USA" in region: new_carrier = PIPE_US
                        elif "Canada" in region: new_carrier = PIPE_CA
                        else: new_carrier = PIPE_RU # Default
                        
                    # Apply
                    if new_carrier and new_carrier != current_carrier:
                        edge['carrier_id'] = new_carrier
                        count += 1
                        file_changed = True
                            
                if file_changed:
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2)
                    updated_files += 1
                    print(f"Updated {filename}")

    print(f"Assigned logistics to {count} edges across {updated_files} files.")

if __name__ == "__main__":
    assign_logistics()
