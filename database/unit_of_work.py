from contextlib import contextmanager


@contextmanager
def SQLAlchemyUnitOfWork(session):
    db = session()
    try:
        yield db
    finally:
        db.close()
