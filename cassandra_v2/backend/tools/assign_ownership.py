import json
import os
import sys

# Define the root path relative to this script
BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BACKEND_ROOT, "data/topology")

# Explicit Ownership Map: { "node_id_fragment": "actor_id" }
OWNERSHIP_MAP = {
    # -- ENERGY --
    "field_ghawar": "actor_aramco",
    "term_ras_tanura": "actor_aramco",
    "field_permian": "actor_exxon",
    "field_oilsands": "actor_shell",
    "ref_zhenhai": "actor_sinopec",
    "ref_jurong": "actor_shell",
    "field_north_dome": "actor_aramco", 
    "lng_ras_laffan": "actor_aramco",
    "field_marcellus": "actor_exxon",
    "field_yamal": "actor_gazprom",
    "lng_yamal": "actor_gazprom",
    
    # -- METALS --
    "mine_red_dog": "actor_teck",
    "mine_antamina": "actor_glencore",
    "mine_escondida": "actor_bhp",
    "mine_collahuasi": "actor_glencore",
    "mine_cerro_verde": "actor_freeport",
    "mine_morenci": "actor_freeport",
    "mine_grasberg": "actor_freeport",
    "mine_pilbara_bhp": "actor_bhp",
    "mine_pilbara_rio": "actor_rio",
    "mine_pilbara_fmg": "actor_fmg",
    "mine_carajas": "actor_vale",
    "mine_minas_rio": "actor_anglo",
    "mine_mutanda": "actor_glencore",
    "mine_kamoto": "actor_glencore",
    "mine_tenke": "actor_cmoc",
    "mine_kisanfu": "actor_cmoc",
    "mine_greenbushes": "actor_albemarle",
    "mine_pilgangoora": "actor_pilbara",
    "mine_wodgina": "actor_albemarle",
    "mine_salar_atacama_sqm": "actor_sqm",
    "mine_salar_atacama_alb": "actor_albemarle",
    "mine_cigar_lake": "actor_cameco",
    "mine_inkai": "actor_kazatomprom",
    "mine_norilsk": "actor_norilsk",
    "mine_bushveld": "actor_anglo_plat",
    "mine_muruntau": "actor_state_uz",
    "mine_nevada": "actor_barrick",
    "mine_boddington": "actor_newmont",
    "mine_fresnillo": "actor_fresnillo",
    "mine_penasquito": "actor_newmont",
    "smelt_trail": "actor_teck",
    "smelt_onsan": "actor_korea_zinc",
    "smelt_nyrstar": "actor_nyrstar",
    
    # -- AGRI & FOOD --
    "silo_decatur": "actor_adm",
    "crush_rosario": "actor_cargill",
    "crush_rotterdam": "actor_bunge",
    "ref_wilmar": "actor_wilmar",
    "proc_cofco": "actor_cofco",
    "mine_nutrien": "actor_nutrien",
    "mine_mosaic": "actor_mosaic",
    "packer_jbs": "actor_jbs",
    "packer_tyson": "actor_tyson",
    "mfr_mcdonalds": "actor_mcdonalds",
    "mfr_starbucks": "actor_starbucks",
    "mfr_nestle": "actor_nestle",
    "mfr_clarios": "actor_clarios",
    
    # -- TUNA (Explicit) --
    "proc_bangkok": "actor_thai_union",
    "proc_manta": "actor_thai_union", 
    "fleet_pacific": "actor_maruha_nichiro", 
    
    # -- DAIRY (Explicit) --
    "farm_nz": "actor_fonterra",
    "proc_fonterra": "actor_fonterra",
    "mkt_china": "actor_nestle", 
    
    # -- RICE (Explicit) --
    "farm_thai": "actor_state_thai",
    "farm_vietnam": "actor_state_vietnam",
    "mill_bangkok": "actor_state_thai",
    "mill_hcmc": "actor_state_vietnam",
    
    # -- SALMON (Explicit) --
    "farm_norway": "actor_mowi",
    "farm_chile": "actor_mowi", 
    "proc_oslo": "actor_mowi",
    
    # -- WINE (Explicit) --
    "vines_bordeaux": "actor_lvmh",
    "vines_napa": "actor_constellation",
    "proc_le_havre": "actor_lvmh",
    
    # -- COCOA (Explicit) --
    "farm_ivory_coast": "actor_state_ivory_coast",
    "grind_amsterdam": "actor_barrick", 
    "grind_abidjan": "actor_cargill",
    "mfr_chocolate": "actor_nestle",
    
    # -- TEA (Explicit) --
    "farm_kenya": "actor_unilever", 
    "auction_mombasa": "actor_state_kenya",
    "blend_dubai": "actor_unilever",
    
    # -- RUBBER (Explicit) --
    "farm_thailand": "actor_halcyon",
    "proc_rubber": "actor_halcyon",
    "mfr_tire": "actor_bridgestone",
    
    # -- TOMATOES (Explicit) --
    "farm_california": "actor_morning_star",
    "proc_paste": "actor_morning_star",
    
    # -- POTATOES (Explicit) --
    "farm_idaho": "actor_lamb_weston",
    "proc_fries": "actor_lamb_weston"
}

