from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import categories, reviews, users, food, beaches, restaurants, markets, heritage, locations

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mallorca API",
    description="API REST para la información turística de Mallorca",
    version="1.0.0"
)

# Configurar CORS
origins = [
    "http://localhost:3000",    # React default port
    "http://localhost:5173",    # Vite default port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(locations.router, prefix="/api/v1", tags=["locations"])
app.include_router(beaches.router, prefix="/api/v1/beaches", tags=["beaches"])
app.include_router(food.router, prefix="/api/v1/food", tags=["food"])
app.include_router(restaurants.router, prefix="/api/v1/restaurants", tags=["restaurants"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(markets.router, prefix="/api/v1/markets", tags=["markets"])
app.include_router(heritage.router, prefix="/api/v1/heritage", tags=["heritage"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Mallorca",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 