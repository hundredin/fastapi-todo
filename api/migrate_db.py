from sqlalchemy import create_engine

from api.models import Base
from api.models.task import Task, Done

DB_URL = "postgresql+psycopg://vscode:notsecure@db:5432/testdb"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    reset_database()
