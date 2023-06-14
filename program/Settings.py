import json


class Settings:
    """This class handles settings"""
    #TODO __init__
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
        """Changes priority level settings (time windows assigned to each priority level)"""
        self.priority_dict[0] = urgent
        self.priority_dict[1] = coming
        self.priority_dict[2] = far
        self.save_settings()


    def change_language_option(self, l_option: str):
        """Changes default language option setting"""
        self.language_option = l_option
        self.save_settings()

    def change_daily_list_priority_level_setting(self, new_lvl: int):
        """Changes daily list priority level setting"""
        self.daily_list_priority_lvl = new_lvl
        self.save_settings()


