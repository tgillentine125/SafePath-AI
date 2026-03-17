from fastapi import FastAPI
import networkx as nx
from graph_builder import build_graph

app = FastAPI()

G = build_graph()

@app.get("/")
def home():
    return {"SafePath AI": "running"}

@app.get("/nodes")
def nodes():
    return {"nodes": len(G.nodes)}
