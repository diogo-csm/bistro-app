import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(autouse=True)
def override_get_db(db_session, monkeypatch):
    def _get_db():
        try:
            yield db_session
        finally:
            pass
    monkeypatch.setattr("app.main.get_db", _get_db)
