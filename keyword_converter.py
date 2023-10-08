import sys
import torch


class EncodedKeyword:
    alphabet = "AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoPpQqRrSsŚśTtUuÓóVvWwXxYyZzŹźŻż0123456789!@#$%^&*()_-+<>?/\\`~ "
    alph_dict = dict((c, i) for i, c in enumerate(alphabet))
    one_hot_encoded_chars = torch.empty((0, len(alphabet)), dtype=torch.float32)
    encoded_chars_numbers = []

    def __init__(self, word: str):
        for char in word:
            encoded_char = torch.zeros((1, len(self.alphabet)))
            encoded_char[0, self.alph_dict[char]] = 1.0
            self.one_hot_encoded_chars = torch.cat(
                (self.one_hot_encoded_chars, encoded_char)
            )
            self.encoded_chars_numbers.append(self.alph_dict[char])

    def __str__(self) -> str:
        return str(self.encoded_chars_numbers)

    def print_matrix(self):
        print(self.one_hot_encoded_chars)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        encoded_word = EncodedKeyword(sys.argv[1])
        print(encoded_word)
        encoded_word.print_matrix()
    else:
        print("Provide one word to encode as an argument.")
