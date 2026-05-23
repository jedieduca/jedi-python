from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from core.configs import settings

engine: AsyncEngine = create_async_engine(
    settings.DB_URL_API,
    echo=False,
    future=True,
    pool_size=20,          # Mantém até 20 conexões prontas na manga
    max_overflow=10,       # Permite abrir mais 10 se houver pico de acessos
    pool_timeout=30,
    pool_recycle=3600      # Recicla conexões antigas para evitar estouro no MariaDB
)

SessionLocal: AsyncSession = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)

engineJEDi: AsyncEngine = create_async_engine(
    settings.DB_URL_JEDI,
    echo=False,             # lança o SQL gerado no console do servidor
    future=True,
    pool_size=20,          # Mantém até 20 conexões prontas na manga
    max_overflow=10,       # Permite abrir mais 10 se houver pico de acessos
    pool_timeout=30,
    pool_recycle=3600      # Recicla conexões antigas para evitar estouro no MariaDB
)

SessionJEDi: AsyncSession = async_sessionmaker(
    bind=engineJEDi,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)

