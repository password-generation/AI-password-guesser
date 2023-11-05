import pytest
from password_mangler.password_rules import *


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
    assert toggle_at(0, "ala ma KotA") == "Ala ma KotA"
    assert toggle_at(7, "ala ma KotA") == "ala ma kotA"
    assert toggle_at(3, "p@ssW0rd") == "p@sSW0rd"


def test_reverse():
    assert reverse("ala ma KotA") == "AtoK am ala"
    assert reverse("p@ssW0rd") == "dr0Wss@p"


def test_duplicate():
    assert duplicate(1, "ala ma KotA") == "ala ma KotAala ma KotA"
    assert duplicate(2, "ala ma KotA") == "ala ma KotAala ma KotAala ma KotA"
    assert duplicate(1, "p@ssW0rd") == "p@ssW0rdp@ssW0rd"
    assert duplicate(2, "p@ssW0rd") == "p@ssW0rdp@ssW0rdp@ssW0rd"


def test_reflect():
    assert reflect("ala ma KotA") == "ala ma KotAAtoK am ala"
    assert reflect("p@ssW0rd") == "p@ssW0rddr0Wss@p"


def test_rotate_left():
    assert rotate_left(1, "ala ma KotA") == "la ma KotAa"
    assert rotate_left(4, "ala ma KotA") == "ma KotAala "
    assert rotate_left(1, "p@ssW0rd") == "@ssW0rdp"
    assert rotate_left(5, "abc") == "abc"


def test_rotate_right():
    assert rotate_right(1, "ala ma KotA") == "Aala ma Kot"
    assert rotate_right(5, "ala ma KotA") == " KotAala ma"
    assert rotate_right(1, "p@ssW0rd") == "dp@ssW0r"
    assert rotate_right(9, "cde") == "cde"


def test_truncate_left():
    assert cut_start(1, "ala ma KotA") == "la ma KotA"
    assert cut_start(2, "ala ma KotA") == "a ma KotA"
    assert cut_start(1, "p@ssW0rd") == "@ssW0rd"


def test_truncate_right():
    assert cut_end(1, "ala ma KotA") == "ala ma Kot"
    assert cut_end(5, "ala ma KotA") == "ala ma"
    assert cut_end(1, "p@ssW0rd") == "p@ssW0r"


def test_delete_at():
    assert delete_at(3, "ala ma KotA") == "alama KotA"
    assert delete_at(3, "p@ssW0rd") == "p@sW0rd"
    assert delete_at(7, "abc") == "abc"


def test_extract_range():
    assert extract_range(0, 3, "ala ma KotA") == "ala"
    assert extract_range(3, 5, "ala ma KotA") == " ma K"
    assert extract_range(0, 4, "p@ssW0rd") == "p@ss"
    assert extract_range(1, 5, "abc") == "bc"


def test_omit_range():
    assert omit_range(4, 2, "ala ma KotA") == "ala  KotA"
    assert omit_range(1, 2, "p@ssW0rd") == "psW0rd"
    assert omit_range(1, 5, "abc") == "a"


def test_insert_at():
    assert insert_at(3, "n", "ala ma KotA") == "alan ma KotA"
    assert insert_at(4, "nie ", "ala ma KotA") == "ala nie ma KotA"
    assert insert_at(4, "!", "p@ssW0rd") == "p@ss!W0rd"
    assert insert_at(5, "cd3f", "ab") == "abcd3f"


def test_overwrite_at():
    assert overwrite_at(0, "o", "ala ma KotA") == "ola ma KotA"
    assert overwrite_at(3, "$", "p@ssW0rd") == "p@s$W0rd"
    assert overwrite_at(7, "abc", "efg") == "efgabc"


def test_replace():
    assert replace("a", "@", "ala ma KotA") == "@l@ m@ KotA"
    assert replace("k", "4", "ala ma KotA") == "ala ma KotA"
    assert replace("s", "$", "p@ssW0rd") == "p@$$W0rd"


