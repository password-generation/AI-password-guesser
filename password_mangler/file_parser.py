from collections import Counter
from enum import Enum
import pandas as pd
import textract
import spacy
import nltk
import sys
import re
import os

MORFEUSZ_AVAILABLE = True
try:
    import morfeusz2
except ImportError:
    print("morfeusz can't be imported - polish lang is unavailable")
    MORFEUSZ_AVAILABLE = False


# BEFORE YOU RUN THIS CODE:
# nltk.download('wordnet')
# nltk.download('punkt')
# python -m spacy download pl_core_news_lg
# python -m spacy download en_core_web_lg


class Language(Enum):
    ENGLISH = 1
    POLISH = 2


class Phrase:
    def __init__(self, text: str, label: str):
        self.text = text
        self.label = label
        # TODO: Przyda się dodać ujednolicanie etykiet (angielski i polski klasyfikator mają różne nazwy na te same etykiety)

    def __str__(self):
        return self.text + " : " + self.label

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        #TODO wonder what if the same text but different labels?
        return self.text == other.text

    def __hash__(self):
        return hash(self.text)


def extract_text_from_file(file_path: str) -> str:
    """
    Returns plain text read from provided file.
    Supported extensions: pdf, odt, docx, txt
    """
    if file_path.split(".")[-1] != "txt":
        text = textract.process(file_path).decode("utf8")
    else:
        with open(file_path, "rb") as f:
            text = f.read().decode("utf8")
    return text


def clear_text(text: str) -> str:
    """
    Clears the text from punctuation by replacing every character
    specified in the regrex with a space .
    """
    return re.sub("[^A-Za-z0-9ĘęÓóĄąŚśŁłŻżŹźĆćŃń ]+", " ", text)


def recognize_data_strings(text: str, language: Language) -> list[Phrase]:
    """
    Returns list of strings containing data recognized as important
    such as dates, organization names, people's names and surnames and others.
    """
    important_phrases: list[str] = []
    if language == Language.ENGLISH:
        model = "en_core_web_lg"
    elif language == Language.POLISH:
        model = "pl_core_news_lg"
    nlp = spacy.load(model)
    important_text = nlp(text)
    for ent in important_text.ents:
        important_phrases.append(Phrase(ent.text, ent.label_))
    return important_phrases


def lemmatize(words: list[str], language: Language) -> list[str]:
    """
    Creates a list of lemmatized words based on provided list of strings (words).
    """
    if language == Language.ENGLISH:
        lemmatizer = nltk.WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        return lemmatized_words
    elif language == Language.POLISH and MORFEUSZ_AVAILABLE:
        morf = morfeusz2.Morfeusz()
        last_i = -1
        lemmatized_words = []
        for i, _, interp in morf.analyse(" ".join(words)):
            # using last_i number to only save the first interpretation of a word
            if last_i < i:
                lemmatized_words.append(interp[1].split(":")[0])
                last_i = i
    return lemmatized_words


def count_and_sort_words(words: list[str]) -> list[tuple[str, int]]:
    """
    Returns list of touples (word, occurances_count) sorted by occurances in descending order.
    """
    word_count_dict = dict(Counter(words).items())
    sorted_word_count = [
        (word, word_count_dict[word])
        for word in sorted(
            word_count_dict, key=lambda x: word_count_dict[x], reverse=True
        )
    ]
    return sorted_word_count


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
        "labels": [phrase.label for phrase in important_phrases],
    }
    df = pd.DataFrame(data)
    df.to_csv(f"./output/{file_name}.csv")


if __name__ == "__main__":
    # Argument Checking
    if len(sys.argv) != 2:
        print("Provide only one name of file in this directory as program argument")
    file_name = sys.argv[1]

    # Extracting and clearing text
    text = extract_text_from_file(file_name)
    text = clear_text(text)

    # Lemmatiziation and couting of words
    words = text.split()
    lemmatized_words = lemmatize(words, Language.POLISH)
    lemmatized_words = lemmatize(lemmatized_words, Language.ENGLISH)
    sorted_word_count = count_and_sort_words(lemmatized_words)
    save_sorted_words(sorted_word_count, "sorted_tokens_test")

    # Important data recognition
    important_polish_phrases = recognize_data_strings(text, Language.POLISH)
    important_english_phrases = recognize_data_strings(text, Language.ENGLISH)
    save_important_phrases(important_polish_phrases, "important_phrases_polish")
    save_important_phrases(important_english_phrases, "important_phrases_english")
