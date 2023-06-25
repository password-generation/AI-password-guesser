import pytest
from password_rules import *


def test_nothing():
    assert nothing("ala ma KotA") == "ala ma KotA"


def test_lowercase():
    assert lowercase("ala ma KotA") == "ala ma kota"


def test_uppercase():
    assert uppercase("ala ma KotA") == "ALA MA KOTA"


def test_capitalize():
    assert capitalize("ala ma KotA") == "Ala ma kota"


def test_invert_capitalize():
    assert invert_capitalize("ala ma KotA") == "aLA MA KOTA"


def test_toogle_case():
    assert toggle_case("ala ma KotA") == "ALA MA kOTa"


def test_toggle_at():
    assert toggle_at("ala ma KotA", 0) == "Ala ma KotA"
    assert toggle_at("ala ma KotA", 7) == "ala ma kotA"


def test_reverse():
    assert reverse("ala ma KotA") == "AtoK am ala"


def test_duplicate():
    assert duplicate("ala ma KotA") == "ala ma KotAala ma KotA"
    assert duplicate("ala ma KotA", 2) == "ala ma KotAala ma KotAala ma KotA"


def test_reflect():
    assert reflect("ala ma KotA") == "ala ma KotAAtoK am ala"


def test_rotate_left():
    assert rotate_left("ala ma KotA") == "la ma KotAa"
    assert rotate_left("ala ma KotA", 4) == "ma KotAala "


def test_rotate_right():
    assert rotate_right("ala ma KotA") == "Aala ma Kot"
    assert rotate_right("ala ma KotA", 5) == " KotAala ma"


def test_truncate_left():
    assert truncate_left("ala ma KotA") == "la ma KotA"
    assert truncate_left("ala ma KotA", 2) == "a ma KotA"


def test_truncate_right():
    assert truncate_right("ala ma KotA") == "ala ma Kot"
    assert truncate_right("ala ma KotA", 5) == "ala ma"


def test_delete_at():
    assert delete_at("ala ma KotA", 3) == "alama KotA"


def test_extract_range():
    assert extract_range("ala ma KotA", 0, 3) == "ala"
    assert extract_range("ala ma KotA", 3, 5) == " ma K"


def test_omit_range():
    assert omit_range("ala ma KotA", 4, 2) == "ala  KotA"


def test_insert_at():
    assert insert_at("ala ma KotA", 3, "n") == "alan ma KotA"
    assert insert_at("ala ma KotA", 4, "nie ") == "ala nie ma KotA"


def test_overwrite_at():
    assert overwrite_at("ala ma KotA", 0, "o") == "ola ma KotA"


def test_replace():
    assert replace("ala ma KotA", "a", "@") == "@l@ m@ KotA"
    assert replace("ala ma KotA", "k", "4") == "ala ma KotA"


def test_purge():
    assert purge("ala ma KotA", "a") == "l m KotA"


def test_dupicate_first():
    assert duplicate_first("ala ma KotA", 2, 3) == "alalala ma KotA"
    assert duplicate_first("ala ma KotA", 4, 2) == "ala ala ma KotA"


def test_duplicate_last():
    assert duplicate_last("ala ma KotA", 3, 3) == "ala ma KotAotAotA"
    assert duplicate_last("ala ma KotA", 2, 2) == "ala ma KotAtA"


def test_duplicate_at():
    assert duplicate_at("ala ma KotA", 7, 3) == "ala ma KKKotA"


def test_duplicate_all():
    assert duplicate_all("ala ma KotA") == "aallaa  mmaa  KKoottAA"
    assert duplicate_all("ala ma KotA", 2) == "aaalllaaa   mmmaaa   KKKoootttAAA"


def test_swap_chars_at():
    assert swap_chars_at("ala ma KotA", 0, 10) == "Ala ma Kota"


def test_increment_char_ascii_at():
    assert increment_char_ascii_at("ala ma KotA", 5, 3) == "ala md KotA"
    assert increment_char_ascii_at("ala ma KotA", 10, 1) == "ala ma KotB"


def test_decrement_char_ascii_at():
    assert decrement_char_ascii_at("ala ma KotA", 1, 1) == "aka ma KotA"
    assert decrement_char_ascii_at("ala ma KotA", 8, 2) == "ala ma KmtA"


def test_join():
    assert join("ala ma KotA", "@ 0La ma psa") == "ala ma KotA@ 0La ma psa"
    assert join("@ 0La ma psa", "pAs$wOrd") == "@ 0La ma psapAs$wOrd"


def test_interlace():
    assert (
        interlace("ala ma KotA", "@ 0La ma psa", [i for i in range(12)])
        == "@a l0aL am am aK optsAa"
    )
    assert (
        interlace("ala ma KotA", "pAs$wOrd", [i for i in range(8)])
        == "paAlsa$ wmOar dKotA"
    )
