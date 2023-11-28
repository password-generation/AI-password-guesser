import os
from commons import LabelType, Token


def save_tokens(tokens: list[Token], file_name: str) -> None:
    """
    Saves important tokens in csv format into ./output/file_name.csv
    """
    import pandas as pd
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving extracted important tokens
    tokens = sorted(tokens)
    data = {
        "tokens": [token.text for token in tokens],
        "labels": [LabelType.from_binary_mask(token.binary_mask)
                   for token in tokens],
    }
    df = pd.DataFrame(data)
    df.to_csv(f"./output/{file_name}")

def save_result_to_txt(tokens: list[Token], file_name: str) -> None:
    """
    Saves result wordlist in txt format
    """
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving the result passwords
    tokens = sorted(tokens)
    with open(f"./output/{file_name}", "w") as file:
        file.writelines([token.text + "\n" for token in tokens])


def save_sorted_words(sorted_words: list[tuple[str, int]], file_name: str) -> None:
    """
    Saves sorted words in csv format into ./output/file_name.csv
    """
    import pandas as pd
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving the tokens and their count
    data = {
        "word": [word for (word, _) in sorted_words],
        "count": [count for (_, count) in sorted_words],
    }
    df = pd.DataFrame(data)
    df.to_csv(f"./output/{file_name}")


if __name__ == "__main__":
    import sys
    from file_reader import extract_text_from_file, clear_text
    from commons import *
    from text_parser import *

    # Argument Checking
    if len(sys.argv) != 2:
        print("Provide only one name of file in this directory as program argument")
    file_name = sys.argv[1]

    # Extracting and clearing text
    text = extract_text_from_file(file_name)
    text = clear_text(text)

    # Lemmatiziation and couting of words
    words = text.split()
    # lemmatized_words = lemmatize_tokens(words, Language.POLISH)

    sorted_word_count = count_and_sort_words(words)
    save_sorted_words(sorted_word_count, "sorted_tokens_test.csv")

    # Important data recognition
    # important_polish_tokens = recognize_data_strings(text, Language.POLISH)
    # save_tokens(important_polish_tokens, "tokens_polish")

    important_english_tokens = recognize_data_strings(text, Language.ENGLISH)
    save_tokens(important_english_tokens, "tokens_english.csv")
