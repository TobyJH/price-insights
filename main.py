from typing import List

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas
import crud

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="eBay Insights API")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello from eBay Insights API with DB!"}


# ---------- JSON API endpoints ----------

@app.get("/queries", response_model=List[schemas.Query])
def list_queries(db: Session = Depends(get_db)):
    return crud.get_queries(db)


@app.post("/queries", response_model=schemas.Query)
def create_query(query_in: schemas.QueryCreate, db: Session = Depends(get_db)):
    db_query = crud.get_query_by_name(db, name=query_in.name)
    if db_query:
        raise HTTPException(status_code=400, detail="Query with this name already exists")
    return crud.create_query(db, query_in)


@app.get("/queries/{query_id}/items", response_model=List[schemas.Item])
def list_items_for_query(query_id: int, db: Session = Depends(get_db)):
    db_query = crud.get_query(db, query_id=query_id)
    if not db_query:
        raise HTTPException(status_code=404, detail="Query not found")
    return crud.get_items_for_query(db, query_id=query_id)


# ---------- HTML UI endpoints ----------

@app.get("/ui", response_class=HTMLResponse)
@app.get("/ui/queries", response_class=HTMLResponse)
def ui_queries(request: Request, db: Session = Depends(get_db)):
    queries = crud.get_queries(db)
    return templates.TemplateResponse(
        "queries.html",
        {"request": request, "queries": queries},
    )


@app.get("/ui/queries/{query_id}", response_class=HTMLResponse)
def ui_query_detail(query_id: int, request: Request, db: Session = Depends(get_db)):
    query = crud.get_query(db, query_id=query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    items = crud.get_items_for_query(db, query_id=query_id)
    return templates.TemplateResponse(
        "query_detail.html",
        {
            "request": request,
            "query": query,
            "items": items,
        },
    )

