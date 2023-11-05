from enum import Enum
from typing import NamedTuple


WILDCARD_CHAR = '\t'
CHARMAP_PATH = 'DATA/AE_char_map.pickle'
MODEL_PATH = 'DATA/AE_based_Noise_a4_ls128_hn4_al8/'


class MorfeuszNotAvailable(Exception):
    ...

class NotSupportedLabelType(Exception):
    ...


class Language(Enum):
    ENGLISH = 1
    POLISH = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class LabelType(Enum):
    PERSON = 0
    ORG = 1
    LOC = 2
    DATE = 3
    WILDCARD = 4
    EMAIL = 5

    @staticmethod
    def to_binary_mask(labels: list['LabelType']) -> int:
        binary_mask = 0
        for label in labels:
            binary_mask |= 1 << label.value
        return binary_mask

    @staticmethod
    def from_binary_mask(binary_mask: int) -> list['LabelType']:
        labels = []
        for label in LabelType:
            if binary_mask & (1 << label.value):
                labels.append(label)
        return labels

    @staticmethod
    def remove_label_from_binary_mask(label: 'LabelType', binary_mask: int) -> int:
        label_bin = 1 << label.value
        return binary_mask - label_bin

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class ManglingEpochType(Enum):
    UNARY = 1
    BINARY = 2


class FilterType(Enum):
    AND = 1
    OR = 2
    NOT = 3


Token = NamedTuple('Token', text=str, binary_mask=int)


def token_to_str(token: Token) -> str:
    labels = LabelType.from_binary_mask(token.binary_mask)
    if (1 << LabelType.WILDCARD.value) & token.binary_mask:
        replaced_text = token.text.replace(WILDCARD_CHAR, '*')
        return f"{replaced_text:12} : {labels}"
    return f"{token.text:12} : {labels}"
