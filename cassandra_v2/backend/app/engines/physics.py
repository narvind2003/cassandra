import random
from typing import List, Optional
from ..schema.cargo import Cargo
from ..schema.commodity import CommodityGrade
from ..schema.node import Node, Recipe

class PhysicsEngine:
    @staticmethod
    def blend(cargoes: List[Cargo], new_id: str) -> Cargo:
        """
        Blends multiple cargoes into one.
        Properties are calculated as weighted averages.
        """
        if not cargoes:
            raise ValueError("No cargoes to blend")
            
        total_quantity = sum(c.quantity for c in cargoes)
        if total_quantity == 0:
            return Cargo(id=new_id, commodity=cargoes[0].commodity, quantity=0)

        # Base commodity info from the first cargo
        base_commodity = cargoes[0].commodity
        new_properties = {}
        
        # Calculate weighted average for all numeric properties
        # Assumes all cargoes have the same property keys for now
        all_keys = set()
        for c in cargoes:
            all_keys.update(c.commodity.properties.keys())
            
        for key in all_keys:
            weighted_sum = sum(c.commodity.properties.get(key, 0.0) * c.quantity for c in cargoes)
            new_properties[key] = weighted_sum / total_quantity

        new_grade = CommodityGrade(
            name=f"Blended {base_commodity.name}",
            category=base_commodity.category,
            properties=new_properties
        )
        
        return Cargo(
            id=new_id,
            commodity=new_grade,
            quantity=total_quantity,
            value_per_unit=sum(c.value_per_unit * c.quantity for c in cargoes) / total_quantity
        )

    @staticmethod
    def validate_constraints(node: Node, cargo: Cargo) -> bool:
        """
        Checks if a cargo meets the node's input specifications.
        Returns True if accepted, False if rejected (The Quality Cliff).
        """
        # 1. Check Category Allow-list
        if node.specs.allowed_inputs and cargo.commodity.category not in node.specs.allowed_inputs:
             # Relaxed check: if list is empty, allow all. If not, must match.
             # Also allow if the exact name matches
             if cargo.commodity.name not in node.specs.allowed_inputs:
                 return False

        # 2. Check Chemical Constraints (e.g., Sulfur < 0.5)
        for prop, limits in node.specs.constraints.items():
            val = cargo.commodity.properties.get(prop, 0.0)
            if "max" in limits and val > limits["max"]:
                return False
            if "min" in limits and val < limits["min"]:
                return False
                
        return True

    @staticmethod
    def process(node: Node, inputs: List[Cargo]) -> List[Cargo]:
        """
        Executes transformation recipes.
        Supports Substitution Logic (Sprint 7): Tries recipes in order.
        """
        if not node.recipes:
            return inputs

        outputs = []
        input_map = {c.commodity.name: c for c in inputs}
        
        # Track if any recipe was successfully executed
        any_success = False
        
        # Recipes are tried in order of appearance (priority)
        for recipe in node.recipes:
            can_run = True
            max_batches = float('inf')
            
            # Check if all inputs for this SPECIFIC recipe are available
            for commodity_name, required_amount in recipe.inputs.items():
                if commodity_name not in input_map or input_map[commodity_name].quantity < required_amount:
                    can_run = False
                    break
                batches = input_map[commodity_name].quantity / required_amount
                max_batches = min(max_batches, batches)
            
            if can_run and max_batches > 0:
                # Execute this recipe and stop (don't run multiple different recipes in one tick)
                # or we could allow multiple. For Cassandra, one primary mode per node per tick is cleaner.
                for out_name, out_ratio in recipe.outputs.items():
                    new_grade = CommodityGrade(
                        name=out_name,
                        category="Processed",
                        properties={}
                    )
                    
                    outputs.append(Cargo(
                        id=f"out_{node.id}_{out_name}_{random.randint(0,1000)}",
                        commodity=new_grade,
                        quantity=out_ratio * max_batches,
                        value_per_unit=100.0
                    ))
                
                # Consume inputs
                for commodity_name, required_amount in recipe.inputs.items():
                    input_map[commodity_name].quantity -= required_amount * max_batches
                    if input_map[commodity_name].quantity <= 0:
                        del input_map[commodity_name]
                
                any_success = True
                break # We found a valid recipe (Substitution successful)
                    
        # Return remaining inputs + new outputs
        outputs.extend(input_map.values())
        return outputs
