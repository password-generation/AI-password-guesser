import re
from collections import defaultdict
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


def parse_text_to_tokens(
    text: str, label: LabelType, stopwords: set[str]
) -> list[Token]:
    tokens = []
    text = text.lower()
    subtokens = re.split(r"\s{2,}", text)  # split if 2 or more whitespaces between
    if not label == LabelType.DATE:
        subtokens = sum(map(lambda s: s.split(), subtokens), [])

    for subtoken in subtokens:
        if subtoken in stopwords:
            continue
        if subtoken == "":
            continue
        tok = Token(subtoken, 1 << label.value)
        tokens.append(tok)
    return tokens


def recognize_data_strings(text: str, language: Language) -> list[Token]:
    """
    Returns list of strings containing data recognized as important
    such as dates, organization names, people's names and surnames and others.
    """
    tokens: list[str] = []
    if language == Language.ENGLISH:
        model = "en_core_web_lg"
        stop_words = set(stopwords.words("english"))
    elif language == Language.POLISH:
        model = "pl_core_news_lg"
        stop_words = set(stopwords.words("polish"))

    nlp = spacy.load(model)
    important_text = nlp(text)
    for ent in important_text.ents:
        try:
            label = LabelType.parse_label(ent.label_)
            new_tokens = parse_text_to_tokens(ent.text, label, stop_words)
            tokens.extend(new_tokens)
        except NotSupportedLabelType as e:
            pass
            # print(e)
    return tokens


def merge_token_duplicates(tokens: list[Token]) -> list[Token]:
    token_dict = defaultdict[str, int](int)
    for token in tokens:
        text = token.text
        binary_mask = token.binary_mask
        token_dict[text] |= binary_mask

    new_tokens = list(map(
        lambda k_v: Token(*k_v),
        token_dict.items()))
    return new_tokens


def lemmatize_tokens(tokens: list[Token], language: Language) -> list[Token]:
    """
    Creates a list of lemmatized words based on provided list of strings (words).
    """
    if language == Language.ENGLISH:
        lemmatizer = nltk.WordNetLemmatizer()
        for i, token in enumerate(tokens):
            text = token.text
            lemmatized_text = lemmatizer.lemmatize(text)
            tokens[i] = Token(lemmatized_text, token.binary_mask)
        return tokens
    elif language == Language.POLISH:
        raise NotImplementedError("Polish lemmatization is not implemented")
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


def email_to_token(match: re.Match[str]) -> list[Token]:
    names = [n for n in match.group(1).split('.') if n]
    orgs = [o for o in match.group(2).split('.') if o]
    locs = [l for l in match.group(3).split('.') if l]
    tokens = [Token(name, LabelType.to_binary_mask([LabelType.PERSON,
                                                    LabelType.EMAIL]))
              for name in names]
    tokens += [Token(org, LabelType.to_binary_mask([LabelType.ORG,
                                                    LabelType.EMAIL]))
               for org in orgs]
    tokens += [Token(loc, LabelType.to_binary_mask([LabelType.LOC,
                                                    LabelType.EMAIL]))
               for loc in locs]
    return tokens


def recognize_email_addresses(text: str) -> list[Token]:
    email_rgx = r"(\b[A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+)\.([A-Z|a-z]{2,7}\b)"
    pattern = re.compile(email_rgx)

    tokens = []
    for m in re.finditer(pattern, text):
        tokens.extend(email_to_token(m))

    return tokens


def count_and_sort_words(words: list[str]) -> list[tuple[str, int]]:
    """
    Returns list of tuples (word, occurrences_count) sorted by occurrences in descending order.
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
    #     lemmatized_words = lemmatize_tokens(words, Language.POLISH)
    # except MorfeuszNotAvailable as _:
    #     print("Can't lemmatize in polish because morfeusz is not available")

    # sorted_word_count = count_and_sort_words(words)
    # print(sorted_word_count)

    # Important data recognition
    # important_polish_tokens = recognize_data_strings(text, Language.POLISH)
    important_english_tokens = recognize_data_strings(text, Language.ENGLISH)
    print(important_english_tokens)
