import argparse
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import crud
import schemas

# Ensure tables exist before we try to use them
models.Base.metadata.create_all(bind=engine)


def seed_dummy_data(name: str, search_term: str):
    db: Session = SessionLocal()
    try:
        # Create or get query
        existing = crud.get_query_by_name(db, name=name)
        if existing:
            query = existing
        else:
            query = crud.create_query(
                db,
                schemas.QueryCreate(name=name, search_term=search_term),
            )

        print(f"Using query id={query.id} name={query.name!r}")

        # Create a few fake items
        base_time = datetime.utcnow()
        dummy_items = [
            schemas.ItemCreate(
                query_id=query.id,
                ebay_item_id=f"DUMMY-{query.id}-1",
                title=f"{name} - Test Listing 1",
                category_name="Coats & Jackets",
                condition="Used",
                listing_type="Auction",
                end_time=base_time - timedelta(days=1),
                price=85.0,
                currency="GBP",
                shipping_cost=4.0,
                total_price_est=89.0,
                bid_count=12,
                selling_state="EndedWithSales",
                seller_username="test_seller_1",
                seller_feedback_score=1234,
                seller_positive_percent=99.5,
                view_url="https://www.ebay.co.uk/itm/DUMMY-1",
            ),
            schemas.ItemCreate(
                query_id=query.id,
                ebay_item_id=f"DUMMY-{query.id}-2",
                title=f"{name} - Test Listing 2",
                category_name="Coats & Jackets",
                condition="Used",
                listing_type="FixedPrice",
                end_time=base_time - timedelta(days=2),
                price=95.0,
                currency="GBP",
                shipping_cost=0.0,
                total_price_est=95.0,
                bid_count=0,
                selling_state="EndedWithSales",
                seller_username="test_seller_2",
                seller_feedback_score=456,
                seller_positive_percent=98.0,
                view_url="https://www.ebay.co.uk/itm/DUMMY-2",
            ),
        ]

        for item in dummy_items:
            try:
                crud.create_item(db, item)
            except Exception as e:
                print(f"Skipping item {item.ebay_item_id}: {e}")

        print("Dummy data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed dummy data into the eBay Insights DB."
    )
    parser.add_argument(
        "--name",
        required=True,
        help='Logical name for the query, e.g. "Rab Microlight Alpine Men\'s"',
    )
    parser.add_argument(
        "--search-term",
        required=True,
        help='Search term used against eBay, e.g. "Rab Microlight Alpine jacket"',
    )
    args = parser.parse_args()
    seed_dummy_data(args.name, args.search_term)

