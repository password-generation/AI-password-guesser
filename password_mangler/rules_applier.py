from typing import Callable
from password_rules import *
from commons import *


UnStrRule = Callable[[str], str]
BinStrRule = Callable[[str, str], str]


def apply_unary_rules_to_tokens(
    rules: list[UnStrRule],
    tokens: list[Token],
    max_length: int,
) -> list[Token]:
    tokens_after_applying_rules: list[Token] = []
    for token in tokens:
        for rule in rules:
            new_string = rule(token.text)
            if len(new_string) > max_length:
                new_string = new_string[:max_length]

            new_token = Token(new_string, token.labels[:])
            tokens_after_applying_rules.append(new_token)

    return tokens_after_applying_rules


def apply_binary_rules_to_tokens(
    rules: list[BinStrRule],
    tokens: list[Token],
    max_length: int,
) -> list[Token]:
    strings_after_applying_rules: list[Token] = []
    for token1 in tokens:
        for token2 in tokens:
            if token1.text == token2.text:
                continue
            for rule in rules:
                new_string = rule(token1.text, token2.text)
                if len(new_string) > max_length:
                    new_string = new_string[:max_length]

                new_labels = token1.labels + token2.labels
                new_token = Token(new_string, new_labels)
                strings_after_applying_rules.append(new_token)

    return strings_after_applying_rules


def mangle_tokens(
    unary_rules: list[UnStrRule],
    binary_rules: list[BinStrRule],
    mangling_schedule: list[ManglingEpochType],
    tokens: list[Token],
    wildcard: bool = True,
    max_length: int = 8,
) -> list[Token]:
    mangled_tokens: list[Token] = tokens
    for mangling_epoch_type in mangling_schedule:
        if wildcard:
            for n in range(1, max_length + 1):
                mangled_tokens.append(Token(WILDCARD_CHAR * n,
                                              [LabelType.WILDCARD]))

        if mangling_epoch_type == ManglingEpochType.UNARY:
            mangled_tokens = apply_unary_rules_to_tokens(unary_rules, mangled_tokens,
                                                           max_length)
        elif mangling_epoch_type == ManglingEpochType.BINARY:
            mangled_tokens = apply_binary_rules_to_tokens(binary_rules, mangled_tokens,
                                                            max_length)
        mangled_tokens = list(set(mangled_tokens))
    return mangled_tokens


if __name__ == "__main__":
    tokens = [Token("piotr", [LabelType.PERSON]),
               Token("2001", [LabelType.DATE])]
    unary_rules = [capitalize, toggle_case]
    binary_rules = [join, interlace]
    mangling_schedule = [ManglingEpochType.UNARY] * 2 + [ManglingEpochType.BINARY]
    mangled_tokens = mangle_tokens(
        unary_rules,
        binary_rules,
        mangling_schedule,
        tokens
    )
    print(mangled_tokens)
