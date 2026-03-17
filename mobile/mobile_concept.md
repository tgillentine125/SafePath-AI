# Mobile Concept

## Goal & Target User
A mobile-first companion to the SafePath API that surfaces safer walking routes and safety context for students in Winston-Salem, with minimal friction.

## MVP Feature Set (V0)
- **Search & route**: enter start/end (address, campus building, current location)
- **Safer route computation**: call FastAPI `/route`
- **Route details**: length, node count, safety weight, incident count
- **Heatmap overlay**: crime density heatmap toggle
- **Feedback**: report “unsafe experience” pins (stored locally first)

## Screens (suggested)
1. **Launch/Home**
2. **Route planner** (start/end selectors, alpha/radius sliders)
3. **Route detail** (polyline, stats, step list)
4. **Map-only mode** (heatmap + incidents)
5. **Settings** (privacy, cache, data refresh)

## API Integration
Backend endpoints consumed:
- `GET /nodes` for sanity checks
- `GET /route?start_lat=...&start_lon=...&end_lat=...&end_lon=...&alpha=...&radius_m=...`

Expect the response to include:
- node id list
- optional (lat, lon) coordinate sequence
- length/safety summary

## Tech Stack Options
- React Native (Expo) or Flutter
- HTTP client: fetch/axios
- Map: Mapbox/Leaflet wrapper, or native Google Maps SDK

## Offline & Caching
- Cache last N routes by `(start,end,alpha,radius_m)` key
- Sync incidents periodically (not continuously)
- degrade gracefully if graph cannot load

## Privacy & Safety
- default: no background tracking and no location history stored on device
- anonymize feedback pins before upload (strip timestamps/precision)

## Roadmap (V1)
- notifications for nearby incidents (opt-in)
- crowdsourced “unsafe zones” weighting
- campus-specific POI routing (classrooms, parking)
- accessibility routing constraints (lighting, sidewalks)
