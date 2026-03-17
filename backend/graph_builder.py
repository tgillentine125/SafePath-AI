import osmnx as ox

def build_graph():

    place = "Winston-Salem, North Carolina, USA"

    G = ox.graph_from_place(
        place,
        network_type="walk"
    )

    return G
