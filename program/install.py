from sqlalchemy import create_engine

from program.db_tables import db, Base


def create_database(db_name):
    engine = create_engine(db_name, echo=True) #TODO silence
    Base.metadata.create_all(engine)


def install():
    create_database(db)


if __name__ == '__main__':
    install()
