from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from data.beaches import BEACHES_DATA

def init_beaches(db: Session):
    """Initialize beaches table with predefined data"""
    # First, check if we already have beaches
    existing_beaches = db.query(models.Beach).count()
    if existing_beaches > 0:
        print("Beaches table already contains data. Skipping initialization.")
        return

    # Add each beach from our predefined data
    for beach_data in BEACHES_DATA:
        services_str = ",".join(beach_data["services"]) if beach_data["services"] else ""
        
        beach = models.Beach(
            name=beach_data["name"],
            image=beach_data["image"],
            description=beach_data["description"],
            region=beach_data["region"],
            town=beach_data["town"],
            type=beach_data["type"],
            services=services_str,
            access=beach_data["access"],
            featured=beach_data["featured"],
            latitude=beach_data["latitude"],
            longitude=beach_data["longitude"]
        )
        db.add(beach)
    
    try:
        db.commit()
        print(f"Successfully added {len(BEACHES_DATA)} beaches to the database.")
    except Exception as e:
        print(f"Error adding beaches to database: {e}")
        db.rollback()

def init_db():
    """Initialize database with all predefined data"""
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = SessionLocal()
    try:
        # Initialize beaches
        init_beaches(db)
        
        # Add more initialization functions here as needed
        # init_restaurants(db)
        # init_activities(db)
        # etc.
        
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization completed.") 