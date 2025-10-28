from fastapi import FastAPI
from app.core.config import database
from app.adapters.api import punto_api 
from app.adapters.api import linea_api 
from app.adapters.api import zona_api 
from app.adapters.api import feature_api
from app.adapters.api import global_style_api 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Backend Geoespacial")

app.include_router(punto_api.router)
app.include_router(linea_api.router)
app.include_router(zona_api.router)
app.include_router(feature_api.router)
app.include_router(global_style_api.router)

@app.on_event("startup")
async def startup():
    await database.connect()
    print("Conectado a la BD")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("Desconectado de la BD")



# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # si usas un frontend con Vite/React/Angular
    "http://localhost:3071",
    "http://127.0.0.1:5500",
    "file://",                # para abrir index.html directamente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],       # Permitir todos los métodos: GET, POST, etc.
    allow_headers=["*"],       # Permitir todos los headers
)