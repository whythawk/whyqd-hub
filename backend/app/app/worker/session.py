from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings


def get_scoped_session():
    # https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/68#issuecomment-537883784
    # Method of use:
    #     SessionScoped = get_scoped_session()
    #     db = SessionScoped()
    #     ...
    #     db.close()
    #     SessionScoped.remove()
    # Has to be *inside* the function calling it to ensure that it is an independent session.
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI.unicode_string(),
        pool_pre_ping=True,
        pool_recycle=3600,  # this line might not be needed
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    )
    meta = MetaData()
    meta.reflect(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    SessionScoped = scoped_session(SessionLocal)
    # Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionScoped
