import argparse
from file_reader import *
from yaml_parser import parse_yaml
from rules_applier import mangle_tokens
from commons import Language
from text_parser import *
from results_saver import save_tokens


def guess_passwords(
    max_length: int,
    output_filename: str,
    arg_language: str,
    evidence_files: list[str],
    config_file: str,
    wildcards_present: bool,
) -> None:
    # Printing arguments
    print(f"Generating passwords of max length {max_length}")
    print(f"Output file: {output_filename}")
    print(f"Evidence files: {evidence_files}")
    print(f"Language: {arg_language}")
    print(f"Wildcards are {'not' if not wildcards_present else ''} present")

    # Gathering tokens from the evidence files
    language = Language.ENGLISH if arg_language == "EN" else Language.POLISH
    tokens = read_evidence(evidence_files, language)
    tokens = lemmatize_tokens(tokens, language)
    tokens = merge_token_duplicates(tokens)

    save_tokens(tokens, "extracted_tokens.csv")
    print("Extracted tokens")
    for tok in sorted(tokens):
        print(tok)

    # sorted_word_count = count_and_sort_words(tokens)

    user_config = parse_yaml(config_file)
    tokens = mangle_tokens(user_config, tokens, wildcards_present, max_length)

    label_types = [LabelType.PERSON]
    filter_type = FilterType.AND

    if wildcards_present:
        label_types.append(LabelType.WILDCARD)
        filter_type = FilterType.AND
        tokens = filter_tokens_based_on_label(tokens, label_types, filter_type)

    save_tokens(tokens, output_filename)
    print("Mangled tokens")
    for tok in sorted(tokens):
        print(tok)


def read_evidence(evidence_files: list[str], language: Language) -> list[Token]:
    tokens = []
    for file_name in evidence_files:
        text = extract_text_from_file(file_name)
        tokens += recognize_email_addresses(text)

        text = clear_text(text)
        tokens += recognize_data_strings(text, language)

    return tokens


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password_guessing.py",
        description="This program generates a dictionary of passwords using the provided evidence."
                     "Currently supported evidence formats are: .txt, .pdf, .docx, .odt",
    )
    parser.add_argument(
        "-n",
        "--length",
        type=int,
        help="Max length of passwords",
        default=10,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file with mangled tokens",
        default="mangled_tokens.csv",
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
        max_length=args.length,
        output_filename=args.output,
        arg_language=args.language,
        evidence_files=args.filename,
        config_file=args.config,
        wildcards_present=args.wildcard,
    )
