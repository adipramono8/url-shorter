from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import crud
import schemas
import dbModel
from dbSetup import engine, get_db, Base

# Create the database tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Creating a new short URL endpoint (1)
@app.post("/api/links", response_model=schemas.responseURL)
def create_short_link(link: schemas.newURL, request: Request, db: Session = Depends(get_db)):
    db_link = crud.create_short_url(db=db, link=link)
    base_url = str(request.base_url)
    short_url = base_url + db_link.short_url
    return schemas.responseURL(
        long_url=db_link.long_url,
        short_url=short_url,
        created_at=db_link.created_at
    )

# Redirecting short URL to long URL endpoint (2)
@app.get("/{short_url}")
def redirect_short_url(short_url: str, db: Session = Depends(get_db)):
    db_link = crud.get_short_url(db=db, short_url=short_url)
    if db_link is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=db_link.long_url, status_code=302)