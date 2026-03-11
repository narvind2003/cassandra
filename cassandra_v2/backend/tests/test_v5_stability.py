import pytest
from app.simulation.world import World

def test_long_term_stability():
    """
    Sprint 3 Task 3.3: Long-Run Validation.
    Ensures the world stays 'Green' (0 loss) for a full year of operation.
    """
    world = World()
    
    # Run simulation in batches to use the authoritative simulate_timeline logic
    # total 360 days (6 batches of 60)
    for batch in range(6):
        timeline = world.simulate_timeline({}, days=60)
        for day_idx, snapshot in enumerate(timeline):
            daily_loss = snapshot.get("global_loss", 0.0)
            
            if daily_loss > 0:
                 # Find culprits in snapshot
                 culprits = [n['label'] for n in snapshot['nodes'] if n['tension_score'] > 50]
                 print(f"\n[FAIL] Stability broken in Batch {batch} Day {day_idx} by {culprits}")
                 
            assert daily_loss == 0, f"World became stressed in batch {batch} day {day_idx}"

    print("\n[PASS] World remained stable for 360 days.")
