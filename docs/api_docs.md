# API Documentation

## Base URL
`http://localhost:8000`

## Endpoints

### GET `/`
Health check.

**Response**
```json
{"SafePath AI": "running"}
```

### GET `/nodes`
Graph size summary.

**Response**
```json
{"nodes": 12345, "edges": 23456}
```

### GET `/route`
Compute a safer walking route.

**Query parameters**
- `start_lat` (float)
- `start_lon` (float)
- `end_lat` (float)
- `end_lon` (float)
- `alpha` (float, optional) safety weight multiplier (default handled by backend)
- `radius_m` (float, optional) incident-to-node radius in meters

**Response**
```json
{
  "start_node": 123,
  "end_node": 456,
  "alpha": 0.2,
  "radius_m": 150,
  "route_nodes": [123, 789, 456]
}
```

## Notes
- Routing uses NetworkX shortest path with edge weight `safety_weight`.
- `safety_weight` = `length + alpha * edge_risk` where `edge_risk` is derived from nearby incidents.
- OSMnx must be able to download/build the Winston-Salem walkable graph.
