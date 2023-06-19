from sqlalchemy import create_engine

from program.db_tables import db, Base
import json
from program.Tasker import Tasker
from program.Settings import Settings


def create_database(db_name):
    engine = create_engine(db_name, echo=True)  # TODO silence
    Base.metadata.create_all(engine)


def create_settings():
    settings_dict = {"urgent_priority": 1, "coming_priority": 3, "far_priority": 7, "language_option": "polish",
                     "daily_list_priority_lvl": 0}

    with open("settings.json", "w") as settings_file:
        json.dump(settings_dict, settings_file)


def create_initial_categories():
    settings = Settings()
    tasker = Tasker(settings.priority_dict, settings.daily_list_priority_lvl)
    tasker.add_category("dom")
    tasker.add_category("studia")
    tasker.add_category("inne")


def install():
    create_database(db)
    create_settings()
    create_initial_categories()


if __name__ == '__main__':
    install()
