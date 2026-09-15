import pytest
from sqlmodel import Session, create_engine

DATABASE_URL = (
    "postgresql+psycopg://postgres:postgres" "@localhost:5434/ai_chat_api_test"
)

engine = create_engine(
    DATABASE_URL,
)


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session
