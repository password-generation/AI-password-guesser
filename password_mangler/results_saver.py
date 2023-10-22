import os
import pandas as pd
from commons import Phrase


def save_important_phrases(important_phrases: list[Phrase], file_name: str) -> None:
    """
    Saves important phrases in csv format into ./output/file_name.csv
    """
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving extracted important phrases
    data = {
        "phrases": [phrase.text for phrase in important_phrases],
        "labels": [phrase.labels for phrase in important_phrases],
    }
    df = pd.DataFrame(data)
    df.to_csv(f"./output/{file_name}.csv")


def save_sorted_words(sorted_words: list[tuple[str, int]], file_name: str) -> None:
    """
    Saves sorted words in csv format into ./output/file_name.csv
    """
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving the tokens and their count
    data = {
        "word": [word for (word, _) in sorted_words],
        "count": [count for (_, count) in sorted_words],
    }
    df = pd.DataFrame(data)
    df.to_csv(f"./output/{file_name}.csv")


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
    # try:
    #     lemmatized_words = lemmatize_phrases(words, Language.POLISH)
    # except MorfeuszNotAvailable as _:
    #     print("Can't lemmatize in polish because morfeusz is not available")

    sorted_word_count = count_and_sort_words(words)
    save_sorted_words(sorted_word_count, "sorted_tokens_test")

    # Important data recognition
    # important_polish_phrases = recognize_data_strings(text, Language.POLISH)
    # save_important_phrases(important_polish_phrases, "important_phrases_polish")

    important_english_phrases = recognize_data_strings(text, Language.ENGLISH)
    save_important_phrases(important_english_phrases, "important_phrases_english")
