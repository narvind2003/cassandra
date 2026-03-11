from typing import List, Dict
from ..schema.cargo import Cargo
from ..schema.compliance import ComplianceProfile
from ..schema.market import Trader

class ComplianceEngine:
    @staticmethod
    def check_trade_compliance(
        buyer: Trader, 
        seller: Trader, 
        cargo: Cargo, 
        buyer_profile: ComplianceProfile,
        seller_profile: ComplianceProfile
    ) -> Dict[str, bool]:
        """
        Validates if a trade can occur based on sanctions and internal watchlists.
        Returns: {"allowed": bool, "reason": str}
        """
        
        # 1. Sanctions Check (Buyer vs Seller)
        # If the seller is sanctioned by the buyer's jurisdiction
        if buyer_profile.jurisdiction in seller_profile.sanctioned_by:
            return {"allowed": False, "reason": f"Sanctioned: Buyer {buyer_profile.jurisdiction} sanctions Seller"}

        # 2. Watchlist Check
        if seller.id in buyer_profile.internal_watch_list:
             return {"allowed": False, "reason": "Seller is on Buyer's Internal Watchlist"}

        # 3. Origin Check (The 'Form' aspect of Compliance)
        # Future: Check cargo.origin vs Buyer's prohibited origins
        # For now, we use a simple logic: If cargo is 'STS' (Ship-to-Ship) and buyer is strict
        if "sts" in cargo.id and buyer_profile.jurisdiction == "EU":
            return {"allowed": False, "reason": "High Risk: STS Transfer detected for EU Buyer"}

        return {"allowed": True, "reason": "Compliance OK"}

    @staticmethod
    def flag_high_risk_vessels(vessels: List[dict]) -> List[str]:
        """
        Returns list of vessel IDs that are engaging in suspicious behavior 
        (e.g., turning off AIS - simulated here by 'hidden' status or STS activity)
        """
        risky_vessels = []
        for v in vessels:
            if v.get('status') == 'sts_transfer':
                risky_vessels.append(v['id'])
        return risky_vessels
