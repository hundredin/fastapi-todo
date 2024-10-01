from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


DB_URL = "postgresql+asyncpg://vscode:notsecure@db:5432/testdb"
async_engine = create_async_engine(DB_URL, echo=True)

async_session = async_sessionmaker(expire_on_commit=True, autoflush=False, bind=async_engine)

async def get_db():
    async with async_session() as session:
        yield session