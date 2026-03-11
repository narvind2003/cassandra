from typing import List, Dict
from ..schema.node import Node
from ..schema.cargo import Cargo

class StrategicReservesAgent:
    """
    If a node's inventory falls below a threshold, this agent 
    injects emergency supply from strategic reserves.
    """
    def __init__(self, target_node_id: str, commodity: str, threshold: float, release_amount: float):
        self.target_node_id = target_node_id
        self.commodity = commodity
        self.threshold = threshold
        self.release_amount = release_amount

    def step(self, nodes: List[Node]):
        for node in nodes:
            if node.id == self.target_node_id:
                current_inv = node.inventory.get(self.commodity, 0)
                if current_inv < self.threshold:
                    node.inventory[self.commodity] = current_inv + self.release_amount
                    print(f"[AGENT] Strategic Reserve Release: {self.release_amount} {self.commodity} to {node.label}")

class SwingProducerAgent:
    """
    Increases production capacity if global prices exceed a threshold.
    """
    def __init__(self, node_id: str, threshold_price: float, extra_capacity: float):
        self.node_id = node_id
        self.threshold_price = threshold_price
        self.extra_capacity = extra_capacity

    def step(self, nodes: List[Node], current_price: float):
        if current_price > self.threshold_price:
            for node in nodes:
                if node.id == self.node_id:
                    # In a real system, this would modify a dynamic capacity field
                    # For now, we'll just inject extra inventory to simulate extra production
                    node.inventory[node.commodity] = node.inventory.get(node.commodity, 0) + self.extra_capacity
                    print(f"[AGENT] Swing Producer Ramp-up at {node.label}")
