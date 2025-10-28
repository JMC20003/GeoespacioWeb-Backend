# app/adapters/db/feature_repo.py
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from app.schemas.feature_schema import FeatureCreate
from app.core.config import database, features
from sqlalchemy import select, func
import json

class FeatureRepository:
    async def create_feature_collection(self, features_list: list[FeatureCreate]):
        values = []
        for feature in features_list:
            geom = from_shape(shape(feature.geometry), srid=4326)
            values.append({"geom": geom, "properties": feature.properties})

        if not values:
            return 0

        query = features.insert()
        await database.execute_many(query=query, values=values)
        return len(values)

    async def get_all_features(self):
        query = select(
            features.c.id,
            features.c.properties,
            func.ST_AsGeoJSON(features.c.geom).label("geom_geojson")
        )
        rows = await database.fetch_all(query)
        
        results = []
        for row in rows:
            props = {}
            if row["properties"]:
                if isinstance(row["properties"], str):
                    props = json.loads(row["properties"])
                else:
                    props = row["properties"]

            results.append({
                "id": row["id"],
                "type": "Feature",
                "geometry": json.loads(row["geom_geojson"]),
                "properties": props
            })
        return results

    async def eliminar(self, id: int) -> bool:
        query = features.delete().where(features.c.id == id).returning(features.c.id)
        result = await database.fetch_one(query)
        return result is not None

    async def obtener_por_id(self, id: int):
        query = select(
            features.c.id,
            features.c.properties,
            func.ST_AsGeoJSON(features.c.geom).label("geom_geojson")
        ).where(features.c.id == id)
        row = await database.fetch_one(query)

        if not row:
            return None

        props = {}
        if row["properties"]:
            if isinstance(row["properties"], str):
                props = json.loads(row["properties"])
            else:
                props = row["properties"]

        return {
            "id": row["id"],
            "type": "Feature",
            "geometry": json.loads(row["geom_geojson"]),
            "properties": props
        }

    async def actualizar(self, id: int, feature: FeatureCreate):
        geom = from_shape(shape(feature.geometry), srid=4326)
        query = features.update().where(features.c.id == id).values(
            geom=geom,
            properties=feature.properties
        ).returning(features.c.id, features.c.properties, func.ST_AsGeoJSON(features.c.geom).label("geom_geojson"))

        row = await database.fetch_one(query)

        if not row:
            return None

        props = {}
        if row["properties"]:
            if isinstance(row["properties"], str):
                props = json.loads(row["properties"])
            else:
                props = row["properties"]

        return {
            "id": row["id"],
            "type": "Feature",
            "geometry": json.loads(row["geom_geojson"]),
            "properties": props
        }