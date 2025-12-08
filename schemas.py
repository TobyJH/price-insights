from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class QueryBase(BaseModel):
    name: str
    search_term: str


class QueryCreate(QueryBase):
    pass


class Query(QueryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    ebay_item_id: str
    title: str
    category_name: Optional[str] = None
    condition: Optional[str] = None
    listing_type: Optional[str] = None
    end_time: Optional[datetime] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    shipping_cost: Optional[float] = None
    total_price_est: Optional[float] = None
    bid_count: Optional[int] = None
    selling_state: Optional[str] = None
    seller_username: Optional[str] = None
    seller_feedback_score: Optional[int] = None
    seller_positive_percent: Optional[float] = None
    view_url: Optional[str] = None


class ItemCreate(ItemBase):
    query_id: int


class Item(ItemBase):
    id: int
    query_id: int
    created_at: datetime

    class Config:
        orm_mode = True

