from app.domain.models.punto import Punto
import json


class PuntoRepository:
    def __init__(self, db):
        self.db = db

    async def crear(self, nombre: str, feature: dict):
        geom = feature["geometry"]
        query = """
        INSERT INTO puntos_interes (nombre, geom)
        VALUES (:nombre, ST_SetSRID(ST_GeomFromGeoJSON(:geom), 4326))
        RETURNING id, nombre, ST_AsGeoJSON(geom) AS geom;
        """
        values = {"nombre": nombre, "geom": json.dumps(geom)}
        row = await self.db.fetch_one(query, values)
        row = dict(row)
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        row["feature"] = feature_out
        return Punto(id=row["id"], nombre=row["nombre"], feature=feature_out)

    async def listar(self):
        query = "SELECT id, nombre, ST_AsGeoJSON(geom) AS geom FROM puntos_interes;"
        rows = await self.db.fetch_all(query)
        puntos = []
        for row in rows:
            feature_out = {
                "type": "Feature",
                "properties": {},
                "geometry": json.loads(row["geom"])
            }
            puntos.append(Punto(
                id=row["id"],
                nombre=row["nombre"],
                feature=feature_out
            ))
        return puntos

    async def obtener(self, id: int):
        query = "SELECT id, nombre, ST_AsGeoJSON(geom) AS geom FROM puntos_interes WHERE id = :id;"
        row = await self.db.fetch_one(query, values={"id": id})
        if not row:
            return None
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        return Punto(
            id=row["id"],
            nombre=row["nombre"],
            feature=feature_out
        )

    async def actualizar(self, id: int, nombre: str, feature: dict):
        geom = feature["geometry"]
        query = """
        UPDATE puntos_interes
        SET nombre = :nombre,
            geom = ST_SetSRID(ST_GeomFromGeoJSON(:geom), 4326)
        WHERE id = :id
        RETURNING id, nombre, ST_AsGeoJSON(geom) AS geom;
        """
        values = {"id": id, "nombre": nombre, "geom": json.dumps(geom)}
        row = await self.db.fetch_one(query, values)
        if not row:
            return None
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        return Punto(
            id=row["id"],
            nombre=row["nombre"],
            feature=feature_out
        )

    async def eliminar(self, id: int) -> bool:
        query = "DELETE FROM puntos_interes WHERE id = :id RETURNING id;"
        result = await self.db.fetch_one(query, values={"id": id})
        return bool(result)