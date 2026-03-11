import json
import os
import sys

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BACKEND_ROOT, "data/topology")

# Infrastructure ID Mapping
# 1. By Edge Note Keyword
NOTE_RULES = {
    "druzhba": "infra_druzhba",
    "espo": "infra_transneft_espo",
    "tmx": "infra_trans_mountain",
    "keystone": "infra_keystone",
    "colonial": "infra_colonial",
    "btc": "infra_btc",
    "cpc": "infra_cpc",
    "trans-siberian": "infra_trans_siberian",
    "rail": "infra_trans_siberian" # Fallback for Russian rail if not specific
}

# 2. By Connection to Choke Points (Node IDs)
CHOKE_RULES = {
    "suez": "infra_suez",
    "panama": "infra_panama",
    "hormuz": "infra_hormuz",
    "malacca": "infra_malacca",
    "bosphorus": "infra_bosphorus"
}

# 3. By Geography (Source/Target Keywords)
GEO_RULES = [
    { "mode": "pipe", "src": ["russia", "siberia"], "tgt": ["europe", "germany", "poland"], "id": "infra_druzhba" },
    { "mode": "rail", "src": ["russia", "siberia"], "tgt": ["china", "vladivostok"], "id": "infra_trans_siberian" },
    { "mode": "rail", "src": ["brazil", "carajas"], "tgt": ["port"], "id": "infra_carajas_rail" },
    { "mode": "sea", "src": ["qatar", "saudi", "uae"], "tgt": ["europe", "rotterdam"], "id": "infra_suez" },
    { "mode": "sea", "src": ["usa", "brazil"], "tgt": ["china", "japan", "asia"], "id": "infra_panama" }
]

def assign_infrastructure():
    count = 0
    updated_files = 0
    
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                nodes = {n['id']: n for n in data.get('nodes', [])}
                file_changed = False
                
                for edge in data.get('edges', []):
                    # 1. Check Notes
                    notes = edge.get('notes', '').lower()
                    matched_id = None
                    
                    for keyword, infra_id in NOTE_RULES.items():
                        if keyword in notes:
                            matched_id = infra_id
                            break
                    
                    # 2. Check Choke Points
                    if not matched_id:
                        src_id = edge['source'].lower()
                        tgt_id = edge['target'].lower()
                        for keyword, infra_id in CHOKE_RULES.items():
                            if keyword in src_id or keyword in tgt_id:
                                matched_id = infra_id
                                break
                    
                    # 3. Check Geo
                    if not matched_id:
                        src_node = nodes.get(edge['source'])
                        tgt_node = nodes.get(edge['target'])
                        if src_node and tgt_node:
                            src_text = (src_node.get('label', '') + " " + src_node.get('jurisdiction', '')).lower()
                            tgt_text = (tgt_node.get('label', '') + " " + tgt_node.get('jurisdiction', '')).lower()
                            mode = edge.get('transport_mode', 'sea')
                            
                            for rule in GEO_RULES:
                                if rule['mode'] == mode:
                                    # Check src keywords
                                    src_hit = any(k in src_text for k in rule['src'])
                                    tgt_hit = any(k in tgt_text for k in rule['tgt'])
                                    if src_hit and tgt_hit:
                                        matched_id = rule['id']
                                        break

                    # Apply
                    if matched_id:
                        if edge.get('infrastructure_id') != matched_id:
                            edge['infrastructure_id'] = matched_id
                            count += 1
                            file_changed = True
                            
                if file_changed:
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2)
                    updated_files += 1
                    print(f"Updated {filename}")

    print(f"Assigned infrastructure to {count} edges across {updated_files} files.")

if __name__ == "__main__":
    assign_infrastructure()