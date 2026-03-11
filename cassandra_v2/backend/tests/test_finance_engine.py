import pytest
from app.schema.market import Trader, PricePoint
from app.schema.cargo import Cargo
from app.schema.commodity import CommodityGrade
from app.engines.finance import FinanceEngine

def test_market_random_walk():
    start_price = PricePoint(commodity_name="Oil", price=80.0, timestamp=0, volatility=0.1)
    
    # Generate 100 ticks and check if they stay positive
    current = start_price
    for i in range(1, 101):
        current = FinanceEngine.generate_next_price(current, i)
        assert current.price > 0
        assert current.timestamp == i

def test_margin_call_and_bankruptcy():
    # Trader with $1M cash and $2M credit limit
    trader = Trader(id="t1", name="Overleveraged Alpha", cash=1000000, credit_limit=2000000)
    
    # They hold 1,000,000 barrels of Oil (Current price $80)
    oil_grade = CommodityGrade(name="Oil", category="Energy")
    cargo = Cargo(id="c1", commodity=oil_grade, quantity=1000000, value_per_unit=80.0)
    trader.inventory.append(cargo)
    
    # 1. Normal State: Price $80
    # Position Value: $80M. Margin (10%): $8M. Liquidity: $3M.
    # WAIT - In this setup they are already in trouble if margin is 10% of total value.
    # Let's adjust margin ratio for the test or liquidity.
    
    prices = {"Oil": 80.0}
    FinanceEngine.mark_to_market(trader, prices, margin_ratio=0.01) # 1% margin
    # Position: $80M. Margin: $800,000. Liquidity: $3,000,000. OK.
    assert trader.margin_requirement == 800000
    assert FinanceEngine.check_liquidity_crisis(trader) is False
    
    # 2. Crisis State: Price drops to $40 (Flash Crash)
    # Position: $40M. Margin: $400,000. 
    # BUT wait, margin usually increases during volatility, or let's say they bought more.
    # Let's keep it simple: Liquidity crunch.
    
    # Trader lost cash elsewhere
    trader.cash = 100000 
    # Total Liquidity: $2.1M.
    # Price rises to $300 (Short Squeeze).
    # Position: $300M. Margin (1%): $3,000,000.
    prices = {"Oil": 300.0}
    FinanceEngine.mark_to_market(trader, prices, margin_ratio=0.01)
    assert trader.margin_requirement == 3000000
    
    # CRISIS: Margin ($3M) > Liquidity ($2.1M)
    is_bankrupt = FinanceEngine.check_liquidity_crisis(trader)
    assert is_bankrupt is True
    assert trader.is_bankrupt is True

def test_ownership_transfer():
    buyer = Trader(id="b1", name="Buyer", cash=5000)
    seller = Trader(id="s1", name="Seller", cash=0)
    
    grade = CommodityGrade(name="Gold", category="Metal")
    cargo = Cargo(id="c1", commodity=grade, quantity=10) # 10 units
    seller.inventory.append(cargo)
    
    # Price is $400/unit -> Total $4000
    success = FinanceEngine.execute_trade(buyer, seller, cargo, 400.0)
    
    assert success is True
    assert buyer.cash == 1000
    assert seller.cash == 4000
    assert cargo in buyer.inventory
    assert cargo not in seller.inventory
    assert cargo.owner_id == "b1"
