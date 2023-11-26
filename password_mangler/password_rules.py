def nothing(s: str) -> str:
    return s


def lowercase(s: str) -> str:
    return s.lower()


def uppercase(s: str) -> str:
    return s.upper()


def capitalize(s: str) -> str:
    return s.capitalize()


def invert_capitalize(s: str) -> str:
    return s.capitalize().swapcase()


def toggle_case(s: str) -> str:
    return s.swapcase()


def toggle_at(i: int, s: str) -> str:
    if i < len(s):
        return s[:i] + s[i].swapcase() + s[i + 1 :]
    return s


def reverse(s: str) -> str:
    return s[::-1]


def duplicate(n: int, s: str) -> str:
    return s * (n + 1)


def reflect(s: str) -> str:
    return s + s[::-1]


def rotate_left(i: int, s: str) -> str:
    return s[i:] + s[:i]


def rotate_right(i: int, s: str) -> str:
    return s[len(s) - i :] + s[: len(s) - i]


def cut_start(i: int, s: str) -> str:
    return s[i:]


def cut_end(i: int, s: str) -> str:
    if i < len(s):
        return s[: len(s) - i]
    return s


def delete_at(i: int, s: str) -> str:
    return s[:i] + s[i + 1 :]


def extract_range(i: int, n: int, s: str) -> str:
    return s[i : i + n]


def omit_range(i: int, n: int, s: str) -> str:
    return s[:i] + s[i + n :]


def insert_at(i: int, c: str, s: str) -> str:
    return s[:i] + c + s[i:]


def overwrite_at(i: int, c: str, s: str) -> str:
    return s[:i] + c + s[i + 1 :]


def replace(old: str, new: str, s: str) -> str:
    return s.replace(old, new)


def purge(c: str, s: str) -> str:
    return s.replace(c, "")


def duplicate_first(n: int, i: int, s: str) -> str:
    return s[:i] * (n + 1) + s[i:]


def duplicate_last(n: int, i: int, s: str) -> str:
    return s[:-i] + s[-i:] * (n + 1)


def duplicate_at(i: int, n: int, s: str) -> str:
    return s[:i] + s[i] * (n + 1) + s[i + 1 :]


def duplicate_all(n: int, s: str) -> str:
    return "".join(c * (n + 1) for c in s)


def swap_front(s: str) -> str:
    return s[1] + s[0] + s[2:]


def swap_back(s: str) -> str:
    return s[:-2] + s[-1] + s[-2]


def swap_chars_at(i: int, j: int, s: str) -> str:
    if i > j:
        i, j = j, i
    return s[:i] + s[j] + s[i + 1 : j] + s[i] + s[j + 1 :]


def increment_char_ascii_at(i: int, n: int, s: str) -> str:
    return s[:i] + chr(ord(s[i]) + n) + s[i + 1 :]


def decrement_char_ascii_at(i: int, n: int, s: str) -> str:
    return s[:i] + chr(ord(s[i]) - n) + s[i + 1 :]


def join(s1: str, s2: str) -> str:
    return s1 + s2


def interlace(s1: str, s2: str, idxs: list[int] | None = None) -> str:
    if idxs is None:
        idxs = list(range(len(s2)))
    s3 = ""
    i = 0
    for j, c in zip(idxs, s2):
        s3 += s1[i:j] + c
        i = j
    s3 += s1[i:]
    return s3


GAMER_TRANSLATION = {
    "A": "4",
    "a": "@",
    "B": "8",
    "C": "(",
    "c": "(",
    "E": "3",
    "e": "3",
    "G": "6",
    "g": "9",
    "H": "#",
    "h": "#",
    "I": "1",
    "i": "!",
    "O": "0",
    "o": "0",
    "S": "$",
    "s": "$",
    "T": "7",
    "t": "+",
    "U": "v",
    "u": "v",
    "Z": "2",
    "z": "2",
}


def gamerize(i: int, s: str):  # if we dont have a mapping we dont change the symbol
    if i < len(s):
        c = GAMER_TRANSLATION.get(s[i], s[i])
        return s[:i] + c + s[i + 1 :]
    return s
