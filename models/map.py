import secrets
from enum import Enum
from random import randrange
from typing import NamedTuple, Optional, Union, Dict, List

from pydantic.main import BaseModel
from sqlalchemy.testing.schema import Table

from maphash import maphash
from printing import print
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim

from sqlalchemy import create_engine, ForeignKey, Float, insert, MetaData
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

JsonValue = Union[str, float, int]

def get_id():
    return secrets.token_urlsafe(6)


class Amenity(str, Enum):
    bar = 'bar'
    pub = 'pub'
    restaurant = 'restaurant'


class Address(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    housenumber: Optional[Union[int, str]] = None
    postcode: Optional[int] = None


class AmenityData(BaseModel):
    id: str
    osm_id: int
    lat: float
    lon: float
    address: Address
    name: Optional[str] = None
    amenity: Optional[str] = None


def extract_amenity(data: Dict[str, Union[Dict[str, JsonValue], JsonValue]]) -> AmenityData:
    lat = data['lat']
    lon = data['lon']
    osm_id = data['id']

    try:
        addresss = Address(**{field: data['tags'].get(f'addr:{field}', None) for field in list(Address.schema()['properties'])})
    except:
        print(data['tags'])
        raise ValueError

    amenity = data['tags'].get('amenity', None)
    name = data['tags'].get('name')

    id_ = get_id()

    return AmenityData(id=id_, lat=lat, lon=lon, osm_id=osm_id, amenity=amenity, name=name, address=addresss)


def flatten_amenity(amenity: AmenityData) -> Dict[str, JsonValue]:
    data = amenity.dict()
    address = data.pop('address')
    return {**data, **address}



# print(result.toJSON())
# print(result.countElements())

venues_db_uri = 'sqlite:////Users/lukassanner/Documents/Private/Python/wozapftis/models/db/venues.db'
engine = create_engine(f'{venues_db_uri}', echo=True)
meta = MetaData()

Base = declarative_base()

vanues = Table(
    'venues', meta,
    Column('id', String, primary_key=True),
    Column('name', String),
    Column('lat', Float),
    Column('lon', Float),
    Column('country', String),
    Column('city', String),
    Column('street', String),
    Column('housenumber', String),
    Column('postcode', Integer),
    Column('amenity', String)
)

meta.create_all(engine)

ins = vanues.insert()
conn = engine.connect()

nominatim = Nominatim()
hannover = nominatim.query('Hannover')

area_id = hannover.areaId()

overpass = Overpass()


def scrape_for_amenity(amenity: str) -> List[AmenityData]:
    query = overpassQueryBuilder(area=area_id, elementType='node', selector=f'"amenity"="{amenity}"', out='center')
    result = overpass.query(query)

    venue_datas = [extract_amenity(r) for r in result.toJSON()['elements']]

    return venue_datas


datas = scrape_for_amenity('bar') + scrape_for_amenity('restaurant') + scrape_for_amenity('pub')

ids = set()
for d in datas:
    if d.id not in ids:
        ids.update(set(d.id))
        print(d)

        conn.execute(ins, [flatten_amenity(d)])

