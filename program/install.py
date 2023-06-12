from sqlalchemy import create_engine

import db_tables as db


def create_database(db_name):
    engine = create_engine(f"sqlite:///{db_name}.db", echo=True) #TODO silence
    db.Base.metadata.create_all(engine)


def install():
    create_database(db.db_name)


if __name__ == '__main__':
    install()
