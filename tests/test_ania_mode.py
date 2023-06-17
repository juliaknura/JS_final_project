import os

import pytest

from program import ania_mode
from program.Tasker import Tasker

os.chdir("../program")


@pytest.mark.parametrize("string, recipe", [("spotkanie biznesowe", None),
                                            ("ugotować bigos", "bigos"),
                                            ("upiec pierogi ruskie", "pierogi-ruskie"),
                                            ("ugotować gołąbki", "golabki")])
def test_find_recipe_name(string, recipe):
    # WHEN
    found = ania_mode.find_recipe_name_for_url(string)

    # THEN
    assert found == recipe


@pytest.mark.parametrize("string, should_return",
                         [("ugotować pierogi ruskie", "https://aniagotuje.pl/przepis/pierogi-ruskie"),
                          ("spotkanie biznesowe", None),
                          ("ugotować gołąbki tradycyjne", "https://aniagotuje.pl/przepis/golabki-tradycyjne"),
                          ("ugotować gołąbki", None)])
def test_search(string, should_return):
    # WHEN
    url = ania_mode.search(string)

    # THEN
    assert url == should_return

