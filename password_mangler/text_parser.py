import re
from commons import Language, LabelType
from collections import Counter
import spacy
import nltk
from nltk.corpus import stopwords
from commons import *


MORFEUSZ_AVAILABLE = True
try:
    import morfeusz2
except ImportError:
    print("morfeusz can't be imported - polish lang is unavailable")
    MORFEUSZ_AVAILABLE = False


# BEFORE YOU RUN THIS CODE:
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('stopwords')
# python -m spacy download pl_core_news_lg
# python -m spacy download en_core_web_lg


def parse_label(text: str) -> LabelType:
    match text:
        case 'PERSON' | 'persName':
            return LabelType.PERSON
        case 'ORG' | 'orgName':
            return LabelType.ORG
        case 'LOC' | 'geogName' | 'placeName':
            return LabelType.LOC
        case 'DATE' | 'date':
            return LabelType.DATE
        case _:
            raise NotSupportedLabelType(text)


def parse_text_to_phrases(text: str, label: LabelType, stopwords: set[str]) -> list[Phrase]:
    phrases = []
    text = text.lower()
    tokens = re.split(r'\s{2,}', text)
    if not label == LabelType.DATE:
        tokens = sum(map(lambda s: s.split(), tokens), [])

    for token in tokens:
        if token in stopwords:
            continue
        if token == '':
            continue
        phr = Phrase(token, [label])
        phrases.append(phr)
    return phrases


def recognize_data_strings(text: str, language: Language) -> list[Phrase]:
    """
    Returns list of strings containing data recognized as important
    such as dates, organization names, people's names and surnames and others.
    """
    important_phrases: list[str] = []
    if language == Language.ENGLISH:
        model = "en_core_web_lg"
        stop_words = set(stopwords.words('english'))
    elif language == Language.POLISH:
        model = "pl_core_news_lg"
        stop_words = set(stopwords.words('polish'))

    nlp = spacy.load(model)
    important_text = nlp(text)
    for ent in important_text.ents:
        try:
            label = parse_label(ent.label_)
            new_phrases = parse_text_to_phrases(ent.text, label, stop_words)
            important_phrases.extend(new_phrases)
        except NotSupportedLabelType as e:
            pass
            # print(e)
    return important_phrases


def merge_phrase_duplicates(phrases: list[Phrase]) -> list[Phrase]:
    phrase_dict = dict[str, Phrase]()
    for phrase in phrases:
        text = phrase.text
        if text in phrase_dict:
            old_phrase = phrase_dict[text]
            old_phrase.add_new_labels(phrase.labels)
        else:
            phrase_dict[text] = phrase
    return list(phrase_dict.values())


def lemmatize_phrases(phrases: list[Phrase], language: Language) -> list[Phrase]:
    """
    Creates a list of lemmatized words based on provided list of strings (words).
    """
    if language == Language.ENGLISH:
        lemmatizer = nltk.WordNetLemmatizer()
        for phrase in phrases:
            text = phrase.text
            lemmatized_text = lemmatizer.lemmatize(text)
            phrase.text = lemmatized_text
        return phrases
    elif language == Language.POLISH:
        raise NotImplementedError('Polish lemmatization is not implemented')
        if not MORFEUSZ_AVAILABLE:
            raise MorfeuszNotAvailable()
        morf = morfeusz2.Morfeusz()
        last_i = -1
        lemmatized_words = []
        for i, _, interp in morf.analyse(" ".join(words)):
            # using last_i number to only save the first interpretation of a word
            if last_i < i:
                lemmatized_words.append(interp[1].split(":")[0])
                last_i = i
        return lemmatized_words


def filter_phrases_based_on_label(phrases: list[Phrase], label_types: list[LabelType],
                                  filter_type: FilterType) -> list[Phrase]:
    new_phrases = list[Phrase]()
    if filter_type == FilterType.AND:
        for phrase in phrases:
            include = True
            for label_type in label_types:
                if label_type not in phrase.labels:
                    include = False
                    break
            if include:
                new_phrases.append(phrase)
    elif filter_type == FilterType.OR:
        for phrase in phrases:
            for label_type in label_types:
                if label_type in phrase.labels:
                    new_phrases.append(phrase)
                    break
    elif filter_type == FilterType.NOT:
        for phrase in phrases:
            include = True
            for label_type in label_types:
                if label_type in phrase.labels:
                    include = False
                    break
            if include:
                new_phrases.append(phrase)
    return new_phrases


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


if __name__ == "__main__":
    import sys
    from file_reader import extract_text_from_file, clear_text
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

    # sorted_word_count = count_and_sort_words(words)
    # print(sorted_word_count)

    # Important data recognition
    # important_polish_phrases = recognize_data_strings(text, Language.POLISH)
    important_english_phrases = recognize_data_strings(text, Language.ENGLISH)
    print(important_english_phrases)
