import json
import os

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BACKEND_ROOT, "data/topology")
FRONTEND_MANIFEST = os.path.abspath(os.path.join(BACKEND_ROOT, "../../cassandra_v2/frontend/src/data/commodity_manifest.ts"))

def audit_commodities():
    # 1. Get list of all commodity JSON files
    topology_files = []
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            if f.endswith(".json"):
                topology_files.append(os.path.join(root, f))
    
    # 2. Parse Frontend Manifest (crude regex-less scan)
    with open(FRONTEND_MANIFEST, 'r') as f:
        manifest_content = f.read()
    
    report = []
    
    for filepath in topology_files:
        filename = os.path.basename(filepath)
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except:
                report.append(f"❌ {filename}: CORRUPT JSON")
                continue
                
        commodity = data.get("commodity", "Unknown")
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        
        # Check Node Coverage
        total_nodes = len(nodes)
        nodes_with_owners = sum(1 for n in nodes if n.get("owner_id"))
        owner_pct = (nodes_with_owners / total_nodes * 100) if total_nodes > 0 else 0
        
        # Check Edge Coverage
        total_edges = len(edges)
        edges_with_metadata = sum(1 for e in edges if e.get("carrier_id") and e.get("transport_mode"))
        edge_pct = (edges_with_metadata / total_edges * 100) if total_edges > 0 else 0
        
        # Check Manifest Presence
        in_manifest = f'"{commodity}":' in manifest_content or f"'{commodity}':" in manifest_content
        
        status = "✅" if (owner_pct > 80 and edge_pct > 80 and in_manifest) else "⚠️"
        if owner_pct < 10 or not in_manifest: status = "🚨"
        
        report.append({
            "status": status,
            "file": filename,
            "commodity": commodity,
            "owner_pct": f"{owner_pct:.0f}%",
            "edge_pct": f"{edge_pct:.0f}%",
            "manifest": "YES" if in_manifest else "MISSING"
        })

    # Sort by urgency (MISSING manifest first, then low owner pct)
    report.sort(key=lambda x: (x['manifest'] == "YES", x['owner_pct']))
    
    print(f"{'STAT':<4} | {'FILE':<20} | {'COMMODITY':<20} | {'OWN%':<5} | {'EDGE%':<5} | {'MANIFEST'}")
    print("-" * 80)
    for r in report:
        print(f"{r['status']:<4} | {r['file']:<20} | {r['commodity']:<20} | {r['owner_pct']:<5} | {r['edge_pct']:<5} | {r['manifest']}")

if __name__ == "__main__":
    audit_commodities()
