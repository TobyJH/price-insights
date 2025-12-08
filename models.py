from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    search_term = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("Item", back_populates="query")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    ebay_item_id = Column(String, unique=True, index=True, nullable=False)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)

    # Basic info
    title = Column(String, nullable=False)
    category_name = Column(String)
    condition = Column(String)
    listing_type = Column(String)
    end_time = Column(DateTime)

    # Pricing
    price = Column(Float)
    currency = Column(String(10))
    shipping_cost = Column(Float)
    total_price_est = Column(Float)

    # Auction/meta
    bid_count = Column(Integer)
    selling_state = Column(String)

    # Seller
    seller_username = Column(String)
    seller_feedback_score = Column(Integer)
    seller_positive_percent = Column(Float)
    view_url = Column(String)

    # Parsed / structured fields
    brand = Column(String)
    model = Column(String)      # e.g. "Microlight Alpine"
    variant = Column(String)    # e.g. "Hooded", "Vest"
    gender = Column(String)     # e.g. "Men", "Women", "Unisex"
    size = Column(String)       # e.g. "M", "L", "XL"
    colour = Column(String)     # free-text colour, if we ever parse it

    created_at = Column(DateTime, default=datetime.utcnow)

    query = relationship("Query", back_populates="items")

