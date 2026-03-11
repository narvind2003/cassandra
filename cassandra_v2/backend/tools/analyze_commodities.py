import json
import os
from collections import defaultdict

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BACKEND_ROOT, "data/topology")
ACTORS_FILE = os.path.join(BACKEND_ROOT, "data/actors/global_actors.json")

def analyze_commodities():
    with open(ACTORS_FILE, 'r') as f:
        actors = {a['id']: a for a in json.load(f)}
    
    report = {}
    
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                comm = data.get("commodity", "Unknown")
                nodes = data.get("nodes", [])
                edges = data.get("edges", [])
                
                # 1. Top Producers (Resource owners)
                producers = defaultdict(float)
                for n in nodes:
                    if n['type'] == 'resource' and n.get('owner_id'):
                        owner_name = actors.get(n['owner_id'], {}).get('name', 'Independent')
                        producers[owner_name] += 1 # Or use production_rate if available in JSON
                
                # 2. Top Traders / Carriers
                carriers = defaultdict(int)
                for e in edges:
                    if e.get('carrier_id'):
                        carrier_name = actors.get(e['carrier_id'], {}).get('name', 'Unknown')
                        carriers[carrier_name] += 1
                
                # 3. Top 5 Flows (Heuristic: longest lag or marked as critical)
                # For now, just take top 5 edges by lag or specific importance
                flows = []
                for e in edges:
                    src = next((n['label'] for n in nodes if n['id'] == e['source']), e['source'])
                    tgt = next((n['label'] for n in nodes if n['id'] == e['target']), e['target'])
                    flows.append(f"{src} → {tgt}")
                
                report[comm] = {
                    "top_producers": sorted(producers.keys(), key=lambda x: producers[x], reverse=True)[:5],
                    "top_logistics": sorted(carriers.keys(), key=lambda x: carriers[x], reverse=True)[:5],
                    "strategic_flows": flows[:5]
                }

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    analyze_commodities()
