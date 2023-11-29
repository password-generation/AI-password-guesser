import re
from tqdm import tqdm
from collections import defaultdict
from commons import Language, LabelType
from collections import Counter
from commons import NotSupportedLabelType, Language, LabelType, Token


def parse_label(text: str) -> LabelType:
    match text:
        case "PERSON" | "persName":
            return LabelType.PERSON
        case "ORG" | "orgName":
            return LabelType.ORG
        case "LOC" | "geogName" | "placeName":
            return LabelType.LOC
        case "DATE" | "date":
            return LabelType.DATE
        case _:
            raise NotSupportedLabelType(text)


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


def tokenize_text(text: str, language: Language, user_config: dict) -> list[Token]:
    """
    Returns list of strings containing data recognized as important
    such as dates, organization names, people's names and surnames and others.
    """
    from spacy_download import load_spacy

    tokens: list[str] = []
    if language == Language.ENGLISH:
        model = user_config["english_tokenizer"]
        stopword_file = './DATA/stopwords-en.txt'
    elif language == Language.POLISH:
        model = user_config["polish_tokenizer"]
        stopword_file = './DATA/stopwords-pl.txt'

    with open(stopword_file, 'r', encoding='utf8') as f:
        stopwords = f.read().splitlines()
    stop_words = set(stopwords)

    nlp = load_spacy(model)  # If the model is not yet downloaded, this line will download the model and load it afterwards
    important_text = nlp(text)
    for ent in important_text.ents:
        try:
            label = parse_label(ent.label_)
            new_tokens = parse_text_to_tokens(ent.lemma_, label, stop_words)
            tokens.extend(new_tokens)
        except NotSupportedLabelType as e:
            pass
            # print(e)

    return tokens


def merge_token_duplicates(tokens: list[Token]) -> list[Token]:
    token_dict = defaultdict[str, int](int)
    for token in tqdm(tokens, desc='Merging tokens'):
        text = token.text
        binary_mask = token.binary_mask
        token_dict[text] |= binary_mask

    new_tokens = list(map(
        lambda k_v: Token(*k_v),
        token_dict.items()))
    return new_tokens


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
