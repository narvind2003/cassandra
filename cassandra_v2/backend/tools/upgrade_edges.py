import json
import os
import sys

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BACKEND_ROOT, "data/topology")

# Heuristic Mapping for Carriers
# If a route touches these ports/regions, we assign a dominant carrier.
# Priority: Pipeline > Rail > Sea
CARRIER_RULES = [
    { "type": "pipe", "keywords": ["pipe", "line"], "carrier": "actor_log_pipeline" },
    { "type": "rail", "keywords": ["rail", "train"], "carrier": "actor_log_rail" },
    { "type": "sea", "regions": ["China", "Asia", "Singapore"], "carrier": "actor_cosco" },
    { "type": "sea", "regions": ["Europe", "Rotterdam", "Hamburg"], "carrier": "actor_maersk" },
    { "type": "sea", "regions": ["USA", "America"], "carrier": "actor_msc" },
    { "type": "sea", "default": True, "carrier": "actor_maersk" }
]

def upgrade_edges():
    count = 0
    updated_files = 0
    
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    file_changed = False
                    commodity = data.get("commodity", "Unknown")
                    
                    for edge in data.get('edges', []):
                        # Add carrier_id and transport_mode if missing
                        if "carrier_id" not in edge:
                            edge["carrier_id"] = None
                            edge["transport_mode"] = "sea" # Default
                            
                            # Deduce Mode
                            notes = edge.get("notes", "").lower()
                            if "pipe" in notes:
                                edge["transport_mode"] = "pipe"
                                edge["carrier_id"] = "actor_log_pipeline"
                            elif "rail" in notes:
                                edge["transport_mode"] = "rail"
                                edge["carrier_id"] = "actor_log_rail"
                            elif "road" in notes or "truck" in notes:
                                edge["transport_mode"] = "road"
                                edge["carrier_id"] = "actor_log_road"
                            else:
                                # Sea Logic
                                edge["transport_mode"] = "sea"
                                # Find Carrier based on source/target node labels (requires lookups, doing simple heuristic now)
                                # We don't have node labels here easily without a lookup map.
                                # Simple heuristic: Random deterministic assignment or just default for now.
                                edge["carrier_id"] = "actor_maersk" # Placeholder default
                            
                            file_changed = True
                            count += 1
                            
                    if file_changed:
                        with open(filepath, 'w') as f:
                            json.dump(data, f, indent=2)
                        updated_files += 1
                        print(f"Upgraded edges in {filename}")
                        
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    print(f"Upgraded {count} edges across {updated_files} files.")

if __name__ == "__main__":
    upgrade_edges()
