import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.config import database
from app.adapters.api import punto_api 
from app.adapters.api import linea_api 
from app.adapters.api import zona_api 
from app.adapters.api import feature_api
from app.adapters.api import global_style_api 




app = FastAPI(
    title="Geoespacial API",
    description="API para gestión de features geoespaciales",
    version="1.0.0"
)

# Configuración de CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4033").split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Geoespacial API is running", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

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
