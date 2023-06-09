"""This file contains functions adding functions for getting ingredient lists from aniagotuje.pl"""
from datetime import datetime
from bs4 import BeautifulSoup

import requests

key_words = ["ugotuj", "ugotować", "upiecz", "upiec", "usmażyć", "usmaż"]


def add_task_with_ania_mode(add_task_func):
    """Wrapp add_task function with to operate with Ania Mode"""

    def wrapper(self, name: str, cat: str, desc: str, exec_date: datetime, deadline: datetime, subtasks: list):
        recipe_url = search(name)
        add_task_func(self, name, cat, desc, exec_date, deadline, subtasks)
        return recipe_url

    return wrapper


def search(task_name):
    """Returns an url address if a recipe is found or None otherwise"""
    recipe_name = find_recipe_name_for_url(task_name)
    if recipe_name is not None:
        url = f"https://aniagotuje.pl/przepis/{recipe_name}"
        request = requests.get(url)
        if request.status_code == 200:
            return url
        else:
            return None
    else:
        return None


def find_recipe_name_for_url(task_name):
    """Returns the name of a recipe if found, None otherwise.
    Returned recipe name is prepared for using in url"""
    replace = 'ĄąĘęŻżŹźĆćÓóŁł'
    replace_with = 'AaEeZzZzCcOoLl'
    translator = str.maketrans(replace, replace_with)

    task_name_list = task_name.split(" ")
    for word in key_words:
        if task_name_list[0] == word:
            joined = '-'.join(task_name_list[1:])
            no_polish_letters = joined.translate(translator)
            return no_polish_letters
    return None


def find_recipe_name(task_name):
    """Returns the name of a recipe if found, None otherwise"""
    return " ".join(task_name.split(" ")[1:])


def get_ing_list(request):
    """Returns a list of ingredients"""
    soup = BeautifulSoup(request.content, "html.parser")
    ing_lists = soup.find("div", id="__layout").find_all("ul", class_="recipe-ing-list")
    ingredients = list()
    for ing_list in ing_lists:
        part_ingredients = ing_list.find_all("li", itemprop="recipeIngredient")
        for ing in part_ingredients:
            ingredients.append(ing.get_text())

    return ingredients


def create_shopping_task(tasker, parent_task_name, cat, exec_date, deadline, url):
    """
    Returns a task with ingredients for the recipe as subtasks.
    """
    recipe_name = find_recipe_name(parent_task_name)
    task_name = f"Zakupy na {recipe_name}"
    desc = f"Wygenerowane na podstawie przepisu ze strony: {url}"
    ingredients = get_ing_list(requests.get(url))

    tasker.add_task(name=task_name, cat=cat, desc=desc, exec_date=exec_date, deadline=deadline,
                    subtasks=ingredients)


if __name__ == '__main__':
    get_ing_list(requests.get("https://aniagotuje.pl/przepis/pierogi-ruskie"))
