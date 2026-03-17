from pathlib import Path
import networkx as nx

from crime_loader import load_crime_data
from risk_model import compute_node_risk, add_safety_weights

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "raw" / "sample_crime_data.csv"


def safe_route(G, start_node, end_node, alpha: float = 0.2, radius_m: float = 150.0):
    """Safety-weighted shortest path.

    alpha controls how much the risk score penalizes the path.
    """
    crimes = load_crime_data(DATA_FILE)
    node_risk = compute_node_risk(G, crimes, radius_m=radius_m)
    add_safety_weights(G, node_risk, alpha=alpha)

    return nx.shortest_path(G, start_node, end_node, weight="safety_weight")
