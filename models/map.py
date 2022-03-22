from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, Float, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.testing.schema import Table

from models.scrape_osm import scrape_for_amenity, scrape_for_amenities
from printing import print, progress

VANUES_DB = "sqlite:////Users/lukassanner/Documents/Private/Python/wozapftis/models/db/venues.db"


@progress
def _venues_table(engine: Engine):
    meta = MetaData()
    Base = declarative_base()
    meta.create_all(engine)

    venues = Table(
        "venues",
        meta,
        Column("id", String, primary_key=True),
        Column("name", String),
        Column("lat", Float),
        Column("lon", Float),
        Column("country", String),
        Column("city", String),
        Column("street", String),
        Column("housenumber", String),
        Column("postcode", Integer),
        Column("amenity", String),
    )

    return venues


@progress
def get_amenity_engine() -> Engine:
    engine = create_engine(VANUES_DB, echo=False)
    return engine


def _init_db(init_city: str = "Hannover", *amenities: str):
    from OSMPythonTools.overpass import Overpass
    from OSMPythonTools.nominatim import Nominatim

    engine = get_amenity_engine()
    venues = _venues_table(engine)
    ins = venues.insert()
    conn = engine.connect()

    nominatim = Nominatim()
    overpass = Overpass()
    hannover = nominatim.query(init_city)
    data = scrape_for_amenities(
        *amenities, area_id=hannover.areaId(), overpass=overpass
    )

    @progress
    def insert_data(data_):
        ids = set()
        for d in data_:
            if d.id not in ids:
                ids.update(set(d.id))
                print(d)

                conn.execute(ins, [d.dict()])

    insert_data(data)


if __name__ == "__main__":
    _init_db("Hannover", "bar", "pub", "restaurant")