def test_purge():
    assert purge("a", "ala ma KotA") == "l m KotA"
    assert purge("s", "p@ssW0rd") == "p@W0rd"


def test_duplicate_first():
    assert duplicate_first(2, 2, "ala ma KotA") == "alalala ma KotA"
    assert duplicate_first(1, 4, "ala ma KotA") == "ala ala ma KotA"
    assert duplicate_first(2, 1, "p@ssW0rd") == "ppp@ssW0rd"


def test_duplicate_last():
    assert duplicate_last(2, 3, "ala ma KotA") == "ala ma KotAotAotA"
    assert duplicate_last(1, 2, "ala ma KotA") == "ala ma KotAtA"
    assert duplicate_last(2, 1, "p@ssW0rd") == "p@ssW0rddd"


def test_duplicate_at():
    assert duplicate_at(7, 2, "ala ma KotA") == "ala ma KKKotA"
    assert duplicate_at(1, 1, "p@ssW0rd") == "p@@ssW0rd"


def test_duplicate_all():
    assert duplicate_all(1, "ala ma KotA") == "aallaa  mmaa  KKoottAA"
    assert duplicate_all(2, "ala ma KotA") == "aaalllaaa   mmmaaa   KKKoootttAAA"
    assert duplicate_all(1, "p@ssW0rd") == "pp@@ssssWW00rrdd"


def test_swap_front():
    assert swap_front("ala ma KotA") == "laa ma KotA"
    assert swap_front("p@ssW0rd") == "@pssW0rd"


def test_swap_back():
    assert swap_back("ala ma KoAt") == "ala ma KotA"
    assert swap_back("p@ssW0rd") == "p@ssW0dr"


def test_swap_chars_at():
    assert swap_chars_at(0, 10, "ala ma KotA") == "Ala ma Kota"
    assert swap_chars_at(0, 1, "p@ssW0rd") == "@pssW0rd"
    assert swap_chars_at(1, 3, "p@ssW0rd") == "pss@W0rd"
    assert swap_chars_at(3, 1, "p@ssW0rd") == "pss@W0rd"


def test_increment_char_ascii_at():
    assert increment_char_ascii_at(5, 3, "ala ma KotA") == "ala md KotA"
    assert increment_char_ascii_at(10, 1, "ala ma KotA") == "ala ma KotB"
    assert increment_char_ascii_at(2, 1, "p@ssW0rd") == "p@tsW0rd"


def test_decrement_char_ascii_at():
    assert decrement_char_ascii_at(1, 1, "ala ma KotA") == "aka ma KotA"
    assert decrement_char_ascii_at(8, 2, "ala ma KotA") == "ala ma KmtA"
    assert decrement_char_ascii_at(1, 1, "p@ssW0rd") == "p?ssW0rd"


def test_join():
    assert join("ala ma KotA", "@ 0La ma psa") == "ala ma KotA@ 0La ma psa"
    assert join("@ 0La ma psa", "pAs$wOrd") == "@ 0La ma psapAs$wOrd"
    assert join("p@ssW0rd", "p?W0rd") == "p@ssW0rdp?W0rd"


def test_interlace():
    assert interlace("ala ma KotA", "@ 0La ma psa") == "@a l0aL am am aK optsAa"
    assert interlace("ala ma KotA", "pAs$wOrd", range(8)) == "paAlsa$ wmOar dKotA"
    assert interlace("p@ssW0rd", "12345", range(1, 6)) == "p1@2s3s4W50rd"
    assert interlace("p@ssW0rd", "123456789", range(1, 10)) == "p1@2s3s4W506r7d89"


def test_gamerize():
    assert gamerize(0, "Ala ma kota") == "4la ma kota"
    assert gamerize(5, "Ala ma kota") == "Ala m@ kota"
    assert gamerize(7, "Ala ma kota") == "Ala ma kota"
    assert gamerize(3, "p@ssW0rd") == "p@s$W0rd"
    assert gamerize(1, "p@ssW0rd") == "p@ssW0rd"
