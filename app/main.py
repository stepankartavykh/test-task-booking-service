"""App init module."""
import os.path
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.booking.controller import booking_router
from app.config import DATABASE_PATH, LOCAL_STORAGE_DIR
from app.users.controller import users_router
from app.utils import check_schemas_and_tables, create_database_from_models


def check_database_status() -> None:
    """Are there required databases, tables in place?"""
    if not os.path.exists(DATABASE_PATH):
        create_database_from_models()
    check_schemas_and_tables()


def check_storage_status():
    """Is there directory for reports?"""
    if not os.path.exists(LOCAL_STORAGE_DIR):
        os.mkdir(LOCAL_STORAGE_DIR)
    if not os.path.exists(LOCAL_STORAGE_DIR + "/reports"):
        os.mkdir(LOCAL_STORAGE_DIR + "/reports")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Procedures to launch app correctly (database, may be key-value storage, etc.)."""
    print('Start app procedures...')
    check_database_status()
    check_storage_status()
    print(app_)
    yield
    print('Shutdown procedures...')


app = FastAPI(debug=True, lifespan=lifespan)
app.include_router(booking_router, prefix="/api/dev")
app.include_router(users_router, prefix="/api/dev")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
