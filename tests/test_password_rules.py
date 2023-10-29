import pytest
from password_mangler.password_rules import *


#TODO Change order of arguments in some of the functions

def test_nothing():
    assert nothing("ala ma KotA") == "ala ma KotA"
    assert nothing("p@ssW0rd") == "p@ssW0rd"


def test_lowercase():
    assert lowercase("ala ma KotA") == "ala ma kota"
    assert lowercase("p@ssW0rd") == "p@ssw0rd"


def test_uppercase():
    assert uppercase("ala ma KotA") == "ALA MA KOTA"
    assert uppercase("p@ssW0rd") == "P@SSW0RD"


def test_capitalize():
    assert capitalize("ala ma KotA") == "Ala ma kota"
    assert capitalize("p@ssW0rd") == "P@ssw0rd"


def test_invert_capitalize():
    assert invert_capitalize("ala ma KotA") == "aLA MA KOTA"
    assert invert_capitalize("p@ssW0rd") == "p@SSW0RD"


def test_toogle_case():
    assert toggle_case("ala ma KotA") == "ALA MA kOTa"
    assert toggle_case("p@ssW0rd") == "P@SSw0RD"


def test_toggle_at():
    assert toggle_at("ala ma KotA", 0) == "Ala ma KotA"
    assert toggle_at("ala ma KotA", 7) == "ala ma kotA"
    assert toggle_at("p@ssW0rd", 3) == "p@sSW0rd"


def test_reverse():
    assert reverse("ala ma KotA") == "AtoK am ala"
    assert reverse("p@ssW0rd") == "dr0Wss@p"


def test_duplicate():
    assert duplicate("ala ma KotA") == "ala ma KotAala ma KotA"
    assert duplicate("ala ma KotA", 2) == "ala ma KotAala ma KotAala ma KotA"
    assert duplicate("p@ssW0rd") == "p@ssW0rdp@ssW0rd"
    assert duplicate("p@ssW0rd", 2) == "p@ssW0rdp@ssW0rdp@ssW0rd"


def test_reflect():
    assert reflect("ala ma KotA") == "ala ma KotAAtoK am ala"
    assert reflect("p@ssW0rd") == "p@ssW0rddr0Wss@p"


def test_rotate_left():
    assert rotate_left("ala ma KotA") == "la ma KotAa"
    assert rotate_left("ala ma KotA", 4) == "ma KotAala "
    assert rotate_left("p@ssW0rd") == "@ssW0rdp"


def test_rotate_right():
    assert rotate_right("ala ma KotA") == "Aala ma Kot"
    assert rotate_right("ala ma KotA", 5) == " KotAala ma"
    assert rotate_right("p@ssW0rd") == "dp@ssW0r"


def test_truncate_left():
    assert cut_start("ala ma KotA") == "la ma KotA"
    assert cut_start("ala ma KotA", 2) == "a ma KotA"
    assert cut_start("p@ssW0rd") == "@ssW0rd"


def test_truncate_right():
    assert cut_end("ala ma KotA") == "ala ma Kot"
    assert cut_end("ala ma KotA", 5) == "ala ma"
    assert cut_end("p@ssW0rd") == "p@ssW0r"


def test_delete_at():
    assert delete_at("ala ma KotA", 3) == "alama KotA"
    assert delete_at("p@ssW0rd", 3) == "p@sW0rd"


def test_extract_range():
    assert extract_range("ala ma KotA", 0, 3) == "ala"
    assert extract_range("ala ma KotA", 3, 5) == " ma K"
    assert extract_range("p@ssW0rd", 0, 4) == "p@ss"


def test_omit_range():
    assert omit_range("ala ma KotA", 4, 2) == "ala  KotA"
    assert omit_range("p@ssW0rd", 1, 2) == "psW0rd"


def test_insert_at():
    assert insert_at("ala ma KotA", 3, "n") == "alan ma KotA"
    assert insert_at("ala ma KotA", 4, "nie ") == "ala nie ma KotA"
    assert insert_at("p@ssW0rd", 4, "!") == "p@ss!W0rd"


