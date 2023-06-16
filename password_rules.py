def lowercase(s: str):
    return s.lower()


def capitalize(s: str):
    return s.capitalize()


def toggle_case(s: str):
    return "".join(c.upper() if c.islower() else c.lower() for c in s)


def reverse(s: str):
    return "".join(reversed(s))


def duplicate(s: str, n: int = 1):
    return s * n


def rotate_left(s: str, i: int = 1):
    return s[i:] + s[:i]


def join(s1: str, s2: str):
    return s1 + s2


def truncate_left(s: str, i: int = 1):
    return s[i:]


def delete_at(s: str, i: int):
    return s[:i] + s[i + 1 :]


def omit_range(s: str, i: int, n: int):
    return s[:i] + s[i + n :]


def overwrite_at(s: str, i: int, c: str):
    return s[:i] + c + s[i + 1 :]


def replace(s: str, old: str, new: str):
    return s.replace(old, new)


def duplicate_at(s: str, i: int, n: int):
    return s[:i] + (s[i] * n) + s[i + 1 :]


def duplicate_all(s: str, n: int):
    return "".join(c * n for c in s)


def swap_chars_at(s: str, i: int, j: int):
    if i > j:
        i, j = j, i
    return s[:i] + s[j] + s[i + 1 : j] + s[i] + s[j + 1 :]


def increment_char_ascii_at(s: str, i: int, n: int):
    return s[:i] + chr(ord(s[i]) + n) + s[i + 1 :]


def decrement_char_ascii_at(s: str, i: int, n: int):
    return s[:i] + chr(ord(s[i]) - n) + s[i + 1 :]


def duplicate_first(s: str, i: int, n: int = 2):
    return (s[:i] * n) + s[i:]


def duplicate_last(s: str, i: int, n: int = 2):
    return s[:-i] + (s[-i:] * n)


def interlace(s1: str, s2: str, idxs: list[int]):
    assert len(s2) == len(idxs)
    s3 = ""
    i = 0
    for j, c in zip(idxs, s2):
        s3 += s1[i:j] + c
        i = j
    s3 += s1[i:]
    return s3

def nothing(s: str):
    return s

def uppercase(s: str):
    return s.upper()

def invert_capitalize(s: str):
    return s.capitalize().swapcase()

def toggle_at(s: str, i: int):
    return s[:i] + s[i].swapcase() + s[i+1:]

def reflect(s: str):
    return s + s[::-1]

def rotate_right(s: str, i: int = 1):
    return  s[len(s) - i:] + s[: len(s) - i]

def truncate_right(s: str, i: int = 1):
    return s[:len(s) - i]

def extract_range(s: str, i: int, n: int):
    pass

s = "p@ssW0rd"
print(truncate_right(s, 1))