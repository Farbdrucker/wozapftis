from sqlalchemy.orm import Session

from schemas.vote import Vote
from . import models, schemas


def get_venue(db: Session, venue_id: int):
    """

    Args:
        db:
        venue_id:

    Returns:

    """
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()


def get_venues(db: Session, skip: int = 0, limit: int = 100):
    """

    Args:
        db:
        skip:
        limit:

    Returns:

    """
    return db.query(models.Venue).offset(skip).limit(limit).all()


def create_vote(db: Session, vote: schemas.vote.CreateVote, venue_id: int):
    """

    Args:
        db:
        vote:

    Returns:

    """
    db_vote = models.Vote(**vote.dict(), venue_id=venue_id)
    db.add(db_vote)
    db.commit()
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_votes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vote).offset(skip).limit(limit).all()


def get_votes_for_venue(db: Session, venue):
    pass