def test_overwrite_at():
    assert overwrite_at("ala ma KotA", 0, "o") == "ola ma KotA"
    assert overwrite_at("p@ssW0rd", 3, "$") == "p@s$W0rd"


def test_replace():
    assert replace("ala ma KotA", "a", "@") == "@l@ m@ KotA"
    assert replace("ala ma KotA", "k", "4") == "ala ma KotA"
    assert replace("p@ssW0rd", "s", "$") == "p@$$W0rd"


def test_purge():
    assert purge("ala ma KotA", "a") == "l m KotA"
    assert purge("p@ssW0rd", "s") == "p@W0rd"


def test_dupicate_first():
    assert duplicate_first("ala ma KotA", 2, 2) == "alalala ma KotA"
    assert duplicate_first("ala ma KotA", 1, 4) == "ala ala ma KotA"
    assert duplicate_first("p@ssW0rd", 2) == "ppp@ssW0rd"


def test_duplicate_last():
    assert duplicate_last("ala ma KotA", 2, 3) == "ala ma KotAotAotA"
    assert duplicate_last("ala ma KotA", 1, 2) == "ala ma KotAtA"
    assert duplicate_last("p@ssW0rd", 2) == "p@ssW0rddd"


def test_duplicate_at():
    assert duplicate_at("ala ma KotA", 7, 2) == "ala ma KKKotA"
    assert duplicate_at("p@ssW0rd", 1) == "p@@ssW0rd"


def test_duplicate_all():
    assert duplicate_all("ala ma KotA") == "aallaa  mmaa  KKoottAA"
    assert duplicate_all("ala ma KotA", 2) == "aaalllaaa   mmmaaa   KKKoootttAAA"
    assert duplicate_all("p@ssW0rd") == "pp@@ssssWW00rrdd"


def test_swap_front():
    assert swap_front("ala ma KotA") == "laa ma KotA"
    assert swap_front("p@ssW0rd") == "@pssW0rd"


def test_swap_back():
    assert swap_back("ala ma KoAt") == "ala ma KotA"
    assert swap_back("p@ssW0rd") == "p@ssW0dr"


def test_swap_chars_at():
    assert swap_chars_at("ala ma KotA", 0, 10) == "Ala ma Kota"
    assert swap_chars_at("p@ssW0rd", 0, 1) == "@pssW0rd"
    assert swap_chars_at("p@ssW0rd", 1, 3) == "pss@W0rd"
    assert swap_chars_at("p@ssW0rd", 3, 1) == "pss@W0rd"


def test_increment_char_ascii_at():
    assert increment_char_ascii_at("ala ma KotA", 5, 3) == "ala md KotA"
    assert increment_char_ascii_at("ala ma KotA", 10, 1) == "ala ma KotB"
    assert increment_char_ascii_at("p@ssW0rd", 2) == "p@tsW0rd"


def test_decrement_char_ascii_at():
    assert decrement_char_ascii_at("ala ma KotA", 1, 1) == "aka ma KotA"
    assert decrement_char_ascii_at("ala ma KotA", 8, 2) == "ala ma KmtA"
    assert decrement_char_ascii_at("p@ssW0rd", 1) == "p?ssW0rd"


def test_join():
    assert join("ala ma KotA", "@ 0La ma psa") == "ala ma KotA@ 0La ma psa"
    assert join("@ 0La ma psa", "pAs$wOrd") == "@ 0La ma psapAs$wOrd"
    assert join("p@ssW0rd", "p?W0rd") == "p@ssW0rdp?W0rd"


def test_interlace():
    assert interlace("ala ma KotA", "@ 0La ma psa") == "@a l0aL am am aK optsAa"
    assert interlace("ala ma KotA", "pAs$wOrd", range(8)) == "paAlsa$ wmOar dKotA"
    assert interlace("p@ssW0rd", "12345", range(1, 6)) == "p1@2s3s4W50rd"
    assert interlace("p@ssW0rd", "123456789", range(1, 10)) == "p1@2s3s4W506r7d89"
