# FastAPI Todo app

## poetry commands
### project initialization using poetry
```
poetry init --name demo-app --dependency fastapi --dependency uvicorn[standard] --dependency sqlalchemy
```

### poetry install all dependencies
```
poetry install --no-root
```

### add dependency
```
poetry add asyncpg
poetry add psycopg
poetry add httpx
```

### run uvicorn server using poetry
```
poetry run uvicorn api.main:app --host 0.0.0.0 --reload
```

## Alembic Database Migration
### init
```bash
alembic init alembic
```

### add revision
```bash
alembic revision -m 'some messgage`
```

### upgrade
```bash
alembic upgrade head # upgrade to latest version
alembic upgrade +1 # upgrade one step after downgrade
```

### downgrade
```bash
alembic downgrade -1 # downgrade one step
alembic downgrade -2 # downgrade two step
alembic downgrade base # downgrade to all the way down
```