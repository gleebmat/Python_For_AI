from typing import Generator
from sqlalchemy.orm import Session
from app.database import sessionLocal


def get_db() -> Generator[Session, None, None]:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
