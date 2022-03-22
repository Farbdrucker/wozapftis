import time
from typing import Optional, List

from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session

import crud
import schemas

from database import SessionLocal


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    db: Session = Depends(get_db),
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
    db_city = crud.get_city_by_name(db, city)

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

    return {"data": db_city}


@app.get("/bar/{bar}")
def get_bar(bar: str, db: Session = Depends(get_db)):
    """

    Args:
        bar:

    Returns:

    """
    data = crud.get_bar_by_name(db, bar_name=bar)
    return {"data": data}


@app.post("/bar/{bar_id}", response_model=schemas.Vote)
def create_vote_for_bar(
    bar_id: int, vote: schemas.CreateVote, db: Session = Depends(get_db)
):
    return crud.create_vote(db, vote, venue_id=bar_id)


@app.put("/bar/{bar}")
def vote_beer(bar: str, beer: str, user: Optional[str] = None):
    """

    Args:
        bar:
        beer:
        user:

    Returns:

    """

    return {"data": {"bar": bar, "beer": beer, "user": user}}
