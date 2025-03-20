# Mallorca Paraíso - Backend API

API REST para la información turística de Mallorca, desarrollada con FastAPI.

## 🚀 Características

- API RESTful con FastAPI
- Base de datos PostgreSQL con SQLAlchemy
- Autenticación JWT
- Migraciones de base de datos con Alembic
- Documentación automática con Swagger UI
- Endpoints para:
  - Playas
  - Platos típicos
  - Cultura


## 📋 Prerrequisitos

- Python 3.8+
- PostgreSQL
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/mallorca-paraiso.git
cd mallorca-paraiso
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Unix o MacOS:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:


5. Ejecutar las migraciones:
```bash
alembic upgrade head
```

## 🚀 Uso

1. Iniciar el servidor:
```bash
uvicorn main:app --reload
```

2. Acceder a la documentación de la API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 Endpoints Principales

### Playas
- `GET /api/v1/playas` - Listar todas las playas
- `POST /api/v1/playas` - Crear una nueva playa
- `GET /api/v1/playas/{id}` - Obtener una playa específica
- `PUT /api/v1/playas/{id}` - Actualizar una playa
- `DELETE /api/v1/playas/{id}` - Eliminar una playa

### Platos Típicos
- `GET /api/v1/food` - Listar todos los platos
- `POST /api/v1/food` - Crear un nuevo plato
- `GET /api/v1/food/{id}` - Obtener un plato específico
- `PUT /api/v1/food/{id}` - Actualizar un plato
- `DELETE /api/v1/food/{id}` - Eliminar un plato

### Usuarios(TODO)
- `POST /api/v1/users/register` - Registrar un nuevo usuario
- `POST /api/v1/users/login` - Iniciar sesión
- `GET /api/v1/users/me` - Obtener información del usuario actual

## 🔒 Autenticación(TODO)

La API utilizará autenticación JWT. Para acceder a endpoints protegidos:
1. Obtener el token mediante el endpoint de login
2. Incluir el token en el header: `Authorization: Bearer <token>`

## 🛠️ Desarrollo

### Estructura del Proyecto

```
mallorca-paraiso/
├── alembic/              # Migraciones de base de datos
│   └── revisions/       # Migraciones de base de datos
├── routers/             # Endpoints de la API
│   ├── beaches.py       # Rutas de playas
│   ├── food.py          # Rutas de platos típicos
│   ├── users.py         # Rutas de usuarios
│   ├── categories.py    # Rutas de categorías
│   └── reviews.py       # Rutas de reseñas
├── models.py            # Modelos de base de datos
├── database.py          # Configuración de base de datos
├── main.py             # Punto de entrada de la aplicación
└── requirements.txt    # Dependencias del proyecto
```

### Crear una nueva migración

```bash
alembic revision --autogenerate -m "descripción de los cambios"
alembic upgrade head
```


## 👥 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

