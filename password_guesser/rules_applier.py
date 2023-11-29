from typing import Callable
from tqdm import tqdm
from password_rules import *
from commons import LabelType, ManglingEpochType, FilterType, Token, WILDCARD_CHAR


UnStrRule = Callable[[str], str]
BinStrRule = Callable[[str, str], str]


def apply_unary_rules_to_tokens(
    rules: list[UnStrRule],
    tokens: set[Token],
    max_length: int,
    progress_bar,
) -> set[Token]:
    tokens_after_applying_rules = set[Token]()
    try:
        for token in tokens:
            for rule in rules:
                new_string = rule(token.text)
                if len(new_string) > max_length:
                    new_string = new_string[:max_length]

                new_token = Token(new_string, token.binary_mask)
                tokens_after_applying_rules.add(new_token)
                progress_bar.update()
    except KeyboardInterrupt:
        print("Early stopping")

    return tokens_after_applying_rules


def apply_binary_rules_to_tokens(
    rules: list[BinStrRule],
    tokens: set[Token],
    max_length: int,
    progress_bar=None,
) -> set[Token]:
    strings_after_applying_rules = set[Token]()
    try:
        for token1 in tokens:
            for token2 in tokens:
                if token1.text == token2.text:
                    continue
                for rule in rules:
                    new_string = rule(token1.text, token2.text)
                    if len(new_string) > max_length:
                        new_string = new_string[:max_length]

                    new_binary_mask = token1.binary_mask | token2.binary_mask
                    new_token = Token(new_string, new_binary_mask)
                    strings_after_applying_rules.add(new_token)
                    if progress_bar:
                        progress_bar.update()
    except KeyboardInterrupt:
        print("Early stopping")

    return strings_after_applying_rules


def generate_wildcard_tokens(max_length: int) -> list[Token]:
    wildcard_binary_mask = 1 << LabelType.WILDCARD.value
    tokens = [Token(WILDCARD_CHAR * n, wildcard_binary_mask)
              for n in range(1, max_length + 1)]
    return set(tokens)


def mangle_tokens(
    user_config,
    tokens: list[Token],
    wildcard: bool = False,
    max_length: int = 8,
) -> list[Token]:
    mangled_tokens: set[Token] = set(tokens)
    epochs = user_config['mangling_schedule']

    for i, epoch in enumerate(epochs):
        mangled_tokens = filter_tokens_based_on_label(
            mangled_tokens, epoch['labels'], FilterType.OR)
        mangled_tokens = set(mangled_tokens)

        rules = epoch['rules']
        if epoch['type'] == ManglingEpochType.UNARY:
            total_num = len(mangled_tokens) * len(rules)
            progress_bar = tqdm(desc=f'[{i+1}/{len(epochs)}]  Unary mangling epoch',
                                total=total_num)

            mangled_tokens = apply_unary_rules_to_tokens(rules, mangled_tokens,
                                                         max_length, progress_bar)
            progress_bar.close()
        elif epoch['type'] == ManglingEpochType.BINARY:
            total_num = len(rules) * len(mangled_tokens) * len(mangled_tokens)
            progress_bar = tqdm(desc=f'[{i+1}/{len(epochs)}] Binary mangling epoch',
                                total=total_num)
            mangled_tokens = apply_binary_rules_to_tokens(rules, mangled_tokens,
                                                          max_length, progress_bar)
            progress_bar.close()

    return list(mangled_tokens)


def filter_tokens_based_on_label(tokens: list[Token], label_types: list[LabelType],
                                 filter_type: FilterType) -> list[Token]:
    binary_mask = LabelType.to_binary_mask(label_types)
    if filter_type == FilterType.AND:
        return list(filter(
            lambda tok: tok.binary_mask == binary_mask,
            tokens))
    elif filter_type == FilterType.OR:
        return list(filter(
            lambda tok: (tok.binary_mask & binary_mask) != 0,
            tokens))
    elif filter_type == FilterType.NOT:
        return list(filter(
            lambda tok: (tok.binary_mask & binary_mask) == 0,
            tokens))
