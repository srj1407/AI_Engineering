from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# postgresql+asyncpg tells SQLAlchemy to use the async driver
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/task_db"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Dependency to use in FastAPI routes
async def get_db():
    async with SessionLocal() as session:
        yield session