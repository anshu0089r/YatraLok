# YatraLok Geo-Fencing System

## 1. Overview
This module implements circular geo-fencing using the Haversine distance formula to calculate great-circle distances on Earth.

## 2. Core Components
- `haversine.py`: Calculates distance in meters between two GPS coordinates `(lat1, lon1)` and `(lat2, lon2)`.
- `zone_checker.py`: Checks if a tourist coordinate is within any circular danger/restricted zone radius and calculates nearest zone distances.
- `geofence_service.py`: State-aware service that tracks entry/exit events and suppresses duplicate continuous warnings.

## 3. Mathematical Formula (Haversine)
Given latitude $\phi_1, \phi_2$ and longitude $\lambda_1, \lambda_2$ in radians:
$$a = \sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)$$
$$c = 2 \cdot \text{atan2}\left(\sqrt{a}, \sqrt{1-a}\right)$$
$$d = R \cdot c \quad (\text{where } R = 6,371,000 \text{ meters})$$

## 4. Zone Types & Warning Logic
- `DANGER`: Triggers immediate warning.
- `RESTRICTED`: Triggers immediate warning.
- When $d \le \text{radius}$, tourist is marked `inside_zone = True` and `warning = True`.
