from sqlalchemy.orm import Session
import dbModel, schemas, shorterLogic
import auth

# Finding a long URL in DB
def get_long_url(db: Session, long_url: str):
    return db.query(dbModel.Link).filter(dbModel.Link.long_url == str(long_url)).first()

# Finidng a short URL in DB
def get_short_url(db: Session, short_url: str):
    return db.query(dbModel.Link).filter(dbModel.Link.short_url == str(short_url)).first()

# Creating new short URL
def create_short_url(db: Session, link: schemas.newURL) -> dbModel.Link:
    # Checking if this long URL already shortened
    db_link = get_long_url(db, link.long_url)
    if db_link:
        return db_link
    
    # If there isn't, then we create a new entry based on the URL
    # 1. Creating new 'Link' object based on long_url column
    db_link = dbModel.Link(long_url=str(link.long_url))
    # 2. Adding session and committing to get the ID
    db.add(db_link)
    db.flush()
    db.refresh(db_link)
    # 3. Encoding the ID and updating the short_url column
    short_url = shorterLogic.encode_base62(db_link.id)
    db_link.short_url = short_url
    # 4. Commiting new update
    db.commit()
    db.refresh(db_link)
    return db_link

# Getting all links created by a specific user
def get_links_by_user(db: Session, user_id: int):
    return db.query(dbModel.Link).filter(dbModel.Link.owner_id == user_id).all()

# Getting user by email
def get_user_by_email(db: Session, email: str):
    return db.query(dbModel.User).filter(dbModel.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = dbModel.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user