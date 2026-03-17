import networkx as nx

def safe_route(G,start,end):

    route = nx.shortest_path(
        G,
        start,
        end,
        weight="length"
    )

    return route
