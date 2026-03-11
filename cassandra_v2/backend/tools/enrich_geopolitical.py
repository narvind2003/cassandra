import json
import os

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BACKEND_ROOT, "data/topology")

# Geopolitical Configuration
RISK_MAP = {
    "Russia": {"risk": 0.9, "sanctioned": True},
    "Ukraine": {"risk": 1.0, "conflict": True},
    "Iran": {"risk": 0.8, "sanctioned": True},
    "Red Sea": {"risk": 0.9, "conflict": True},
    "Suez": {"risk": 0.7, "conflict": True},
    "DRC": {"risk": 0.6, "conflict": False},
    "Myanmar": {"risk": 0.8, "conflict": True},
    "Venezuela": {"risk": 0.7, "sanctioned": True}
}

COUNTRY_MAP = {
    "(RU)": "Russia", "Russia": "Russia",
    "(UA)": "Ukraine", "Ukraine": "Ukraine",
    "(CN)": "China", "China": "China",
    "(USA)": "USA", "US": "USA",
    "(Aus)": "Australia", "Australia": "Australia",
    "(Can)": "Canada", "Canada": "Canada",
    "(BR)": "Brazil", "Brazil": "Brazil",
    "(DRC)": "DR Congo", "DRC": "DR Congo",
    "(SA)": "Saudi Arabia", "Saudi": "Saudi Arabia",
    "(Qatar)": "Qatar",
    "(UAE)": "UAE",
    "(NL)": "Netherlands",
    "(BE)": "Belgium",
    "(FR)": "France",
    "(DE)": "Germany",
    "(ES)": "Spain",
    "(IT)": "Italy",
    "(JP)": "Japan",
    "(KR)": "South Korea",
    "(IN)": "India",
    "Suez": "Egypt",
    "Hormuz": "International",
    "Malacca": "International",
    "Panama": "Panama"
}

def enrich_geopolitical():
    count = 0
    
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                changed = False
                for node in data.get('nodes', []):
                    # 1. Assign Jurisdiction
                    detected_country = "International"
                    label = node.get('label', '')
                    for key, country in COUNTRY_MAP.items():
                        if key in label:
                            detected_country = country
                            break
                    
                    node['jurisdiction'] = detected_country
                    
                    # 2. Assign Risk & Sanctions
                    risk_info = RISK_MAP.get(detected_country)
                    # Special check for chokepoints in labels
                    if "Suez" in label or "Red Sea" in label:
                        risk_info = RISK_MAP.get("Red Sea")
                    
                    if risk_info:
                        node['risk_level'] = risk_info.get('risk', 0.1)
                        node['is_sanctioned'] = risk_info.get('sanctioned', False)
                        node['conflict_zone'] = risk_info.get('conflict', False)
                    else:
                        node['risk_level'] = 0.05 # Default low risk
                        node['is_sanctioned'] = False
                        node['conflict_zone'] = False
                    
                    changed = True
                    count += 1
                
                # Enrich Edges (Route Risk)
                for edge in data.get('edges', []):
                    # If target or source is high risk, edge gets higher risk
                    # This is simple for now, but in reality depends on the path.
                    edge['risk_level'] = 0.1 # Base
                    changed = True

                if changed:
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2)

    print(f"Enriched {count} nodes with Geopolitical metadata.")

if __name__ == "__main__":
    enrich_geopolitical()
