import math
import os
import random

import requests

def predict_delivery_time(distance_km, prep_time_min,
                          traffic='moderate',
                          weather='clear',
                          vehicle='bike',
                          time_of_day='afternoon'):

    effective_speed = 30
    travel_time = (distance_km / effective_speed) * 60
    total = prep_time_min + travel_time + 5

    return {
        "total_minutes": round(total),
        "range_low": round(total - 5),
        "range_high": round(total + 5)
    }


def simulate_maps_distance(origin, destination):
    """Demo distance without Google APIs; returns shape expected by the web UI."""
    o = (origin or "").strip()
    d = (destination or "").strip()
    n = max(1, len(o) + len(d))
    distance_km = round(2.5 + (n % 180) / 10.0, 1)
    duration_min = max(5, int(distance_km * 3.2))
    return {
        "distance_km": distance_km,
        "duration_min": duration_min,
        "status": "SIMULATED",
    }


def real_maps_distance(origin, destination):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    url     = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params  = {
        'origins':      origin,
        'destinations': destination,
        'key':          api_key,
        'units':        'metric',
    }
    r       = requests.get(url, params=params).json()
    elem    = r['rows'][0]['elements'][0]
    return {
        'distance_km':  elem['distance']['value'] / 1000,
        'duration_min': elem['duration']['value'] // 60,
        'status': 'OK',
    }
