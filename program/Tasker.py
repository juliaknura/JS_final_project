from program.selecter import by_ddl, by_category, by_checked_off_date, by_exec_date
from sqlalchemy import create_engine
from datetime import datetime
import json
from program.db_tables import db_name


class Tasker:

    def __init__(self):
        self.current_task_list = self.get_today_list()
        self.engine = create_engine(db_name, echo=True)
        # TODO na razie niech bedzie verbose zeby ogladac co sie dzieje, potem to zmienimy
        p_dict, l_opt, d_list_p_lvl = self.load_settings()
        self.priority_dict = p_dict
        # A dictionary with default priority level settings:
        # level 0 - urgent
        # level 1 - coming
        # level 2 - far
        self.language_option = l_opt
        self.daily_list_priority_lvl = d_list_p_lvl

    def get_by_category(self, cat_id):
        task_tuple_list = by_category(cat_id, self.engine)
        # TODO - find out the format of the output of the selecting function, then proceed
        task_list = []
        return task_list

    def get_today_list(self):
        task_tuple_list = ...
        task_list = []
        return task_list

    def get_by_checked_off_date(self, checked_off_date: datetime):
        task_list = []
        return task_list

    def load_settings(self):
        """Loads saved settings"""
        with open("settings.json", "r") as settings_file:
            settings_dict = json.load(settings_file)
            priority_dict = {0: settings_dict["urgent_priority"], 1: settings_dict["coming_priority"],
                             2: settings_dict["far_priority"]}
            lang_option = settings_dict["language_option"]

            d_list_p_lvl = settings_dict["daily_list_priority_lvl"]
        return priority_dict, lang_option, d_list_p_lvl

    def save_settings(self):
        """Saves current app settings"""
        settings_dict = {}
        settings_dict["urgent_priority"] = self.priority_dict[0]
        settings_dict["coming_priority"] = self.priority_dict[1]
        settings_dict["far_priority"] = self.priority_dict[2]

        settings_dict["language_option"] = self.language_option

        settings_dict["daily_list_priority_lvl"] = self.daily_list_priority_lvl

        with open("settings.json", "w") as settings_file:
            json.dump(settings_dict, settings_file)

    def change_priority_lvl_settings(self, urgent: int, coming: int, far: int):
        """Changes priority level settings (time windows assigned to each priority level) in the current app run"""
        self.priority_dict[0] = urgent
        self.priority_dict[1] = coming
        self.priority_dict[2] = far

    def change_language_option(self, l_option: str):
        """Changes language option setting in the current app run"""
        self.language_option = l_option

    def change_daily_list_priority_level_setting(self, new_lvl: int):
        """Changes daily list priority level setting in the current app run"""
        self.daily_list_priority_lvl = new_lvl

    def _calculate_priority(self, deadline_date: datetime):
        """Calculates the number of days left until the deadline (rounds up) and returns priority category"""
        normalized_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (deadline_date - normalized_today).days
        urgent_bar = self.priority_dict[1]
        coming_bar = self.priority_dict[2]
        far_bar = self.priority_dict[3]
        if days_diff <= urgent_bar:
            return 0
        elif days_diff <= coming_bar:
            return 1
        elif days_diff <= far_bar:
            return 2

