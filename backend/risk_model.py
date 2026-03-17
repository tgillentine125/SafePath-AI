from __future__ import annotations

import numpy as np
from sklearn.neighbors import BallTree
import geopandas as gpd


def compute_node_risk(G, crimes_gdf: gpd.GeoDataFrame, radius_m: float = 150.0) -> dict:
    """Compute a risk score for each node based on nearby incidents.

    Risk score = sum(severity) of incidents within `radius_m` of the node.
    """
    # Build nodes GeoDataFrame
    nodes = (
        gpd.GeoDataFrame(
            {
                "node": list(G.nodes()),
                "x": [G.nodes[n]["x"] for n in G.nodes()],
                "y": [G.nodes[n]["y"] for n in G.nodes()],
            },
            geometry=gpd.points_from_xy(
                [G.nodes[n]["x"] for n in G.nodes()],
                [G.nodes[n]["y"] for n in G.nodes()],
            ),
            crs="EPSG:4326",
        )
        .to_crs(3857)
    )

    crimes = crimes_gdf.to_crs(3857)

    # BallTree over node coordinates
    node_coords = np.vstack([nodes.geometry.x.values, nodes.geometry.y.values]).T
    tree = BallTree(node_coords)

    node_risk = {n: 0.0 for n in G.nodes()}

    for _, row in crimes.iterrows():
        pt = row.geometry
        severity = float(row.get("severity", 1.0))
        # Query node indices within radius
        ind = tree.query_radius([[pt.x, pt.y]], r=radius_m)[0]
        for i in ind:
            node_id = nodes.iloc[i]["node"]
            node_risk[node_id] += severity

    return node_risk


def add_safety_weights(G, node_risk: dict, alpha: float = 1.0):
    """Attach a safety_weight to each edge: length + alpha * risk."""
    for u, v, data in G.edges(data=True):
        length = float(data.get("length", 1.0))
        edge_risk = 0.5 * (node_risk.get(u, 0.0) + node_risk.get(v, 0.0))
        data["safety_weight"] = length + alpha * edge_risk

    # store for later inspection
    for n, r in node_risk.items():
        G.nodes[n]["risk"] = r

    return G
