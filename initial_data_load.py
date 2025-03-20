from scraper import MallorcaScraper
from database import SessionLocal
from models import Beach, Monument, Food

def load_initial_data():
    db = SessionLocal()
    scraper = MallorcaScraper()
    
    try:
        # Cargar datos de playas
        print("Cargando datos de playas...")
        beaches_data = scraper.scrape_beaches()
        for beach_data in beaches_data:
            beach = Beach(**beach_data)
            db.add(beach)
        
        # Cargar datos de monumentos
        print("Cargando datos de monumentos...")
        monuments_data = scraper.scrape_monuments()
        for monument_data in monuments_data:
            monument = Monument(**monument_data)
            db.add(monument)
        
        # Cargar datos de comida
        print("Cargando datos de gastronomía...")
        food_data = scraper.scrape_food()
        for food_item in food_data:
            food = Food(**food_item)
            db.add(food)
        
        # Guardar todos los cambios
        db.commit()
        print("Datos iniciales cargados exitosamente!")
        
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_initial_data() 