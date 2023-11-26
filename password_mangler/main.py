from argparse import ArgumentParser
from file_reader import *
from yaml_parser import parse_yaml
from rules_applier import mangle_tokens, filter_tokens_based_on_label
from commons import Language, Token
from text_parser import *
from results_saver import save_tokens
from dates_parser import extract_parse_dates
from copy import deepcopy
from unidecode import unidecode


def guess_passwords(
    max_length: int,
    output_filename: str,
    arg_language: str,
    evidence_files: list[str],
    config_file: str,
    wildcards_present: bool,
    verbose: bool,
) -> None:
    
    # Printing program arguments
    print(f"Generating passwords of max length {max_length}")
    print(f"Output file: {output_filename}")
    print(f"Evidence files: {evidence_files}")
    print(f"Language: {arg_language}")
    print(f"Wildcards are {'not ' if not wildcards_present else ''}present")

    # Gathering tokens from the evidence files
    language = Language.ENGLISH if arg_language == "EN" else Language.POLISH
    tokens = read_evidence(evidence_files, language)
    tokens = lemmatize_tokens(tokens, language)
    tokens = merge_token_duplicates(tokens)
    save_tokens(tokens, "extracted_tokens.csv")
    print(f"Extracted {len(tokens)} tokens")
    if verbose:
        for tok in sorted(tokens):
            print(token_to_str(tok))

    # Date parsing
    tokens = extract_parse_dates(tokens, language)
    base_tokens = deepcopy(tokens)

    # Replacing polish specific letters with english equivalents
    if language == Language.POLISH:
        tokens = [ Token(unidecode(token.text), token.binary_mask) for token in tokens ]

    # Mangling of the tokens
    user_config = parse_yaml(config_file)
    tokens = mangle_tokens(user_config, tokens, False, max_length)
    save_tokens(tokens, "mangled_tokens.csv")
    print(f"Mangled {len(tokens)} tokens")
    if verbose:
        for tok in sorted(tokens):
            print(token_to_str(tok))
    if not wildcards_present:
        return

    # Generating new tokens using AI
    from model import TemplateBasedPasswordModel, tokens_to_seeds
    seeds = tokens_to_seeds(base_tokens, max_length)
    samples_count = 10
    std_dev = 0.05 
    print(f"seed_count={len(seeds)}, {samples_count=}, {std_dev=}")
    model = TemplateBasedPasswordModel(samples_count, std_dev)
    generated_tokens = model.sample_model_based_on_templates(seeds)
    save_tokens(tokens, "generated_tokens.csv")
    print(f"Generated {len(generated_tokens)} tokens")
    if verbose:
        for tok in sorted(generated_tokens):
            print(token_to_str(tok))

    # Cutting out duplicates and saving the complete password list
    save_tokens(merge_token_duplicates(tokens+generated_tokens), output_filename)
    print(f"Saved {len(tokens+generated_tokens)} passwords to {output_filename} file")


def read_evidence(evidence_files: list[str], language: Language) -> list[Token]:
    tokens = []
    for file_name in evidence_files:
        text = extract_text_from_file(file_name)
        tokens += recognize_email_addresses(text)

        text = clear_text(text)
        tokens += recognize_data_strings(text, language)

    return tokens


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="password_guessing.py",
        description="This program generates a dictionary of passwords using the provided evidence."
                     "Currently supported evidence formats are: .txt, .pdf, .docx, .odt",
    )
    parser.add_argument(
        "-n",
        "--length",
        type=int,
        help="Max length of passwords",
        default=16,
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
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Flag for printing verbose output"
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
        verbose=args.verbose
    )
