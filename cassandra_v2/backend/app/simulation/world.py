import networkx as nx
import random
from typing import List, Dict, Optional
from ..schema.node import Node
from ..schema.cargo import Cargo
from ..schema.vessel import Vessel, VesselClass
from ..schema.market import Trader, PricePoint
from ..schema.compliance import ComplianceProfile
from .scenarios import ScenarioEngine, Scenario, Injection
from .agents import StrategicReservesAgent, SwingProducerAgent
from ..engines.logistics import LogisticsEngine
from ..engines.finance import FinanceEngine
from ..engines.compliance import ComplianceEngine
from ..engines.physics import PhysicsEngine
from ..services.loader import UniversalLoader
from ..services.market_oracle import MarketOracle
from ..core.config import settings

class World:
    def __init__(self):
        self.nodes, self.raw_edges = UniversalLoader.load_world()
        self.actors = UniversalLoader.load_actors()
        self.G = nx.DiGraph()
        self._build_graph()
        self.node_index = {n.id: n for n in self.nodes}
        
        # Engines
        self.scenario_engine = ScenarioEngine()
        self.logistics_engine = LogisticsEngine(
            UniversalLoader.load_sea_lanes(),
            UniversalLoader.load_infrastructure()
        )
        
        # State Management
        self.tick = 0
        self.vessels: List[Vessel] = []
        self.traders: List[Trader] = []
        self.compliance_profiles: Dict[str, ComplianceProfile] = {}
        self.prices: Dict[str, PricePoint] = {}
        self.agents = [
            StrategicReservesAgent(target_node_id="non_food_lng_ras_laffan", commodity="Natural Gas (LNG)", threshold=1000.0, release_amount=5000.0),
            SwingProducerAgent(node_id="non_food_field_marcellus", threshold_price=120.0, extra_capacity=2000.0)
        ]
        
        # Initialize Market
        self._init_market()
        self._balance_world() # Sprint 5.0 Stability
        self._init_logistics()
        self._init_traders()
        self._injections_applied = False
        self._injection_duration_days: Optional[int] = None

        # v6.0 Warm-up Phase: Prime the world for 60 days
        self.is_warming_up = True
        for _ in range(60):
            self.step([])
        self.is_warming_up = False
        self.tick = 0 # Reset tick counter so user starts at Day 0

        # Load Sea Lanes for API response
        self.sea_lanes = UniversalLoader.load_sea_lanes()

    def _build_graph(self):
        for n in self.nodes:
            self.G.add_node(n.id, **n.dict())
        for e in self.raw_edges:
            self.G.add_edge(e["source_id"], e["target_id"], **e)

    def _init_market(self):
        """Initialize prices for all commodities using Real-Time Data where possible."""
        print("Fetching Live Market Data...")
        live_prices = MarketOracle.fetch_all_prices()
        
        commodities = set(n.commodity for n in self.nodes)
        for comm in commodities:
            # Use live price or default to 100.0
            base_price = live_prices.get(comm, 100.0)
            
            self.prices[comm] = PricePoint(
                commodity_name=comm,
                price=base_price,
                timestamp=0,
                volatility=0.01 
            )
        print("Market Initialization Complete.")

    def _balance_world(self):
        """
        Sprint 3 Task 3.2: Auto-Replenishment.
        Ensures global production rate matches or exceeds global consumption.
        """
        # 1. Calculate total demand per commodity
        global_demand: Dict[str, float] = {}
        for node in self.nodes:
            if node.type == "retail":
                global_demand[node.commodity] = global_demand.get(node.commodity, 0.0) + node.base_demand
        
        # 2. Distribute required production to resource nodes
        for commodity, total_req in global_demand.items():
            resources = [n for n in self.nodes if n.type == "resource" and n.commodity == commodity]
            if resources:
                # Share the load + 50% buffer (v6.1 tuning)
                share = (total_req * 1.5) / len(resources)
                for res in resources:
                    res.specs.production_rate = max(share, 100.0) # Min 100
            else:
                # Handle cases where demand exists but no direct resource (e.g. processed goods)
                # In a deep chain, we should balance the TOP of the chain.
                # For MVP, we ensure the source nodes of any chain are boosted.
                pass

    def _init_logistics(self):
        """Initialize a fleet assigned to specific routes."""
        # Define Vessel Classes
        vlcc = VesselClass(name="VLCC", type="tanker", capacity=200000, speed=13, fuel_consumption_tonnes_per_day=50, daily_charter_rate=40000, max_draft=20.0, beam=60.0)
        suezmax = VesselClass(name="Suezmax", type="tanker", capacity=150000, speed=14, fuel_consumption_tonnes_per_day=40, daily_charter_rate=30000, max_draft=16.0, beam=50.0)
        aframax = VesselClass(name="Aframax", type="tanker", capacity=100000, speed=14.5, fuel_consumption_tonnes_per_day=35, daily_charter_rate=25000, max_draft=14.0, beam=42.0)
        
        capesize = VesselClass(name="Capesize", type="bulker", capacity=170000, speed=12, fuel_consumption_tonnes_per_day=45, daily_charter_rate=35000, max_draft=18.0, beam=45.0)
        panamax = VesselClass(name="Panamax", type="bulker", capacity=75000, speed=13, fuel_consumption_tonnes_per_day=30, daily_charter_rate=20000, max_draft=12.0, beam=32.2)
        
        qflex = VesselClass(name="Q-Flex", type="gas", capacity=90000, speed=19, fuel_consumption_tonnes_per_day=60, daily_charter_rate=60000, max_draft=12.0, beam=50.0)
        
        classes = [vlcc, suezmax, aframax, capesize, panamax, qflex]
        
        # v5.0 FIX: Only spawn at PORTS (type='logistic') to prevent land-ships.
        ports = [n for n in self.nodes if n.type == "logistic"]
        
        # Ensure we have ports to assign to
        if not ports:
            print("Warning: No logistic nodes found for vessel spawning.")
            return

        # Spawn 60 vessels distributed across random ports
        for i in range(60):
            port = random.choice(ports)
            v_class = random.choice(classes)
            
            # Simple heuristic for class selection based on port region?
            # For now random is fine, constraints will filter paths.
            
            v = Vessel(
                id=f"vessel_{i}",
                name=f"{v_class.name} Voyager {i}",
                vessel_class=v_class,
                current_location=port.location,
                status="idle"
            )
            self.vessels.append(v)

    def _init_traders(self):
        t1 = Trader(id="trader_us", name="Liberty Trading", cash=10000000)
        p1 = ComplianceProfile(entity_id="trader_us", jurisdiction="US")
        t2 = Trader(id="trader_eu", name="Euro Commodities", cash=10000000)
        p2 = ComplianceProfile(entity_id="trader_eu", jurisdiction="EU")
        self.traders = [t1, t2]
        self.compliance_profiles = {"trader_us": p1, "trader_eu": p2}

    def step(self, injections: List[Injection]):
        """Executes one simulation tick (1 day) with v4 deterministic logic."""
        self.tick += 1
        self.last_injections = injections # Track for tension logic

        # Per-tick metrics for systemic risk
        self.node_demand: Dict[str, float] = {}
        self.node_unmet_demand: Dict[str, float] = {}
        self.node_unmet_value: Dict[str, float] = {}
        self.node_revenue_loss: Dict[str, float] = {}
        
        # 1. Process Scenarios
        if injections and not self._injections_applied:
            duration = self._injection_duration_days or 15
            for inj in injections:
                self.scenario_engine.inject(Scenario(
                    id=f"manual_{self.tick}_{inj.target_id}_{inj.type}",
                    type=inj.type,
                    target_id=inj.target_id,
                    severity=inj.severity,
                    start_tick=self.tick,
                    end_tick=self.tick + duration
                ))
            self._injections_applied = True

        blocked_nodes = self.scenario_engine.get_blocked_nodes(self.tick)

        # 2. Update Market Prices
        for comm, price_point in self.prices.items():
            self.prices[comm] = FinanceEngine.generate_next_price(price_point, self.tick)

        # 2.5 Reactive Agents (Sprint 6)
        for agent in self.agents:
            if isinstance(agent, StrategicReservesAgent):
                agent.step(self.nodes)
            elif isinstance(agent, SwingProducerAgent):
                comm = next((n.commodity for n in self.nodes if n.id == agent.node_id), None)
                if comm and comm in self.prices:
                    agent.step(self.nodes, self.prices[comm].price)

        # v6.0 Task 1.2: Hinterland Logic (Mine -> Port transfer)
        for n in self.nodes:
            if n.type == "resource":
                # Find connected logistic nodes
                out_edges = self.G.out_edges(n.id, data=True)
                for _, target_id, data in out_edges:
                    target_node = next((node for node in self.nodes if node.id == target_id), None)
                    if target_node and target_node.type == "logistic":
                        # Transfer commodity
                        amount_to_move = n.inventory.get(n.commodity, 0)
                        # Simulate a "daily throughput" or just move everything for now
                        n.inventory[n.commodity] = 0
                        target_node.inventory[n.commodity] = target_node.inventory.get(n.commodity, 0) + amount_to_move

        # 3. Node Processing (Production/Refining/Consumption)
        self.current_tick_unmet_demand = 0.0
        
        for node in self.nodes:
            cap_factor = self.scenario_engine.get_capacity_factor(node.id, self.tick)
            if node.id in blocked_nodes: cap_factor = 0.0
            
            if node.type == "resource":
                # ... (existing resource logic)
                if node.recipes:
                    inputs = [Cargo(id=f"in_{node.id}_{c}", commodity=UniversalLoader.get_commodity_grade(c), quantity=q) 
                             for c, q in node.inventory.items() if q > 0]
                    outputs = PhysicsEngine.process(node, inputs)
                    # For resources, we clear processed inputs but keep the generated commodity
                    # Simplified: just update inventory with outputs
                    node.inventory = {}
                    for out in outputs:
                        node.inventory[out.commodity.name] = node.inventory.get(out.commodity.name, 0) + out.quantity
                else:
                    # Default autonomous generation (Sprint 3: Balanced rate)
                    gen_rate = (node.specs.production_rate * cap_factor)
                    node.inventory[node.commodity] = node.inventory.get(node.commodity, 0) + gen_rate
            
            elif node.type == "transformation" and cap_factor > 0:
                # ... (existing transformation logic)
                inputs = [Cargo(id=f"in_{node.id}_{c}", commodity=UniversalLoader.get_commodity_grade(c), quantity=q) 
                         for c, q in node.inventory.items() if q > 0]
                outputs = PhysicsEngine.process(node, inputs)
                node.inventory = {}
                for out in outputs:
                    node.inventory[out.commodity.name] = out.quantity
            
            elif node.type == "retail":
                # Retail consumption (Demand Destruction + Unmet Demand)
                price_point = self.prices.get(node.commodity)
                current_price = price_point.price if price_point else 100.0
                demand = FinanceEngine.calculate_demand(node.base_demand, current_price)
                self.node_demand[node.id] = demand

                available = node.inventory.get(node.commodity, 0.0)
                fulfilled = min(available, demand)
                node.inventory[node.commodity] = max(0.0, available - fulfilled)

                unmet = max(0.0, demand - fulfilled)
                self.current_tick_unmet_demand += unmet

                self.node_unmet_demand[node.id] = unmet
                self.node_unmet_value[node.id] = unmet * current_price

                stress_factor = 0.0 if demand <= 0 else min(1.0, unmet / demand)
                self.node_revenue_loss[node.id] = node.revenue_per_day * stress_factor

        # v7.5 Sprint 5: Storage Costs & Financial Pressure
        for node in self.nodes:
            for commodity, qty in node.inventory.items():
                if qty > 0:
                    cost = qty * node.specs.storage_cost_per_unit_day
                    # For simplicity, we just deduct "ghost value" or we could link to an actor
                    # If actor owned, deduct from actor cash.
                    if node.owner_id:
                        owner = next((a for a in self.traders if a.id == node.owner_id), None)
                        if owner:
                            owner.cash -= cost

        # 4. Logistics (Vessel Movement & Routing)
        # ... existing logic ...
        self.logistics_engine.tick(self.vessels)
        
        for v in self.vessels:
            if v.status == "idle":
                # v7.5 Sprint 5: Floating Storage Logic
                # If market is in strong contango, and vessel is idle but full, consider floating storage
                if v.cargo and v.cargo.quantity > 0:
                    comm_name = v.cargo.commodity.name
                    price_point = self.prices.get(comm_name)
                    if price_point:
                        # Estimate storage incentive (very simplified)
                        # We assume future price is current price + random expected premium
                        spot = price_point.price
                        future = spot * 1.1 # Expected 10% gain in 30 days
                        cost = v.vessel_class.daily_charter_rate
                        
                        incentive = FinanceEngine.get_storage_incentive(spot, future, cost)
                        if incentive > 0:
                            v.status = "floating_storage"
                            v.is_floating_storage = True
                            v.storage_start_tick = self.tick
                            continue

                # ... existing sourcing logic ...
            
            elif v.status == "loading":
                # Load cargo from node
                node = next((n for n in self.nodes if n.id == v.destination_id), None)
                if node:
                    # Determine commodity
                    comm_name = getattr(v, 'target_commodity', node.commodity)
                    if comm_name == "Logistics": # Don't load "Logistics" commodity from waypoints
                         # Try to find a real commodity
                         real_comm = next((c for c in node.inventory.keys() if c != "Logistics"), None)
                         if real_comm: comm_name = real_comm
                         else: 
                             v.status = "idle" # Nothing to load
                             continue

                    # v6.0 Port Congestion
                    usage = port_usage.get(node.id, 0)
                    if usage >= node.specs.berth_capacity:
                        v.status = "queued"
                        continue

                    # Check for embargo (Sprint 3)
                    if self.scenario_engine.is_embargoed(node.id, comm_name, self.tick):
                        continue # Cannot load if embargoed
                    
                    qty = min(node.inventory.get(comm_name, 0), v.vessel_class.capacity)
                    if qty <= 0: continue
                    
                    v.cargo = Cargo(id=f"cargo_{v.id}_{self.tick}", commodity=UniversalLoader.get_commodity_grade(comm_name), quantity=qty)
                    node.inventory[comm_name] -= qty
                    port_usage[node.id] = usage + 1
                    
                    # Find a transformation/retail/logistic target that needs this
                    # v5.0: Target a LOGISTIC node (Port) closer to demand, or a coastal transformation node.
                    # Simplified: Find any logistic node that is NOT the current one.
                    targets = [n for n in self.nodes if n.type == "logistic" and n.id != node.id]
                    if targets:
                        target = random.choice(targets)
                        
                        # Check for embargo at destination too
                        if self.scenario_engine.is_embargoed(target.id, comm_name, self.tick):
                            pass
                        
                        v.destination_id = target.id
                        v.destination_location = target.location
                        # Calculate Route with Pathfinding (Sprint 2)
                        start_wp = self.logistics_engine.get_nearest_waypoint(v.current_location)
                        end_wp = self.logistics_engine.get_nearest_waypoint(target.location)
                        path_ids = self.logistics_engine.find_path(start_wp, end_wp, blocked_nodes, vessel=v)
                        
                        v.route_path = [self.logistics_engine.waypoints[pid]["location"] for pid in path_ids]
                        v.route_path_ids = path_ids # Store IDs for rerouting checks
                        
                        if v.route_path:
                            # Calculate accurate distance via path
                            dist_to_first_wp = self.logistics_engine.haversine_distance(v.current_location, v.route_path[0])
                            path_internal_dist = self.logistics_engine.calculate_path_distance(path_ids)
                            dist_from_last_wp = self.logistics_engine.haversine_distance(v.route_path[-1], target.location)
                            v.distance_remaining = dist_to_first_wp + path_internal_dist + dist_from_last_wp
                        else:
                            v.distance_remaining = self.logistics_engine.haversine_distance(v.current_location, target.location)

                        v.status = "transit"
            
            elif v.status == "transit":
                pass # Movement handled by logistics_engine.tick() above
            
            elif v.status == "unloading":
                # Deliver to node
                node = next((n for n in self.nodes if n.id == v.destination_id), None)
                if node and v.cargo:
                    # v6.0 Port Congestion
                    usage = port_usage.get(node.id, 0)
                    if usage >= node.specs.berth_capacity:
                        v.status = "queued"
                        continue

                    # Check for embargo (Sprint 3)
                    if self.scenario_engine.is_embargoed(node.id, v.cargo.commodity.name, self.tick):
                        # Cannot unload, vessel waits or queues (Sprint 4)
                        v.status = "queued"
                        continue

                    node.inventory[v.cargo.commodity.name] = node.inventory.get(v.cargo.commodity.name, 0) + v.cargo.quantity
                    v.cargo = None
                    v.status = "idle"
                    port_usage[node.id] = usage + 1

    def simulate_timeline(self, injections: List[Injection], days=90):
        timeline = []
        self._injections_applied = False
        self._injection_duration_days = days
        unmet_sum = revenue_sum = choke_sum = total_sum = 0.0
        max_total = 0.0
        max_day = 0
        summary = None
        for t in range(days):
            self.step(injections)
            daily_nodes = []
            for n in self.nodes:
                snapshot = n.dict()
                total_inv = sum(n.inventory.values())
                
                # v5.1 Stability Fix: Logistic nodes don't generate tension
                # Also, force 0 tension if NO injections are present (Baseline Stability)
                if n.type == "logistic" or not getattr(self, 'last_injections', {}):
                    snapshot['tension_score'] = 0
                else:
                    snapshot['tension_score'] = 100 if total_inv < 100 else (60 if total_inv < 500 else 0)
                
                demand = self.node_demand.get(n.id, 0.0)
                unmet = self.node_unmet_demand.get(n.id, 0.0)
                unmet_value = self.node_unmet_value.get(n.id, 0.0)
                revenue_loss = self.node_revenue_loss.get(n.id, 0.0)
                stress_factor = 0.0 if demand <= 0 else min(1.0, unmet / demand)

                snapshot['inventory'] = total_inv
                snapshot['demand'] = demand
                snapshot['unmet_demand'] = unmet
                snapshot['unmet_value'] = unmet_value
                snapshot['revenue_loss'] = revenue_loss
                snapshot['stress_factor'] = stress_factor
                daily_nodes.append(snapshot)

            # Hybrid Systemic Risk
            blocked_nodes = self.scenario_engine.get_blocked_nodes(self.tick)
            blocked_chokes = [
                node_id for node_id in blocked_nodes
                if node_id.startswith("choke_")
                or (node_id in self.node_index and self.node_index[node_id].subtype == "waypoint")
            ]
            blocked_chokes = list(dict.fromkeys(blocked_chokes))

            unmet_component = sum(self.node_unmet_value.values()) * settings.SYSTEMIC_RISK_UNMET_WEIGHT
            revenue_component = sum(self.node_revenue_loss.values()) * settings.SYSTEMIC_RISK_REVENUE_WEIGHT
            choke_component = 0.0
            for choke_id in blocked_chokes:
                weight = settings.SYSTEMIC_RISK_CHOKE_WEIGHTS.get(choke_id, 1.0)
                severity = self.scenario_engine.get_blockage_severity(choke_id, self.tick) or 1.0
                base_penalty = settings.SYSTEMIC_RISK_CHOKE_PENALTY * weight

                impact_penalty = 0.0
                impact = settings.SYSTEMIC_RISK_CHOKE_IMPACTS.get(choke_id, {})
                if "oil_bpd" in impact:
                    oil_price = None
                    if "Brent Crude" in self.prices:
                        oil_price = self.prices["Brent Crude"].price
                    elif "Crude Oil" in self.prices:
                        oil_price = self.prices["Crude Oil"].price
                    else:
                        oil_price = 100.0
                    flow_fraction = settings.SYSTEMIC_RISK_CHOKE_FLOW_FRACTION.get(choke_id, 0.0)
                    effective_bpd = impact["oil_bpd"] * max(0.0, 1.0 - flow_fraction)
                    impact_penalty += effective_bpd * oil_price * settings.SYSTEMIC_RISK_CHOKE_MACRO_MULTIPLIER

                choke_component += (base_penalty + impact_penalty) * severity
            systemic_risk = unmet_component + revenue_component + choke_component
            unmet_sum += unmet_component
            revenue_sum += revenue_component
            choke_sum += choke_component
            total_sum += systemic_risk
            if systemic_risk > max_total:
                max_total = systemic_risk
                max_day = self.tick

            timeline.append({
                "nodes": daily_nodes,
                "edges": self.raw_edges,
                "sea_lanes": self.sea_lanes,
                "prices": {name: p.price for name, p in self.prices.items()},
                "tick": self.tick,
                "global_loss": systemic_risk,
                "systemic_risk_breakdown": {
                    "unmet_value": unmet_component,
                    "revenue_loss": revenue_component,
                    "choke_penalty": choke_component,
                    "blocked_chokes": blocked_chokes
                },
                "unmet_demand": getattr(self, 'current_tick_unmet_demand', 0.0),
                "vessels": [v.dict() for v in self.vessels],
                "active_blockages": self.scenario_engine.get_blocked_nodes(self.tick)
            })
        if injections:
            avg_unmet = unmet_sum / days
            avg_revenue = revenue_sum / days
            avg_choke = choke_sum / days
            avg_total = total_sum / days
            inj_label = ", ".join([f"{i.type}:{i.target_id}:{i.severity}" for i in injections])
            print("[SYSTEMIC_RISK] Scenario:", inj_label)
            print(f"[SYSTEMIC_RISK] Avg Total: {avg_total:,.0f} | Avg Unmet: {avg_unmet:,.0f} | Avg Revenue: {avg_revenue:,.0f} | Avg Choke: {avg_choke:,.0f}")
            print(f"[SYSTEMIC_RISK] Peak Total: {max_total:,.0f} on Day {max_day}")
            summary = {
                "scenario": inj_label,
                "avg_total": avg_total,
                "avg_unmet": avg_unmet,
                "avg_revenue": avg_revenue,
                "avg_choke": avg_choke,
                "peak_total": max_total,
                "peak_day": max_day
            }
            for entry in timeline:
                entry["systemic_risk_summary"] = summary
        self._injection_duration_days = None
        return timeline

    def trace(self, node_id: str):
        if node_id not in self.G:
             return {"ancestors": [], "descendants": []}
        return {
            "ancestors": list(nx.ancestors(self.G, node_id)),
            "descendants": list(nx.descendants(self.G, node_id))
        }
