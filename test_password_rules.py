import pytest
from password_rules import *


def test_nothing():
    s = "ala ma KotA"
    assert nothing(s) == s


def test_uppercase():
    s = "ala ma KotA"
    assert uppercase(s) == "ALA MA KOTA"


def test_invert_capitalize():
    s = "ala ma KotA"
    assert invert_capitalize(s) == "aLA MA KOTA"


def test_toggle_at():
    s = "ala ma KotA"
    assert toggle_at(s, 0) == "Ala ma KotA"
    assert toggle_at(s, 7) == "ala ma kotA"


def test_reflect():
    s = "ala ma KotA"
    assert reflect(s) == "ala ma KotAAtoK am ala"


def test_rotate_right():
    s = "ala ma KotA"
    assert rotate_right(s) == "Aala ma Kot"
    assert rotate_right(s, 5) == " KotAala ma"


def test_truncate_right():
    s = "ala ma KotA"
    assert truncate_right(s) == "ala ma Kot"
    assert truncate_right(s, 5) == "ala ma"


def test_extract_range():
    s = "ala ma KotA"
    assert extract_range(s, 0, 3) == "ala"
    assert extract_range(s, 3, 5) == " ma K"


def test_insert_at():
    s = "ala ma KotA"
    assert insert_at(s, 3, "n") == "alan ma KotA"
    assert insert_at(s, 4, "nie ") == "ala nie ma KotA"


def test_purge():
    s = "ala ma KotA"
    assert purge(s, "a") == "l m KotA"
