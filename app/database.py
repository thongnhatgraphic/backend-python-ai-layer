from sqlmodel import SQLModel, create_engine, Session
from app.config import settings
# sqlite_url = "sqlite:///./tasks.db"

engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session



# def create_db():
#     SQLModel.metadata.create_all(engine)
    