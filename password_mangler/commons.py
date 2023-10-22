from enum import Enum


WILDCARD_CHAR = '\1'

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
    PERSON = 1
    ORG = 2
    LOC = 3
    DATE = 4
    WILDCARD = 5

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


class Token:
    def __init__(self, text: str, labels: list[LabelType]):
        self.text = text
        self.labels = list(set(labels))

    def add_new_labels(self, new_labels: list[LabelType]) -> None:
        self.labels.extend(new_labels)
        self.labels = list(set(self.labels))

    def __str__(self) -> str:
        if LabelType.WILDCARD in self.labels:
            replaced_text = self.text.replace(WILDCARD_CHAR, '*')
            return f"{replaced_text} : {self.labels}"
        return f"{self.text} : {self.labels}"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.text)

    def __eq__(self, other) -> bool:
        return self.text == other.text

    def __lt__(self, other) -> bool:
        return self.text < other.text
