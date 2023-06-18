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


def test_lowercase():
    s = "ala ma KotA"
    assert lowercase(s) == "ala ma kota"


def test_capitalize():
    s = "ala ma KotA"
    assert capitalize(s) == "Ala Ma Kota"


def test_toogle_case():
    s = "ala ma KotA"
    assert toggle_case(s) == "ALA MA kOTa"


def test_reverse():
    s = "ala ma KotA"
    assert reverse(s) == "AtoK am ala"


def test_duplicate():
    s = "ala ma KotA"
    assert duplicate(s) == "ala ma KotAala ma KotA"
    assert duplicate(s, 3) == "ala ma KotAala ma KotAala ma KotA"


def test_rotate_left():
    s = "ala ma KotA"
    assert rotate_left(s) == "la ma KotAa"
    assert rotate_left(s, 4) == "ma KotAala "


def test_join():
    s1 = "ala ma KotA"
    s2 = "@ 0La ma psa"
    s3 = "pAs$wOrd"
    assert join(s1, s2) == "ala ma KotA@ 0La ma psa"
    assert join(s2, s3) == "@ 0La ma psapAs$wOrd"


def test_truncate_left():
    s = "ala ma KotA"
    assert truncate_left(s) == "la ma KotA"
    assert truncate_left(s, 2) == "a ma KotA"


def test_delete_at():
    s = "ala ma KotA"
    assert delete_at(s, 3) == "alamaKotA"


def test_omit_range():
    s = "ala ma KotA"
    assert omit_range(s, 4, 2) == "ala  KotA"


def test_overwrite_at():
    s = "ala ma KotA"
    assert overwrite_at(s, 0, "o") == "ola ma KotA"


def test_replace():
    s = "ala ma KotA"
    assert replace(s, "a", "@") == "@l@ m@ KotA"
    assert replace(s, "k", "4") == "ala ma KotA"


def test_duplicate_at():
    s = "ala ma KotA"
    assert duplicate_at(s, 7, 3) == "ala ma KKKotA"


def test_duplicate_all():
    s = "ala ma KotA"
    assert duplicate_all(s, 4) == "ala ma KotAala ma KotAala ma KotAala ma KotA"


def test_swap_chars_at():
    s = "ala ma KotA"
    assert swap_chars_at(s, 0, 10) == "Ala ma Kota"


def test_increment_char_ascii_at():
    s = "ala ma KotA"
    assert increment_char_ascii_at(s, 5, 3) == "ala md KotA"
    assert increment_char_ascii_at(s, 10, 1) == "ala ma KotB"


def test_decrement_char_ascii_at():
    s = "ala ma KotA"
    assert decrement_char_ascii_at(s, 1, 1) == "aka ma KotA"
    assert decrement_char_ascii_at(s, 8, 2) == "ala ma KmtA"


def test_dupicate_first():
    s = "ala ma KotA"
    assert duplicate_first(s, 2, 3) == "alalala ma KotA"
    assert duplicate_first(s, 4, 2) == "ala ala ma KotA"


def test_duplicate_last():
    s = "ala ma KotA"
    assert duplicate_last(s, 3, 3) == "ala ma KotAotAotA"
    assert duplicate_last(s, 2, 2) == "ala ma KotAtA"


def test_interlace():
    s1 = "ala ma KotA"
    s2 = "@ 0La ma psa"
    s3 = "pAs$wOrd"
    assert interlace(s1, s2, [i for i in range(12)]) == "@a l0aL am am aK optsAa"
    assert interlace(s1, s3, [i for i in range(8)]) == "paAlsa$ wmOar dKotA"
