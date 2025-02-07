from fastapi import FastAPI, Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from typing import Annotated

Base = declarative_base()
app = FastAPI()


from config import Config

engine = create_engine(Config.DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

Base = declarative_base()

# Dependency injection for the database session
app.dependency_overrides[Session] = get_db

import routes
