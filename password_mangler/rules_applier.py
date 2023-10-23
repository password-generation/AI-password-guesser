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
    user_config,
    tokens: list[Token],
    wildcard: bool = True,
    max_length: int = 8,
) -> list[Token]:
    mangled_tokens: list[Token] = tokens
    for epoch in user_config['mangling_schedule']:
        mangled_tokens = filter_tokens_based_on_label(
            mangled_tokens, epoch['labels'], FilterType.OR)

        if wildcard:
            for n in range(1, max_length + 1):
                mangled_tokens.append(Token(WILDCARD_CHAR * n,
                                              [LabelType.WILDCARD]))

        rules = epoch['rules']
        if epoch['type'] == ManglingEpochType.UNARY:
            mangled_tokens = apply_unary_rules_to_tokens(rules, mangled_tokens,
                                                         max_length)
        elif epoch['type'] == ManglingEpochType.BINARY:
            mangled_tokens = apply_binary_rules_to_tokens(rules, mangled_tokens,
                                                          max_length)
        mangled_tokens = list(set(mangled_tokens))

    return mangled_tokens


def filter_tokens_based_on_label(tokens: list[Token], label_types: list[LabelType],
                                 filter_type: FilterType) -> list[Token]:
    new_tokens = list[Token]()
    if filter_type == FilterType.AND:
        for token in tokens:
            include = True
            for label_type in label_types:
                if label_type not in token.labels:
                    include = False
                    break
            if include:
                new_tokens.append(token)
    elif filter_type == FilterType.OR:
        for token in tokens:
            for label_type in label_types:
                if label_type in token.labels:
                    new_tokens.append(token)
                    break
    elif filter_type == FilterType.NOT:
        for token in tokens:
            include = True
            for label_type in label_types:
                if label_type in token.labels:
                    include = False
                    break
            if include:
                new_tokens.append(token)
    return new_tokens
