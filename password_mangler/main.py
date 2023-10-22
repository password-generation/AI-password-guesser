import argparse
from file_reader import *
from yaml_parser import parse_yaml
from rules_applier import mangle_phrases
from commons import Language
from text_parser import *
from results_saver import save_important_phrases


def guess_passwords(
    nr_of_passwords: int,
    output_filename: str,
    arg_language: str,
    evidence_files: list[str],
    config_file: str,
    wildcards_present: bool,
    max_length: int
) -> None:
    # Printing arguments
    # print(f"Generating {nr_of_passwords} passwords")
    # print(f"Output file: {output_filename}")
    print(f"Evidence files: {evidence_files}")
    print(f"Language: {arg_language}")
    # Gathering tokens from the evidence files
    language = Language.ENGLISH if arg_language == "EN" else Language.POLISH
    phrases = read_evidence(evidence_files, language)
    phrases = lemmatize_phrases(phrases, language)
    phrases = merge_phrase_duplicates(phrases)

    label_types = [LabelType.DATE]
    filter_type = FilterType.NOT
    phrases = filter_phrases_based_on_label(phrases, label_types, filter_type)
    print(phrases)

    # sorted_word_count = count_and_sort_words(phrases)

    unary_rules, binary_rules, mangling_schedule = parse_yaml(config_file)

    phrases = mangle_phrases(unary_rules, binary_rules,
                             mangling_schedule, phrases,
                             wildcards_present, max_length)

    label_types = [LabelType.PERSON]
    filter_type = FilterType.AND
    phrases = filter_phrases_based_on_label(phrases, label_types, filter_type)

    if wildcards_present:
        label_types.append(LabelType.WILDCARD)
        filter_type = FilterType.AND
        phrases = filter_phrases_based_on_label(phrases, label_types, filter_type)

    save_important_phrases(phrases, output_filename)
    for phr in sorted(phrases):
        print(phr)


def read_evidence(evidence_files: list[str], language: Language) -> list[Phrase]:
    important_phrases = []
    for file_name in evidence_files:
        text = extract_text_from_file(file_name)
        text = clear_text(text)
        important_phrases += recognize_data_strings(text, language)

    return important_phrases


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
        "-w",
        "--wildcard",
        action="store_true",
        default=False,
        help="Flag for adding wildcards to passwords"
    )
    parser.add_argument(
        "-m",
        "--max",
        type=int,
        help="Max length of passwords",
        default=8
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
        arg_language=args.language,
        evidence_files=args.filename,
        config_file=args.config,
        wildcards_present=args.wildcard,
        max_length=args.max,
    )