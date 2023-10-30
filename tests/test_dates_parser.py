import pytest
from password_mangler.dates_parser import extract_parse_dates
from password_mangler.commons import LabelType, Token


def test_only_valid():
    date_strings = ["17.12.2001", "7 jul 2001", "5/16/1989", "9 august 1994"]
    tokens = []
    for string in date_strings:
        tokens.append(Token(string, [LabelType.DATE]))

    parsed_dates = extract_parse_dates(tokens)

    assert Token("1712", [LabelType.DATE]) in parsed_dates
    assert Token("707", [LabelType.DATE]) in parsed_dates
    assert Token("01", [LabelType.DATE]) not in parsed_dates
    assert Token("89", [LabelType.DATE]) in parsed_dates
    assert Token("908", [LabelType.DATE]) in parsed_dates


def test_mixed():
    date_strings = ["12.16.2001", "5/16/1989", "7 ju 2001", "19 jun 1984", "jan 17"]
    tokens = []
    for string in date_strings:
        tokens.append(Token(string, [LabelType.DATE]))

    parsed_dates = extract_parse_dates(tokens)

    assert Token("1612", [LabelType.DATE]) in parsed_dates
    assert Token("707", [LabelType.DATE]) not in parsed_dates
    assert Token("01", [LabelType.DATE]) not in parsed_dates
    assert Token("84", [LabelType.DATE]) in parsed_dates
    assert Token("1906", [LabelType.DATE]) in parsed_dates
    assert Token("1701", [LabelType.DATE]) in parsed_dates


def test_only_invalid():
    date_strings = ["15.16.2001", "31/18/1988", "3 fe 2012", "19 maj 1984"]
    tokens = []
    for string in date_strings:
        tokens.append(Token(string, [LabelType.DATE]))

    parsed_dates = extract_parse_dates(tokens)

    assert parsed_dates == []
