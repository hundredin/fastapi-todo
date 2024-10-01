from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_URL = "postgresql+psycopg://vscode:notsecure@db:5432/testdb"
db_engine = create_engine(DB_URL, echo=True)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def get_db():
    with db_session() as session:
        yield session