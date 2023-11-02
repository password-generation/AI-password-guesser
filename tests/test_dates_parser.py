import pytest
from password_mangler.dates_parser import extract_parse_dates
from password_mangler.commons import LabelType, Token

MASK = LabelType.to_binary_mask([LabelType.DATE])


def test_only_valid():
    date_strings = ["17.12.2001", "7 jul 2001", "5/16/1989", "9 august 1994"]
    tokens = []
    for string in date_strings:
        tokens.append(Token(string, MASK))

    parsed_dates = extract_parse_dates(tokens)

    assert Token("1712", MASK) in parsed_dates
    assert Token("0707", MASK) in parsed_dates
    assert Token("01", MASK) in parsed_dates
    assert Token("89", MASK) in parsed_dates
    assert Token("0908", MASK) in parsed_dates


def test_mixed():
    date_strings = ["12.16.2001", "5/16/1989", "7 ju 2001", "19 jun 1984", "jan 17"]
    tokens = []
    for string in date_strings:
        tokens.append(Token(string, MASK))

    parsed_dates = extract_parse_dates(tokens)

    assert Token("1612", MASK) in parsed_dates
    assert Token("0707", MASK) not in parsed_dates
    assert Token("01", MASK) in parsed_dates
    assert Token("84", MASK) in parsed_dates
    assert Token("1906", MASK) in parsed_dates
    assert Token("1701", MASK) in parsed_dates


def test_only_invalid():
    date_strings = ["15.16.2001", "31/18/1988", "3 fe 2012", "19 majj 1984"]
    tokens = []
    for string in date_strings:
        tokens.append(Token(string, MASK))

    parsed_dates = extract_parse_dates(tokens)

    assert parsed_dates == []


test_only_valid()
test_mixed()
test_only_invalid()
