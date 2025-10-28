from databases import Database
import os
from dotenv import load_dotenv
from sqlalchemy import MetaData
from app.domain.models.feature import Feature
from app.domain.models.global_style import GlobalStyle

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = Database(DATABASE_URL)

metadata = MetaData()

features = Feature.__table__
global_styles = GlobalStyle.__table__
