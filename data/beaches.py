BEACHES_DATA = [
    {
        "name": "Playa de Alcúdia",
        "image": "https://mallorca-paraiso-web.s3.eu-central-1.amazonaws.com/beaches/alcudia.jpg",
        "description": "Una de las playas más largas de Mallorca, con aguas cristalinas y arena blanca.",
        "region": "Norte",
        "town": "Alcúdia",
        "type": "arena",
        "services": ["parking", "duchas", "socorrista", "restaurantes", "hamacas", "deportes_acuaticos"],
        "access": "fácil",
        "featured": True,
        "latitude": 39.8353,
        "longitude": 3.1190
    },
    {
        "name": "Cala Mesquida",
        "image": "https://mallorca-paraiso-web.s3.eu-central-1.amazonaws.com/beaches/cala-mesquida.jpg",
        "description": "Hermosa cala rodeada de dunas y pinos, ideal para el windsurf.",
        "region": "Este",
        "town": "Capdepera",
        "type": "cala",
        "services": ["parking", "duchas", "socorrista", "restaurante"],
        "access": "fácil",
        "featured": True,
        "latitude": 39.7444,
        "longitude": 3.4361
    },
    {
        "name": "Es Trenc",
        "image": "https://mallorca-paraiso-web.s3.eu-central-1.amazonaws.com/beaches/es-trenc.jpg",
        "description": "Playa virgen con aspecto caribeño, famosa por sus aguas turquesas.",
        "region": "Sur",
        "town": "Campos",
        "type": "arena",
        "services": ["parking", "chiringuitos", "hamacas"],
        "access": "medio",
        "featured": True,
        "latitude": 39.3497,
        "longitude": 2.9817
    },
    {
        "name": "Cala Deià",
        "image": "https://mallorca-paraiso-web.s3.eu-central-1.amazonaws.com/beaches/cala-deia.jpg",
        "description": "Pequeña cala rocosa con aguas cristalinas, perfecta para el snorkel.",
        "region": "Oeste",
        "town": "Deià",
        "type": "cala",
        "services": ["restaurante"],
        "access": "difícil",
        "featured": True,
        "latitude": 39.7469,
        "longitude": 2.6494
    },
    {
        "name": "Playa de Palma",
        "image": "https://mallorca-paraiso-web.s3.eu-central-1.amazonaws.com/beaches/playa-palma.jpg",
        "description": "Extensa playa urbana con todos los servicios y entretenimiento.",
        "region": "Bahía de Palma",
        "town": "Palma",
        "type": "arena",
        "services": ["parking", "duchas", "socorrista", "restaurantes", "hamacas", "deportes_acuaticos", "wifi"],
        "access": "fácil",
        "featured": True,
        "latitude": 39.5198,
        "longitude": 2.7458
    },
    {
        "name": "Cala Varques",
        "image": "https://mallorca-paraiso-web.s3.eu-central-1.amazonaws.com/beaches/cala-varques.jpg",
        "description": "Cala virgen de difícil acceso pero de extraordinaria belleza.",
        "region": "Este",
        "town": "Manacor",
        "type": "cala",
        "services": [],
        "access": "difícil",
        "featured": True,
        "latitude": 39.5007,
        "longitude": 3.2977
    }
]

# Tipos de playas disponibles
BEACH_TYPES = [
    "arena",    # Playas de arena
    "cala",     # Calas
    "roca",     # Playas rocosas
    "virgen"    # Playas vírgenes
]

# Servicios posibles en las playas
BEACH_SERVICES = [
    "parking",
    "duchas",
    "socorrista",
    "restaurantes",
    "chiringuitos",
    "hamacas",
    "sombrillas",
    "deportes_acuaticos",
    "wifi",
    "acceso_discapacitados",
    "zona_infantil",
    "punto_informacion"
]

# Regiones de Mallorca
REGIONS = [
    "Norte",
    "Sur",
    "Este",
    "Oeste",
    "Bahía de Palma",
    "Sierra de Tramuntana"
] 