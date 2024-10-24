"""Functions to setup database."""
from sqlalchemy import create_engine

from app import DB_URL, Base


def create_database_from_models() -> None:
    """Function launched on start in lifespan."""
    engine = create_engine(DB_URL, echo=True)
    Base.metadata.create_all(engine)


def check_schemas_and_tables():
    """Check on existing tables is required."""
