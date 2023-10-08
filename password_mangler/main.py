import argparse
from file_parser import *
from yaml_parser import parse_yaml
from rules_applier import mangle_strings, ManglingEpochType


def guess_passwords(
    nr_of_passwords: int, 
    output_filename: str,
    language: str,
    evidence_files: list[str],
    config_file: str
) -> None:
    # Printing arguments
    print(f"Generating {nr_of_passwords} passwords")
    print(f"Output file: {output_filename}")
    print(f"Evidence files: {evidence_files}")
    print(f"Language: {language}")
    # Gathering tokens from the evidence files
    important_phrases = read_evidence(evidence_files, language)
    important_phrases = normalize_important_phrases(important_phrases)

    phrases_filtered = list(filter(lambda p: p.label == 'PERSON' 
                                   or p.label == 'ORG',
                                   important_phrases))
    
    phrases = set(phrases_filtered)
    # sorted_word_count = count_and_sort_words(important_phrases)
    # print(important_phrases)

    print(phrases)
    phrases_text = list(map(lambda p: p.text, phrases))

    rules = parse_yaml(config_file)

    mangling_schedule = [ManglingEpochType.UNARY,
                         ManglingEpochType.UNARY,
                         ManglingEpochType.BINARY]

    passwords = mangle_strings(*rules, phrases_text, mangling_schedule)
    print(passwords)

    # print(sorted_word_count)
    # TODO Use sorted word count and important phrases to generate passwords


def read_evidence(evidence_files: list[str], language: str) -> list[Phrase]:
    parser_language = Language.ENGLISH if language == "EN" else Language.POLISH
    important_phrases = []
    lemmatized_words = []
    for file_name in evidence_files:
        # Extracting and clearing text
        text = extract_text_from_file(file_name)
        text = clear_text(text)
        words = text.split()
        # Lemmatiziation and couting of words
        lemmatized_words += lemmatize(words, parser_language)
        # Important data recognition
        important_phrases += recognize_data_strings(text, parser_language)
    return important_phrases


def normalize_important_phrases(phrases: list[Phrase]) -> list[Phrase]:
    normalized_phrases = []

    for phrase in phrases:
        if phrase.label == 'DATE':
            normalized_phrases.append(phrase)
            continue

        splited_phrase_text = phrase.text.split()
        for subphrase_text in splited_phrase_text:
            lowercase_text = subphrase_text.lower()
            new_phrase = Phrase(lowercase_text, phrase.label)
            normalized_phrases.append(new_phrase)

    return normalized_phrases


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password_guessing.py",
        description="This program generates a dictionary of passwords using the provided evidence."
                     "Currently supported evidence formats are: .txt, .pdf, .docx, .odt",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        help="Number of passwords to generate (default: 100)",
        default=100,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Text file with generated passwords (default: password_guessing.txt)",
        default="password_guessing.txt",
    )
    parser.add_argument(
        "-l",
        "--language",
        choices=["EN", "PL"],
        help="Language of the evidence (default: EN)",
        default="EN",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="User config file", #TODO better help
        default="config.yaml"
    )
    parser.add_argument(
        "filename",
        metavar="FILENAME",
        type=str,
        nargs="+",
        help="Name of the file containing the evidence (can be a folder name)",
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    guess_passwords(
        nr_of_passwords=args.number,
        output_filename=args.output,
        language=args.language,
        evidence_files=args.filename,
        config_file=args.config
    )
