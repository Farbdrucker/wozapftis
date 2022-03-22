from typing import Optional, Union, Dict

from pydantic import BaseModel
from rich import inspect

from printing import print


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


if __name__ == "__main__":
    print(inspect((Location)))
    print(inspect(IdObject))
    print(inspect(Address))
    print(inspect(AmenityData))
