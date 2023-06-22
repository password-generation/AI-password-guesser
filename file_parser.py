from collections import Counter
from typing import List, Tuple
from enum import Enum
import pandas as pd
import morfeusz2
import textract
import spacy
import nltk
import sys
import re
import os


# BEFORE YOU RUN THIS CODE:
# nltk.download('wordnet') 
# nltk.download('punkt') 
# python -m spacy download pl_core_news_lg
# python -m spacy download en_core_web_lg


class Language(Enum):
    ENGLISH = 1
    POLISH  = 2

def extract_text_from_file(file_path: str) -> str:
    """ 
    Returns plain text read from provided file.
    Supported extensions: pdf, odt, docx, txt
    """
    if file_path.split(".")[-1] != "txt":
        text = textract.process(file_path).decode('utf8')
    else:
        with open(file_path, "rb") as f:
            text = f.read().decode('utf8')
    return text

def clear_text(text: str) -> str:
    """ 
    Clears the text from punctuation by replacing every character 
    specified in the regrex with a space .
    """
    return re.sub('[^A-Za-z0-9ĘęÓóĄąŚśŁłŻżŹźĆćŃń ]+', ' ', text)

def recognize_data_strings(text: str, language: Language) -> list:
    """
    Returns list of strings containing data recognized as important
    such as dates, organization names, people's names and surnames and others.
    """
    # TODO We might want to return not only the phrases but the categories as well
    important_phrases = []
    if language == Language.ENGLISH:
        model = "en_core_web_lg"
    elif language == Language.POLISH:
        model = "pl_core_news_lg"
    nlp = spacy.load(model)
    important_text = nlp(text)
    for ent in important_text.ents:
        important_phrases.append(ent.text)
    return important_phrases

def lemmatize(words: List[str], language: Language) -> List[str]:
    """
    Creates a list of lemmatized words based on provided list of strings (words). 
    """
    if language == Language.ENGLISH:
        lemmatizer = nltk.WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        return lemmatized_words
    elif language == Language.POLISH:
        morf = morfeusz2.Morfeusz() 
        last_i = -1
        lemmatized_words = []
        for i, _, interp in morf.analyse(' '.join(words)):
            # using last_i number to only save the first interpretation of a word
            if last_i < i:
                lemmatized_words.append(interp[1].split(":")[0])
                last_i = i
    return lemmatized_words

def count_and_sort_words(words: List[str]) -> List[Tuple[int, str]]:
    """
    Returns list of touples (word, occurances_count) sorted by occurances in descending order.
    """
    word_count_dict = dict(Counter(words).items())
    sorted_word_count = [(word, word_count_dict[word]) for word in sorted(word_count_dict, key=word_count_dict.get, reverse=True)]
    return sorted_word_count

def save_sorted_words(counted_words: List[Tuple[str, int]], file_name: str) -> None:
    """
    Saves counted words in csv format into ./output/file_name.csv
    """
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving the tokens and their count
    data = {'word': [word for (word, _) in counted_words], 'count': [count for (_, count) in counted_words]}
    df = pd.DataFrame(data)
    df.to_csv(f"./output/{file_name}.csv")

def save_important_phrases(important_phrases: List[str], file_name: str) -> None:
    """
    Saves important phrases in csv format into ./output/file_name.csv
    """
    # Creating output folder if it does not exist
    if not os.path.exists("./output"):
        os.makedirs("./output")
    # Saving extracted important phrases
    data = {'phrases': important_phrases}
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
