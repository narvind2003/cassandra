from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from app.simulation.world import World
from app.simulation.scenarios import Injection
from app.simulation.playbook import Playbook
from app.services.news_ingestor import NewsIngestor

# Initialize World (Loads Data & Physics)
world = World()

app = FastAPI(
    title="Project Cassandra",
    description="The Omniscient Twin - Global Supply Chain Knowledge Engine",
    version="7.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/news")
def get_news():
    return NewsIngestor.fetch_latest_news()

@app.get("/api/actors")
def get_actors():
    return world.actors

@app.get("/api/actors/{actor_id}")
def get_actor(actor_id: str):
    actor = next((a for a in world.actors if a.id == actor_id), None)
    if not actor:
        return {"error": "Actor not found"}
    return actor

@app.get("/api/playbook")
def get_playbook():
    return Playbook.get_all()

@app.get("/api/graph")
def get_graph():
    return world.simulate_timeline([], days=1)[0]

@app.post("/api/simulate_timeline")
def post_sim_timeline(injections: List[Injection]):
    return world.simulate_timeline(injections)

@app.get("/api/trace/{node_id}")
def get_trace(node_id: str):
    return world.trace(node_id)

@app.post("/api/reset")
def reset_world():
    global world
    world = World()
    return {"status": "World Reset", "tick": world.tick}
