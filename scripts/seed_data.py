from sqlmodel import Session
from app.database import engine
from app.models.task_model import Task
from app.models.user_model import UserModel
from app.models.refresh_token_model import RefreshTokenModel
from uuid import uuid4
from datetime import datetime, timezone
from app.utils.security import hash_password

import random

def seed():

    with Session(engine) as session:
        users: list[UserModel] = [];
        for i in range(50):
            user = UserModel(
                id = uuid4(),
                username= f"user_{i}",
                hashed_password = hash_password("123456"), #"123456",
                created_at = datetime.now(timezone.utc),
                updated_at= datetime.now(timezone.utc)
            )

            session.add(user)
            users.append(user)

        session.commit();

        for i in range(200):
            task = Task(
                name=f"Task {i}",
                status="pending",
                progress=random.randint(0, 100),
                priority=random.randint(1, 5),
                user_id=random.choice(users).id
            )
            session.add(task)

        session.commit()

print("🌱 Not Run Seeding...", __name__)

if __name__ == "__main__":
    print("🌱 Seeding database...")
    seed()