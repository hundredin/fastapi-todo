import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import starlette

from api.db import get_db
from api.models import Base
from api.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # 비동기식 db 접속을 위한 엔진과 세션을 작성
    async_engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 의존성 주입으로 FastAPI 가 테스트용 DB 를 참조하도록 변경
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # 테스트용 비동기 HTTP 클라이언트 반환
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_task(async_client):
    response = await async_client.post("/tasks", json={"title": "test task"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "test task"

    response = await async_client.get("/tasks")
    response_obj = response.json()

    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "test task"
    assert response_obj[0]["done"] is False

@pytest.mark.asyncio
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json={"title": "test task 2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "test task 2"

    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 이미 완료 플래그가 설정되어 있으므로 400 에러가 발생해야 함
    response_obj = response.json()
    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    # 완료 플래그 해제
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    # 이미 완료 플래그가 해제되었으므로 404 에러가 발생해야 함
    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
@pytest.mark.parametrize("input_param, expectation", [
    ("2024-12-01", starlette.status.HTTP_200_OK),
    ("2024-12-32", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("20241201", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("2024/12/01", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY)
])
async def test_due_date(input_param, expectation, async_client):
    response = await async_client.post("/tasks", json={"title": "test task", "due_date": input_param})
    assert response.status_code == expectation