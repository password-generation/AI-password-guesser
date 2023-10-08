from typing import Callable
from enum import Enum
from password_rules import *


UnStrRule = Callable[[str], str]
BinStrRule = Callable[[str, str], str]


def apply_unary_rules_to_strings(
    rules: list[UnStrRule],
    strings: list[str],
) -> list[str]:
    strings_after_applying_rules: list[str] = []
    for string in strings:
        for rule in rules:
            new_string = rule(string)
            strings_after_applying_rules.append(new_string)
    return strings_after_applying_rules


def apply_binary_rules_to_strings(
    rules: list[BinStrRule],
    strings: list[str],
) -> list[str]:
    strings_after_applying_rules: list[str] = []
    for string1 in strings:
        for string2 in strings:
            if string1 == string2:
                continue
            for rule in rules:
                new_string = rule(string1, string2)
                strings_after_applying_rules.append(new_string)
    return strings_after_applying_rules


class ManglingEpochType(Enum):
    UNARY = 1
    BINARY = 2


def mangle_strings(
    unary_rules: list[UnStrRule],
    binary_rules: list[BinStrRule],
    strings: list[str],
    mangling_schedule: list[ManglingEpochType],
) -> list[str]:
    mangled_strings: list[str] = strings
    for mangling_epoch_type in mangling_schedule:
        if mangling_epoch_type == ManglingEpochType.UNARY:
            mangled_strings = apply_unary_rules_to_strings(unary_rules, mangled_strings)
        elif mangling_epoch_type == ManglingEpochType.BINARY:
            mangled_strings = apply_binary_rules_to_strings(binary_rules, mangled_strings)
        mangled_strings = list(set(mangled_strings))
    return mangled_strings


if __name__ == "__main__":
    strings = ["piotr", "2001"]
    unary_rules = [capitalize, toggle_case]
    binary_rules = [join, interlace]
    mangling_schedule = [ManglingEpochType.UNARY] * 2 + [ManglingEpochType.BINARY]
    mangled_strings = mangle_strings(
        unary_rules,
        binary_rules,
        strings,
        mangling_schedule
    )
    print(mangled_strings)
