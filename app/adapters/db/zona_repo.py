import json
from app.domain.models.zona import Zona

class ZonaRepository:
    def __init__(self, db):
        self.db = db

    async def crear(self, nombre: str, tipo: str, feature: dict):
        geom = feature["geometry"]

        # Reordenamos para que type venga antes de coordinates
        geometry_ordered = {
            "type": geom["type"],
            "coordinates": geom["coordinates"]
        }

        query = """
        INSERT INTO zonas (nombre, tipo, geom)
        VALUES (:nombre, :tipo, ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326))
        RETURNING id, nombre, tipo, ST_AsGeoJSON(geom) AS geom;
        """
        values = {"nombre": nombre, "tipo": tipo, "geometry": json.dumps(geometry_ordered)}
        row = await self.db.fetch_one(query, values)

        row = dict(row)
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        row["feature"] = feature_out
        return Zona(id=row["id"], nombre=row["nombre"], tipo=row["tipo"], feature=feature_out)

    async def listar(self):
        query = "SELECT id, nombre, tipo, ST_AsGeoJSON(geom) AS geom FROM zonas;"
        rows = await self.db.fetch_all(query)
        zonas = []
        for row in rows:
            feature_out = {
                "type": "Feature",
                "properties": {},
                "geometry": json.loads(row["geom"])
            }
            zonas.append(Zona(
                id=row["id"],
                nombre=row["nombre"],
                tipo=row["tipo"],
                feature=feature_out
            ))
        return zonas

    async def obtener(self, id: int):
        query = "SELECT id, nombre, tipo, ST_AsGeoJSON(geom) AS geom FROM zonas WHERE id = :id;"
        row = await self.db.fetch_one(query, values={"id": id})
        if not row:
            return None
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        return Zona(
            id=row["id"],
            nombre=row["nombre"],
            tipo=row["tipo"],
            feature=feature_out
        )

    async def actualizar(self, id: int, nombre: str, tipo: str, feature: dict):
        geometry = feature["geometry"]
        query = """
        UPDATE zonas
        SET nombre = :nombre,
            tipo = :tipo,
            geom = ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326)
        WHERE id = :id
        RETURNING id, nombre, tipo, ST_AsGeoJSON(geom) AS geom;
        """
        values = {"id": id, "nombre": nombre, "tipo": tipo, "geometry": json.dumps(geometry)}
        row = await self.db.fetch_one(query, values)
        if not row:
            return None
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        return Zona(
            id=row["id"],
            nombre=row["nombre"],
            tipo=row["tipo"],
            feature=feature_out
        )

    async def eliminar(self, id: int) -> bool:
        query = "DELETE FROM zonas WHERE id = :id RETURNING id;"
        result = await self.db.fetch_one(query, values={"id": id})
        return bool(result)
