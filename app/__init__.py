"""Declaring configuration for database interactions."""
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_PATH, DEBUG, TEST_DATABASE_PATH

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/dev/token")
Base = declarative_base()

DB_URL = "sqlite:///{path}".format(path=DATABASE_PATH)
TEST_DB_URL = "sqlite:///{path}".format(path=TEST_DATABASE_PATH)

engine = create_engine(DB_URL, echo=DEBUG)
test_engine = create_engine(TEST_DB_URL, echo=True)

DBSession = sessionmaker(bind=engine)
