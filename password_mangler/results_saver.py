import os
from commons import LabelType, Token


def save_tokens(tokens: list[Token], file_name: str) -> None:
    """
    Saves important tokens in csv format into ./output/file_name.csv
    """
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving extracted important tokens
    tokens = sorted(tokens)
    with open(f"./output/{file_name}", "w") as file:
        file.writelines([f"{token.text},{LabelType.from_binary_mask(token.binary_mask)}\n"
                         for token in tokens])


def save_result_to_txt(tokens: list[Token], file_name: str) -> None:
    """
    Saves result wordlist in txt format
    """
    tokens = sorted(tokens)
    with open(f"{file_name}", "w") as file:
        file.writelines([token.text + "\n" for token in tokens])
