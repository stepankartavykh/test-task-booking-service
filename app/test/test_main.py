from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import TEST_DATABASE_PATH
from app.main import app

test_db_url = 'sqlite:///{dbname}'.format(dbname=TEST_DATABASE_PATH)
testing_engine = create_engine(test_db_url, echo=True)
testing_session = sessionmaker(bind=testing_engine, autoflush=False)


def get_session() -> Generator[Session]:

    connection = testing_engine.connect()
    transaction = connection.begin()
    session = testing_session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_app(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    with TestClient(app) as client:
        yield client


test_client = TestClient(app)


def test_create_booking():
    booking_data_wrong_dates = {
        "guest_name": "John Doe",
        "check_in_date": "2023-05-01T10:00:00",
        "check_out_date": "2023-05-01T10:00:00",
        "room_number": 1
    }
    post_response = test_client.post("/api/dev/booking", json=booking_data_wrong_dates)
    assert post_response.status_code == 400
    booking_data_wrong_dates = {
        "guest_name": "John Doe",
        "check_in_date": "2023-04-01T10:00:00",
        "check_out_date": "2023-04-01T01:00:00",
        "room_number": 1
    }
    post_response = test_client.post("/api/dev/booking", json=booking_data_wrong_dates)
    assert post_response.status_code == 400
