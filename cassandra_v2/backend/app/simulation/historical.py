from typing import List, Dict, Optional
import json
from pydantic import BaseModel

class HistoricalEvent(BaseModel):
    tick: int
    type: str # "blockage", "strike", "price_set"
    target_id: str
    value: float
    commodity: Optional[str] = None

class HistoricalReplayEngine:
    def __init__(self):
        self.events: List[HistoricalEvent] = []

    def load_scenario(self, name: str):
        """Loads a pre-packaged historical scenario."""
        if name == "energy_crisis_2022":
            # Russia Gas Cutoff Replay
            self.events = [
                # Day 5: Nord Stream Blockage
                HistoricalEvent(tick=5, type="blockage", target_id="non_food_lng_yamal", value=1.0),
                # Day 10: Price Spike for Gas
                HistoricalEvent(tick=10, type="price_set", target_id="Natural Gas (LNG)", value=300.0),
                # Day 15: Fertilizer plant strike (due to costs)
                HistoricalEvent(tick=15, type="strike", target_id="non_food_plant_yara_norway", value=0.8)
            ]
        elif name == "ever_given_2021":
            # Suez Canal Blockage Replay
            self.events = [
                # Day 2: The ship gets stuck
                HistoricalEvent(tick=2, type="blockage", target_id="choke_suez", value=1.0),
                # Day 8: The ship is freed (6 days later)
                # We model unblocking by having the blockage expire or setting value to 0. 
                # Since ScenarioEngine handles duration via start/end, replay events usually trigger start.
                # Here we assume the injection lasts for a set duration or we inject an 'unblock' event.
                # For simplicity in this engine, we'll let the Scenario logic handle duration (15 days default),
                # or we can assume this event starts a 6-day blockage.
            ]

    def get_events_for_tick(self, tick: int) -> List[HistoricalEvent]:
        return [e for e in self.events if e.tick == tick]
