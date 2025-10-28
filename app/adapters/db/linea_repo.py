from app.domain.models.linea import Linea
import json

class LineaRepository:
    def __init__(self, db):
        self.db = db

    async def crear(self, nombre, tipo, feature):
        geom = feature["geometry"]
        query = """
        INSERT INTO rutas (nombre, tipo, geom)
        VALUES (:nombre, :tipo, ST_SetSRID(ST_GeomFromGeoJSON(:geom), 4326))
        RETURNING id, nombre, tipo, ST_AsGeoJSON(geom) AS geom;
        """
        row = await self.db.fetch_one(
            query,
            values={"nombre": nombre, "tipo": tipo, "geom": json.dumps(geom)}
        )
        row = dict(row)
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        row["feature"] = feature_out
        return Linea(id=row["id"], nombre=row["nombre"], tipo=row["tipo"], feature=feature_out)
    

    async def listar(self):
        query = "SELECT id, nombre, tipo, ST_AsGeoJSON(geom) AS geom FROM rutas;"
        rows = await self.db.fetch_all(query)
        lineas = []
        for row in rows:
            feature_out = {
                "type": "Feature",
                "properties": {},
                "geometry": json.loads(row["geom"])
            }
            lineas.append(Linea(
                id=row["id"],
                nombre=row["nombre"],
                tipo=row["tipo"],
                feature=feature_out
            ))
        return lineas

    async def obtener(self, id: int):
        query = "SELECT id, nombre, tipo, ST_AsGeoJSON(geom) AS geom FROM rutas WHERE id = :id;"
        row = await self.db.fetch_one(query, values={"id": id})
        if not row:
            return None
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        return Linea(
            id=row["id"],
            nombre=row["nombre"],
            tipo=row["tipo"],
            feature=feature_out
        )

    async def actualizar(self, id: int, nombre: str, tipo: str, feature: dict):
        geom = feature["geometry"]
        query = """
        UPDATE rutas
        SET nombre = :nombre,
            tipo = :tipo,
            geom = ST_SetSRID(ST_GeomFromGeoJSON(:geom), 4326)
        WHERE id = :id
        RETURNING id, nombre, tipo, ST_AsGeoJSON(geom) AS geom;
        """
        row = await self.db.fetch_one(
            query,
            values={
                "id": id,
                "nombre": nombre,
                "tipo": tipo,
                "geom": json.dumps(geom)
            }
        )
        if not row:
            return None
        feature_out = {
            "type": "Feature",
            "properties": {},
            "geometry": json.loads(row["geom"])
        }
        return Linea(
            id=row["id"],
            nombre=row["nombre"],
            tipo=row["tipo"],
            feature=feature_out
        )

    async def eliminar(self, id: int) -> bool:
        query = "DELETE FROM rutas WHERE id = :id RETURNING id;"
        result = await self.db.fetch_one(query, values={"id": id})
        return bool(result)