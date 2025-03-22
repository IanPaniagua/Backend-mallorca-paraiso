from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Radio de la Tierra en kilómetros

    # Convertir coordenadas a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Diferencias en coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return round(distance, 2)  # Redondear a 2 decimales

def is_point_in_mallorca(latitude: float, longitude: float) -> bool:
    """
    Verifica si un punto está dentro del área aproximada de Mallorca
    """
    # Límites aproximados de Mallorca
    MALLORCA_BOUNDS = {
        'min_lat': 39.2,
        'max_lat': 40.0,
        'min_lon': 2.2,
        'max_lon': 3.5
    }

    return (MALLORCA_BOUNDS['min_lat'] <= latitude <= MALLORCA_BOUNDS['max_lat'] and
            MALLORCA_BOUNDS['min_lon'] <= longitude <= MALLORCA_BOUNDS['max_lon']) 