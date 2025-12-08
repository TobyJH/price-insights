import argparse
from typing import List

from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import crud
import schemas
from ebay_client import find_completed_items, normalise_item, EbayClientError
from parsers_rab import parse_rab_jacket

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)


def ingest_ebay_data(name: str, search_term: str, max_results: int) -> None:
    db: Session = SessionLocal()
    try:
        # Get or create query
        existing = crud.get_query_by_name(db, name=name)
        if existing:
            query = existing
            print(f"Using existing query id={query.id} name={query.name!r}")
        else:
            query = crud.create_query(
                db,
                schemas.QueryCreate(name=name, search_term=search_term),
            )
            print(f"Created new query id={query.id} name={query.name!r}")

        print(
            f"Fetching up to {max_results} sold items from eBay for search term: {search_term!r}"
        )
        try:
            raw_items: List[dict] = find_completed_items(
                search_term=search_term,
                max_results=max_results,
            )
        except EbayClientError as e:
            print(f"ERROR calling eBay API: {e}")
            return

        print(f"Retrieved {len(raw_items)} raw sold items from eBay.")

        inserted = 0
        skipped_existing = 0

        for raw in raw_items:
            norm = normalise_item(raw, query_id=query.id)

            # Simple Rab detection: if title contains "rab", try to parse
            if "rab" in norm["title"].lower():
                extra = parse_rab_jacket(norm["title"])
                norm.update(extra)

            # Skip if we already have this ebay_item_id
            existing_item = crud.get_item_by_ebay_item_id(
                db, norm["ebay_item_id"]
            )
            if existing_item:
                skipped_existing += 1
                continue

            item_create = schemas.ItemCreate(**norm)
            crud.create_item(db, item_create)
            inserted += 1

        print(
            f"Ingestion complete. Inserted {inserted} new items, "
            f"skipped {skipped_existing} existing items."
        )
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest real sold item data from eBay into the local DB."
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
    parser.add_argument(
        "--max",
        type=int,
        default=200,
        help="Maximum number of sold items to fetch (default: 200)",
    )

    args = parser.parse_args()
    ingest_ebay_data(args.name, args.search_term, args.max)

