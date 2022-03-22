from typing import Optional, Union

from pydantic import BaseModel


class CreateBase(BaseModel):
    beer: str
    timestamp: float
    user: Optional[str]


class CreateVote(CreateBase):
    pass


class Vote(CreateBase):
    id: int
    venue_id: int


class Address(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    housenumber: Optional[Union[int, str]] = None
    postcode: Optional[int] = None


class Location(BaseModel):
    lat: float
    lon: float


class IdObject(BaseModel):
    id: str


class Amenity(BaseModel):
    osm_id: int
    name: Optional[str] = None
    amenity: Optional[str] = None


class AmenityData(IdObject, Amenity, Location, Address):
    pass
