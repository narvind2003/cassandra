from typing import List, Dict
from .scenarios import Injection

class PlaybookEntry:
    def __init__(self, id: str, title: str, description: str, injections: List[Injection]):
        self.id = id
        self.title = title
        self.description = description
        self.injections = injections

class Playbook:
    SCENARIOS = [
        PlaybookEntry(
            id="crisis_chip_war",
            title="The Silicon Blockade",
            description="A total naval blockade of the Taiwan Strait halts 90% of advanced semiconductor shipments. Watch the impact on Apple, Tesla, and global tech.",
            injections=[
                Injection(target_id="choke_taiwan_strait", type="blockage", severity=1.0),
                Injection(target_id="fab_tsmc_hsinchu", type="strike", severity=0.8) # Internal disruption
            ]
        ),
        PlaybookEntry(
            id="crisis_energy_2022",
            title="Energy Crisis Redux",
            description="Simulates the 2022 disruption: Northern Stream pipelines cut, plus a strike at Qatari LNG terminals. Europe freezes.",
            injections=[
                Injection(target_id="choke_hormuz", type="blockage", severity=1.0), # Blocks Qatar
                Injection(target_id="field_yamal", type="embargo", severity=1.0) # Russia Embargo
            ]
        ),
        PlaybookEntry(
            id="crisis_food_security",
            title="The Hunger Games",
            description="Simultaneous failure of the Black Sea Grain Corridor and a drought (strike) in the US Midwest. Wheat and Corn prices skyrocket.",
            injections=[
                Injection(target_id="choke_bosphorus", type="blockage", severity=1.0), # Black Sea
                Injection(target_id="farm_kansas", type="strike", severity=0.7), # Drought
                Injection(target_id="farm_iowa_corn", type="strike", severity=0.7)
            ]
        ),
        PlaybookEntry(
            id="crisis_ev_bottleneck",
            title="The Lithium Trap",
            description="A coup in a major Lithium producing region combined with a refinery fire in China blocks the EV battery supply chain.",
            injections=[
                Injection(target_id="mine_pilbara_lithium", type="strike", severity=1.0),
                Injection(target_id="ref_tianqi", type="blockage", severity=1.0)
            ]
        ),
        PlaybookEntry(
            id="crisis_suez_max",
            title="Suez Max (Ever Given II)",
            description="A total, prolonged blockage of the Suez Canal affecting Oil, Consumer Goods, and Coffee simultaneously.",
            injections=[
                Injection(target_id="choke_suez", type="blockage", severity=1.0)
            ]
        ),
        PlaybookEntry(
            id="narrative_marc_rich",
            title="The Marc Rich Pivot",
            description="Sanctions on Russian Urals force a massive redirect to Asia. Watch as traders leverage the 'Shadow Fleet' and STS transfers in the Med.",
            injections=[
                Injection(target_id="oil_term_novorossiysk", type="embargo", severity=1.0),
                Injection(target_id="oil_hub_rotterdam", type="embargo", severity=1.0),
            ]
        ),
        PlaybookEntry(
            id="narrative_glencore_kurdistan",
            title="The Kurdistan Pre-Pay",
            description="Political turmoil blocks official Ceyhan pipelines. Glencore-style pre-pays attempt to move oil via truck to alternate ports.",
            injections=[
                Injection(target_id="infra_btc", type="blockage", severity=1.0)
            ]
        ),
        PlaybookEntry(
            id="narrative_cushing_top",
            title="Cushing Tank Top",
            description="Negative WTI prices! US demand collapses while Permian keeps pumping. Cushing storage fills to 100%.",
            injections=[
                Injection(target_id="oil_retail_gas_usa", type="strike", severity=0.8), # Demand drop
            ]
        )
    ]

    @staticmethod
    def get_all() -> List[Dict]:
        return [
            {
                "id": s.id,
                "title": s.title,
                "description": s.description,
                "injections": [i.dict() for i in s.injections]
            }
            for s in Playbook.SCENARIOS
        ]

    @staticmethod
    def get_injections(scenario_id: str) -> List[Injection]:
        for s in Playbook.SCENARIOS:
            if s.id == scenario_id:
                return s.injections
        return []