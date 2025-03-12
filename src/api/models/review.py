from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from database.db_connection import Base


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)

    movie = relationship("Movie", back_populates="reviews")  # Connect to Movie
