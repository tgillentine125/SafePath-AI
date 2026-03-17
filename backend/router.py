from __future__ import annotations

from pathlib import Path
from typing import Any

import networkx as nx

from crime_loader import load_crime_data
from risk_model import compute_node_risk, add_safety_weights


DATA_FILE = (
    Path(__file__).resolve().parents[1] / "data" / "raw" / "sample_crime_data.csv"
)


def _route_coords(G: Any, route: list[int]) -> list[dict[str, float]]:
    return [{"lat": G.nodes[n]["y"], "lon": G.nodes[n]["x"]} for n in route]


def _route_length(G: Any, route: list[int], weight: str = "length") -> float:
    total = 0.0
    for u, v in zip(route[:-1], route[1:]):
        data = G.get_edge_data(u, v) or {}
        # MultiDiGraph can contain multiple edges between u and v.
        total += min(attr.get(weight, 0.0) for attr in data.values())
    return total


def _route_node_risk(node_risk: dict[int, float], route: list[int]) -> float:
    return sum(node_risk.get(n, 0.0) for n in route)


def safe_route(
    G: Any,
    start_node: int,
    end_node: int,
    alpha: float = 0.2,
    radius_m: float = 150.0,
) -> dict:
    """Safety-weighted shortest path.

    alpha controls how much the risk score penalizes the path.
    """
    crimes = load_crime_data(DATA_FILE)
    node_risk = compute_node_risk(G, crimes, radius_m=radius_m)

    add_safety_weights(G, node_risk, alpha=alpha)
    route = nx.shortest_path(G, start_node, end_node, weight="safety_weight")

    coords = _route_coords(G, route)
    length_m = _route_length(G, route, weight="length")
    safety_weight = _route_length(G, route, weight="safety_weight")
    incident_risk = _route_node_risk(node_risk, route)

    return {
        "route": route,
        "coords": coords,
        "summary": {
            "nodes": len(route),
            "length_m": length_m,
            "safety_weight": safety_weight,
            "incident_risk_sum": incident_risk,
            "alpha": alpha,
            "radius_m": radius_m,
        },
    }
