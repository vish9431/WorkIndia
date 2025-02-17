from app import db
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

@contextmanager
def db_session():
    try:
        yield db.session
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e