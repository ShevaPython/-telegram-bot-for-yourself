from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from data import config



async_engine = create_async_engine( config.POSTGRES_URI, echo=True )
async_session = sessionmaker( async_engine, expire_on_commit=False, class_=AsyncSession,
                              autocommit=False, autoflush=False )


