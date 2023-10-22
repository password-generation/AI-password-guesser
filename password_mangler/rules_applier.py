from typing import Callable
from password_rules import *
from commons import *


UnStrRule = Callable[[str], str]
BinStrRule = Callable[[str, str], str]


def apply_unary_rules_to_phrases(
    rules: list[UnStrRule],
    phrases: list[Phrase],
) -> list[Phrase]:
    phrases_after_applying_rules: list[Phrase] = []
    for phrase in phrases:
        for rule in rules:
            new_string = rule(phrase.text)
            new_phrase = Phrase(new_string, phrase.labels[:])
            phrases_after_applying_rules.append(new_phrase)
    return phrases_after_applying_rules


def apply_binary_rules_to_phrases(
    rules: list[BinStrRule],
    phrases: list[Phrase],
) -> list[Phrase]:
    strings_after_applying_rules: list[Phrase] = []
    for phrase1 in phrases:
        for phrase2 in phrases:
            if phrase1.text == phrase2.text:
                continue
            for rule in rules:
                new_string = rule(phrase1.text, phrase2.text)
                new_labels = phrase1.labels + phrase2.labels
                new_phrase = Phrase(new_string, new_labels)
                strings_after_applying_rules.append(new_phrase)
    return strings_after_applying_rules


def mangle_phrases(
    unary_rules: list[UnStrRule],
    binary_rules: list[BinStrRule],
    mangling_schedule: list[ManglingEpochType],
    phrases: list[Phrase],
) -> list[Phrase]:
    mangled_phrases: list[Phrase] = phrases
    for mangling_epoch_type in mangling_schedule:
        if mangling_epoch_type == ManglingEpochType.UNARY:
            mangled_phrases = apply_unary_rules_to_phrases(unary_rules, mangled_phrases)
        elif mangling_epoch_type == ManglingEpochType.BINARY:
            mangled_phrases = apply_binary_rules_to_phrases(binary_rules, mangled_phrases)
        mangled_phrases = list(set(mangled_phrases))
    return mangled_phrases


if __name__ == "__main__":
    phrases = [Phrase("piotr", [LabelType.PERSON]),
               Phrase("2001", [LabelType.DATE])]
    unary_rules = [capitalize, toggle_case]
    binary_rules = [join, interlace]
    mangling_schedule = [ManglingEpochType.UNARY] * 2 + [ManglingEpochType.BINARY]
    mangled_phrases = mangle_phrases(
        unary_rules,
        binary_rules,
        mangling_schedule,
        phrases
    )
    print(mangled_phrases)
