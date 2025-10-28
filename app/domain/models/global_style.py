
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GlobalStyle(Base):
    __tablename__ = "global_styles"

    id = Column(Integer, primary_key=True, index=True)
    fillColor = Column(String, default='#76c751')
    lineColor = Column(String, default='#76c751')
    pointColor = Column(String, default='#76c751')
    lineWidth = Column(Integer, default=2)
    pointSize = Column(Integer, default=5)
