import sys
import os

# Añadir el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Zone, Locality, LocalityType
from database import SQLALCHEMY_DATABASE_URL

# Crear conexión a la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Datos de zonas
zones_data = [
    "Palma de Mallorca",
    "Sierra de Tramontana",
    "Levante",
    "Migjorn",
    "Llano de Mallorca",
    "Raiguer"
]

# Datos de localidades con su zona correspondiente
localities_data = [
    ("Palma de Mallorca", "Palma", "Palma de Mallorca", "ciudad"),
    ("Valldemossa", "Valldemossa", "Sierra de Tramontana", "pueblo"),
    ("Deià", "Deià", "Sierra de Tramontana", "pueblo"),
    ("Sóller", "Sóller", "Sierra de Tramontana", "pueblo"),
    ("Fornalutx", "Fornalutx", "Sierra de Tramontana", "pueblo"),
    ("Escorca", "Escorca", "Sierra de Tramontana", "pueblo"),
    ("Banyalbufar", "Banyalbufar", "Sierra de Tramontana", "pueblo"),
    ("Estellencs", "Estellencs", "Sierra de Tramontana", "pueblo"),
    ("Esporles", "Esporles", "Sierra de Tramontana", "pueblo"),
    ("Bunyola", "Bunyola", "Sierra de Tramontana", "pueblo"),
    ("Puigpunyent", "Puigpunyent", "Sierra de Tramontana", "pueblo"),
    ("Andratx", "Andratx", "Sierra de Tramontana", "pueblo"),
    ("Calvià", "Calvià", "Sierra de Tramontana", "pueblo"),
    ("Pollença", "Pollença", "Sierra de Tramontana", "pueblo"),
    ("Alcúdia", "Alcúdia", "Sierra de Tramontana", "pueblo"),
    ("Artà", "Artà", "Levante", "pueblo"),
    ("Capdepera", "Capdepera", "Levante", "pueblo"),
    ("Son Servera", "Son Servera", "Levante", "pueblo"),
    ("Manacor", "Manacor", "Levante", "ciudad"),
    ("Sant Llorenç des Cardassar", "Sant Llorenç des Cardassar", "Levante", "pueblo"),
    ("Felanitx", "Felanitx", "Migjorn", "pueblo"),
    ("Santanyí", "Santanyí", "Migjorn", "pueblo"),
    ("Campos", "Campos", "Migjorn", "pueblo"),
    ("Ses Salines", "Ses Salines", "Migjorn", "pueblo"),
    ("Llucmajor", "Llucmajor", "Migjorn", "ciudad"),
    ("Petra", "Petra", "Llano de Mallorca", "pueblo"),
    ("Santa Margalida", "Santa Margalida", "Llano de Mallorca", "pueblo"),
    ("Muro", "Muro", "Llano de Mallorca", "pueblo"),
    ("Sineu", "Sineu", "Llano de Mallorca", "pueblo"),
    ("Porreres", "Porreres", "Llano de Mallorca", "pueblo"),
    ("Montuïri", "Montuïri", "Llano de Mallorca", "pueblo"),
    ("Vilafranca de Bonany", "Vilafranca de Bonany", "Llano de Mallorca", "pueblo"),
    ("Ariany", "Ariany", "Llano de Mallorca", "pueblo"),
    ("Lloret de Vistalegre", "Lloret de Vistalegre", "Llano de Mallorca", "pueblo"),
    ("Costitx", "Costitx", "Llano de Mallorca", "pueblo"),
    ("Sant Joan", "Sant Joan", "Llano de Mallorca", "pueblo"),
    ("Maria de la Salut", "Maria de la Salut", "Llano de Mallorca", "pueblo"),
    ("Algaida", "Algaida", "Llano de Mallorca", "pueblo"),
    ("Llubí", "Llubí", "Llano de Mallorca", "pueblo"),
    ("Inca", "Inca", "Raiguer", "ciudad"),
    ("Lloseta", "Lloseta", "Raiguer", "pueblo"),
    ("Binissalem", "Binissalem", "Raiguer", "pueblo"),
    ("Consell", "Consell", "Raiguer", "pueblo"),
    ("Santa Maria del Camí", "Santa Maria del Camí", "Raiguer", "pueblo"),
    ("Marratxí", "Marratxí", "Raiguer", "pueblo"),
    ("Selva", "Selva", "Raiguer", "pueblo"),
    ("Mancor de la Vall", "Mancor de la Vall", "Raiguer", "pueblo"),
    ("Búger", "Búger", "Raiguer", "pueblo"),
    ("Campanet", "Campanet", "Raiguer", "pueblo"),
    ("Sa Pobla", "Sa Pobla", "Raiguer", "pueblo"),
    ("Alaró", "Alaró", "Raiguer", "pueblo"),
    ("Santa Eugènia", "Santa Eugènia", "Raiguer", "pueblo")
]

def populate_zones_and_localities():
    try:
        # Primero, crear las zonas
        zones = {}
        for zone_name in zones_data:
            zone = Zone(name=zone_name)
            db.add(zone)
            db.flush()  # Para obtener el ID generado
            zones[zone_name] = zone.id
        
        # Luego, crear las localidades
        for locality_name, municipality_name, zone_name, locality_type in localities_data:
            locality = Locality(
                name=locality_name,
                type=locality_type,
                zone_id=zones[zone_name]
            )
            db.add(locality)
        
        db.commit()
        print("Datos insertados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"Error al insertar datos: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_zones_and_localities() 