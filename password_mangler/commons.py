from enum import Enum


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


class Phrase:
    def __init__(self, text: str, labels: list[LabelType]):
        self.text = text
        self.labels = list(set(labels))

    def add_new_labels(self, new_labels: list[LabelType]) -> None:
        self.labels.extend(new_labels)
        self.labels = list(set(self.labels))

    def __str__(self):
        return f"'{self.text}' : {self.labels}"

    def __repr__(self):
        return str(self)

