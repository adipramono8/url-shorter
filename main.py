from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud, schemas, dbModel, auth
from dbSetup import engine, get_db, Base

# Create the database tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

# User 'Registration' endpoint
@app.post("/auth/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# User 'Login' endpoint
@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Creating a new 'Short my URL' endpoint (1)
@app.post("/api/links", response_model=schemas.responseURL)
def create_short_link(link: schemas.newURL, request: Request, db: Session = Depends(get_db), current_user: dbModel.User = Depends(auth.get_current_user)):
    db_link = crud.create_short_url(db=db, link=link)
    base_url = str(request.base_url)
    short_url = base_url + db_link.short_url
    return schemas.responseURL(
        long_url=db_link.long_url,
        short_url=short_url,
        created_at=db_link.created_at
    )

# 'Redirecting short URL to long URL' endpoint (2)
@app.get("/{short_url}")
def redirect_short_url(short_url: str, db: Session = Depends(get_db)):
    db_link = crud.get_short_url(db=db, short_url=short_url)
    if db_link is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=db_link.long_url, status_code=302)

# User 'My Links' endpoint
@app.get("/api/my-links", response_model=list[schemas.responseURL])
def get_user_URL(db: Session = Depends(get_db), current_user: dbModel.User = Depends(auth.get_current_user)):
    user_URL = crud.get_url_by_user(db=db, owner_id=current_user.id)
    return user_URL