# GEO HEURISTICS
GEO_HEURISTICS = {
    "Russia": {
        "resource": "actor_gazprom",
        "logistic": "actor_gazprom"
    },
    "Ukraine": {
        "resource": "actor_state_ua",
        "logistic": "actor_state_ua"
    },
    "China": {
        "resource": "actor_cofco",
        "transformation": "actor_sinopec"
    },
    "Saudi Arabia": {
        "resource": "actor_aramco",
        "logistic": "actor_aramco"
    },
    "Chile": {
        "resource": "actor_codelco"
    },
    "Brazil": {
        "resource": "actor_jbs",
        "logistic": "actor_vale"
    },
    "Australia": {
        "resource": "actor_bhp"
    },
    "Canada": {
        "resource": "actor_nutrien"
    }
}

# KEYWORD MATCHING
KEYWORD_MAP = {
    "Kansas": "actor_adm",
    "Iowa": "actor_adm",
    "Illinois": "actor_cargill",
    "Mississippi": "actor_cargill",
    "Santos": "actor_cargill",
    "Novorossiysk": "actor_viterra",
    "Odessa": "actor_state_ua",
    "Teck": "actor_teck",
    "Nyrstar": "actor_nyrstar",
    "Korea Zinc": "actor_korea_zinc",
    "West Fraser": "actor_west_fraser",
    "Canfor": "actor_canfor",
    "JBS": "actor_jbs",
    "Tyson": "actor_tyson",
    "Nestle": "actor_nestle",
    "Starbucks": "actor_starbucks",
    "McDonald": "actor_mcdonalds",
    "Clarios": "actor_clarios",
    "Cameco": "actor_cameco",
    "Barrick": "actor_barrick",
    "Newmont": "actor_newmont",
    "Fresnillo": "actor_fresnillo",
    "Glencore": "actor_glencore",
    "BHP": "actor_bhp",
    "Rio Tinto": "actor_rio",
    "Vale": "actor_vale",
    "Freeport": "actor_freeport",
    "Codelco": "actor_codelco",
    "Aramco": "actor_aramco",
    "Shell": "actor_shell",
    "Exxon": "actor_exxon",
    "BP": "actor_bp",
    "Total": "actor_total",
    "Chevron": "actor_chevron",
    "Sinopec": "actor_sinopec",
    "Gazprom": "actor_gazprom",
    "Cargill": "actor_cargill",
    "ADM": "actor_adm",
    "Bunge": "actor_bunge",
    "Wilmar": "actor_wilmar",
    "COFCO": "actor_cofco",
    "Nutrien": "actor_nutrien",
    "Mosaic": "actor_mosaic",
    "Tesla": "actor_tesla",
    "Apple": "actor_apple",
    "TSMC": "actor_tsmc",
    "Samsung": "actor_samsung",
    "Toyota": "actor_toyota",
    "Volkswagen": "actor_vw",
    "VW": "actor_vw",
    "Foxconn": "actor_foxconn",
    "CATL": "actor_catl",
    "BYD": "actor_byd",
    "Albemarle": "actor_albemarle",
    "SQM": "actor_sqm",
    "Pilbara": "actor_pilbara",
    "Ganfeng": "actor_ganfeng",
    "CMOC": "actor_cmoc",
    "Huayou": "actor_huayou",
    "Maersk": "actor_maersk",
    "MSC": "actor_msc"
}

def update_topology_files():
    count = 0
    updated_files = 0
    
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                file_changed = False
                for node in data.get('nodes', []):
                    new_owner = None
                    # 1. ID Map
                    for key, owner in OWNERSHIP_MAP.items():
                        if key in node['id']:
                            new_owner = owner
                            break
                    # 2. Geo
                    if not new_owner:
                        juris = node.get('jurisdiction')
                        ntype = node.get('type')
                        if juris in GEO_HEURISTICS:
                            new_owner = GEO_HEURISTICS[juris].get(ntype)
                    # 3. Keywords
                    if not new_owner:
                        for key, owner in KEYWORD_MAP.items():
                            if key.lower() in node['label'].lower():
                                new_owner = owner
                                break
                    if new_owner:
                        if node.get('owner_id') != new_owner:
                            node['owner_id'] = new_owner
                            count += 1
                            file_changed = True
                            
                if file_changed:
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2)
                    updated_files += 1
                    print(f"Updated {filename}")

    print(f"Done. Assigned ownership to {count} nodes across {updated_files} files.")

if __name__ == "__main__":
    update_topology_files()
