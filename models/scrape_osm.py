from typing import List, Dict, Union

from OSMPythonTools.nominatim import Nominatim, NominatimResult
from OSMPythonTools.overpass import overpassQueryBuilder

from schemas import AmenityData, Address

from schemas import JsonValue
from models.utils import get_id
from printing import print

from OSMPythonTools.overpass import Overpass


def extract_amenity(
    data: Dict[str, Union[Dict[str, JsonValue], JsonValue]]
) -> AmenityData:
    lat = data["lat"]
    lon = data["lon"]
    osm_id = data["id"]

    try:
        addresss = Address(
            **{
                field: data["tags"].get(f"addr:{field}", None)
                for field in list(Address.schema()["properties"])
            }
        )
    except:
        print(data["tags"])
        raise ValueError

    amenity = data["tags"].get("amenity", None)
    name = data["tags"].get("name")

    id_ = get_id()

    return AmenityData(
        id=id_,
        lat=lat,
        lon=lon,
        osm_id=osm_id,
        amenity=amenity,
        name=name,
        **addresss.dict(),
    )


def scrape_for_amenity(
    amenity: str, area_id: int, overpass: Overpass
) -> List[AmenityData]:
    query = overpassQueryBuilder(
        area=area_id,
        elementType="node",
        selector=f'"amenity"="{amenity}"',
        out="center",
    )
    result = overpass.query(query)

    venue_datas = [extract_amenity(r) for r in result.toJSON()["elements"]]

    return venue_datas


def scrape_for_amenities(
    *amenities: str, area_id: int, overpass: Overpass
) -> List[AmenityData]:
    return sum(
        [
            scrape_for_amenity(amenity, area_id, overpass=overpass)
            for amenity in list(amenities)
        ],
        [],
    )


def get_city_nominatim(city: str) -> NominatimResult:
    nominatim = Nominatim()
    return nominatim.query(city)


if __name__ == "__main__":
    overpass = Overpass()

    hannover = get_city_nominatim("Hannover")

    area_id = hannover.areaId()

    bars = scrape_for_amenity("bar", area_id, overpass)

    print("overpass", type(overpass))
    print("get_city_nominatim", type(hannover))
    print("areaId", type(area_id))

    print("bars", type(bars))
    print("bars[0]", type(bars[0]))

    print(bars[:10])
