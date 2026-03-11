import random
from typing import Dict, List
from ..schema.market import Trader, PricePoint
from ..schema.cargo import Cargo

class FinanceEngine:
    @staticmethod
    def generate_next_price(current_price: PricePoint, tick: int) -> PricePoint:
        """
        Transformation in Time: Market Oracle.
        Generates a random walk price update.
        """
        change_pct = random.gauss(0, current_price.volatility)
        new_price = current_price.price * (1 + change_pct)
        
        return PricePoint(
            commodity_name=current_price.commodity_name,
            price=max(0.1, new_price), # No negative prices
            timestamp=tick,
            volatility=current_price.volatility
        )

    @staticmethod
    def calculate_demand(base_demand: float, current_price: float, price_elasticity: float = 0.5) -> float:
        """
        Sprint 7.1: Demand Destruction.
        Reduces demand as price rises relative to a $100 baseline.
        """
        baseline_price = 100.0
        if current_price <= baseline_price:
            return base_demand
            
        # Price ratio (e.g., $150 = 1.5)
        ratio = current_price / baseline_price
        
        # Reduced demand = base / (ratio ^ elasticity)
        # e.g., elasticity 1.0 means price 2x -> demand 0.5x
        destroyed_demand = base_demand / (ratio ** price_elasticity)
        return max(0.0, destroyed_demand)

    @staticmethod
    def get_storage_incentive(spot_price: float, expected_future_price: float, storage_cost: float) -> float:
        """
        Calculates the profit incentive to store inventory.
        Positive value = Contango (Incentive to store)
        Negative value = Backwardation (Incentive to sell now)
        """
        profit = expected_future_price - spot_price - storage_cost
        return profit

    @staticmethod
    def mark_to_market(trader: Trader, current_prices: Dict[str, float], margin_ratio: float = 0.1):
        """
        Mark-to-Market calculation.
        Updates trader's collateral value and calculates margin requirement.
        """
        total_inventory_value = 0.0
        for cargo in trader.inventory:
            price = current_prices.get(cargo.commodity.name, cargo.value_per_unit)
            total_inventory_value += cargo.quantity * price
            # Update snapshot on cargo
            cargo.value_per_unit = price
            
        trader.collateral_value = total_inventory_value
        # Margin requirement is a % of the total position value
        trader.margin_requirement = total_inventory_value * margin_ratio

    @staticmethod
    def check_liquidity_crisis(trader: Trader) -> bool:
        """
        The Bankruptcy Logic.
        Triggered if Margin Requirement > Cash + Credit.
        """
        total_liquidity = trader.cash + trader.credit_limit
        if trader.margin_requirement > total_liquidity:
            trader.is_bankrupt = True
            return True
        return False

    @staticmethod
    def execute_trade(buyer: Trader, seller: Trader, cargo: Cargo, price_per_unit: float) -> bool:
        """
        Transformation in Finance: Ownership transfer.
        """
        total_cost = cargo.quantity * price_per_unit
        
        # Check buyer liquidity
        if (buyer.cash + buyer.credit_limit) < total_cost:
            return False
            
        # Execute transfer
        buyer.cash -= total_cost
        seller.cash += total_cost
        
        # Move Cargo
        if cargo in seller.inventory:
            seller.inventory.remove(cargo)
        
        cargo.owner_id = buyer.id
        cargo.value_per_unit = price_per_unit
        buyer.inventory.append(cargo)
        
        return True
