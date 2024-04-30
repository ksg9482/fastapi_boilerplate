from sqlalchemy.orm import sessionmaker, as_declarative, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

"""
sqlite - 내장된 sqlite이용.
aiosqlite - 비동기 연결. (기본적으로 동기연결. asyncio에다가 이거도 써야 비동기 됨)
charset=utf8mb4 - 유니코드 설정. 유니코드 설정하면 sqlalchemy로 문자열 타입으로 매핑하면 유니코드 들어감
"""
DATABASE_URL = "sqlite+aiosqlite:///database.db?charset=utf8mb4"
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False, 
    bind=engine,
    class_=AsyncSession,
    )

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__tablename__.lower()

    @classmethod
    async def get_db(cls):
        async with AsyncSessionLocal() as session:
            yield session

def get_Base():
    return Base