import time
from typing import Optional, List

from fastapi import FastAPI, Query

from schemas import Vote
from models.utils import get_id

app = FastAPI()


@app.get("/")
def index(
    city: Optional[List[str]] = Query(None), beer: Optional[List[str]] = Query(None)
):
    if city is None and beer is None:
        return {"data": "Wo Zapft Is"}

    return {"data": {"city": city, "beer": beer}}


@app.get("/{city}")
def load_city_bars(
    city: str,
    bar: Optional[List[str]] = Query(None),
    district: Optional[List[str]] = Query(None),
    beer: Optional[List[str]] = Query(None),
):
    """

    Args:
        city:
        bar:
        district:
        beer:

    Returns:

    """
    # only load data for requested city

    # filter data by districts
    if district is not None:
        pass

    # if no bar provided load all bar
    if bar is None:
        pass
    # only load provided bar
    else:
        pass

    # if beer is provided filter only provided beers
    if beer is not None:
        pass

    return {"data": {"city": city, "bar": bar, "district": district, "beer": beer}}


@app.get("/bar/{bar}")
def get_bar(bar: str):
    """

    Args:
        bar:

    Returns:

    """
    return {"data": bar}


@app.put("/bar/{bar}")
def vote_beer(bar: str, beer: str, user: Optional[str] = None):
    """

    Args:
        bar:
        beer:
        user:

    Returns:

    """
    vote = Vote(bar=bar, beer=beer, timestamp=time.time(), user=user, id=get_id())
    return {"data": vote.dict()}
