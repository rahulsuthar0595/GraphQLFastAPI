from sqlalchemy import Column, Integer, String, Text

from database.db_connection import Base


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    release_year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    image = Column(String, nullable=True)
