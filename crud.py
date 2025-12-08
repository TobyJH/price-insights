from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas


def get_query(db: Session, query_id: int) -> Optional[models.Query]:
    return db.query(models.Query).filter(models.Query.id == query_id).first()


def get_query_by_name(db: Session, name: str) -> Optional[models.Query]:
    return db.query(models.Query).filter(models.Query.name == name).first()


def get_queries(db: Session) -> List[models.Query]:
    return db.query(models.Query).order_by(models.Query.id).all()


def create_query(db: Session, query_in: schemas.QueryCreate) -> models.Query:
    db_query = models.Query(
        name=query_in.name,
        search_term=query_in.search_term,
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_items_for_query(db: Session, query_id: int) -> List[models.Item]:
    return (
        db.query(models.Item)
            .filter(models.Item.query_id == query_id)
            .order_by(models.Item.end_time.desc())
            .all()
    )


def create_item(db: Session, item_in: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(**item_in.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

