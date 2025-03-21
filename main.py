from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import categories, reviews, users, food, playas, restaurants, markets, heritage

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mallorca API",
    description="API REST para la información turística de Mallorca",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(playas.router, prefix="/api/v1/playas", tags=["playas"])
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