from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    osm_id = Column(Integer)
    name = Column(String, index=True)
    lat = Column(Float)
    lon = Column(Float)
    country = Column(String)
    street = Column(String)
    housenumber = Column(String)
    postcode = Column(Integer)
    venue = Column(Integer)

    votes = relationship("Vote", back_populate="venue")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    beer = Column(String)
    timestamp = Column(Float)
    user = Column(String)
    venue_id = Column(Integer, ForeignKey("venues.id"))
    venue = relationship("Venue", back_populates="votes")
