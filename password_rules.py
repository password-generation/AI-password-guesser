def nothing(s: str):
    return s


def lowercase(s: str):
    return s.lower()


def uppercase(s: str):
    return s.upper()


def capitalize(s: str):
    return s.capitalize()


def invert_capitalize(s: str):
    return s.capitalize().swapcase()


def toggle_case(s: str):
    return "".join(c.upper() if c.islower() else c.lower() for c in s)


def toggle_at(s: str, i: int):
    return s[:i] + s[i].swapcase() + s[i + 1 :]


def reverse(s: str):
    return "".join(reversed(s))


def duplicate(s: str, n: int = 1):
    return s * (n + 1)


def reflect(s: str):
    return s + s[::-1]


def rotate_left(s: str, i: int = 1):
    return s[i:] + s[:i]


def rotate_right(s: str, i: int = 1):
    return s[len(s) - i :] + s[: len(s) - i]


def truncate_left(s: str, i: int = 1):
    return s[i:]


def truncate_right(s: str, i: int = 1):
    return s[: len(s) - i]


def delete_at(s: str, i: int):
    return s[:i] + s[i + 1 :]


def extract_range(s: str, i: int, n: int):
    return s[i : i + n]


def omit_range(s: str, i: int, n: int):
    return s[:i] + s[i + n :]


def insert_at(s: str, i: int, c: str):
    return s[:i] + c + s[i:]


def overwrite_at(s: str, i: int, c: str):
    return s[:i] + c + s[i + 1 :]


def replace(s: str, old: str, new: str):
    return s.replace(old, new)


def purge(s: str, c: str):
    return s.replace(c, "")


def duplicate_first(s: str, n: int = 1, i: int = 1):
    return s[:i] * (n + 1) + s[i:]


def duplicate_last(s: str, n: int = 1, i: int = 1):
    return s[:-i] + s[-i:] * (n + 1)


def duplicate_at(s: str, i: int, n: int = 1):
    return s[:i] + s[i] * (n + 1) + s[i + 1 :]


def duplicate_all(s: str, n: int = 1):
    return "".join(c * (n + 1) for c in s)


def swap_front(s: str):
    return s[1] + s[0] + s[2:]


def swap_back(s: str):
    return s[:-2] + s[-1] + s[-2]


def swap_chars_at(s: str, i: int, j: int):
    if i > j:
        i, j = j, i
    return s[:i] + s[j] + s[i + 1 : j] + s[i] + s[j + 1 :]


def increment_char_ascii_at(s: str, i: int, n: int = 1):
    return s[:i] + chr(ord(s[i]) + n) + s[i + 1 :]


def decrement_char_ascii_at(s: str, i: int, n: int = 1):
    return s[:i] + chr(ord(s[i]) - n) + s[i + 1 :]


def join(s1: str, s2: str):
    return s1 + s2


def interlace(s1: str, s2: str, idxs: list[int] | None = None):
    if idxs is None:
        idxs = range(len(s2))
    s3 = ""
    i = 0
    for j, c in zip(idxs, s2):
        s3 += s1[i:j] + c
        i = j
    s3 += s1[i:]
    return s3
