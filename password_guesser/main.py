import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from argparse import ArgumentParser
from file_reader import extract_text_from_file, clear_text
from yaml_parser import get_model_props_from_config, parse_yaml
from rules_applier import mangle_tokens
from commons import Language, Token, token_to_str
from text_parser import recognize_data_strings, merge_token_duplicates, \
    lemmatize_tokens, recognize_email_addresses
from results_saver import save_result_to_txt, save_tokens
from dates_parser import extract_parse_dates
from copy import deepcopy
from unidecode import unidecode


def guess_passwords(
    max_length: int,
    output_filename: str,
    arg_language: str,
    evidence_files: list[str],
    config_file: str,
    mangle: bool,
    generate: bool,
    verbose: bool,
) -> None:
    # Printing program arguments
    print(f"Generating passwords of max length {max_length}")
    print(f"Output file: {output_filename}")
    print(f"Evidence files: {evidence_files}")
    print(f"Language: {arg_language}")
    print(f"Will {'not ' if not mangle else ''}mangle passwords")
    print(f"Will {'not ' if not generate else ''}generate passwords")

    # Gathering tokens from the evidence files
    language = Language.ENGLISH if arg_language == "EN" else Language.POLISH

    print("Reading evidence...")
    tokens = read_evidence(evidence_files, language)

    print("Lemmatizing tokens...")
    tokens = lemmatize_tokens(tokens, language)

    print("Merging duplicates...")
    tokens = merge_token_duplicates(tokens)

    save_tokens(tokens, "extracted_tokens.csv")

    print(f"Extracted {len(tokens)} tokens")
    if verbose:
        for tok in sorted(tokens):
            print(token_to_str(tok))

    if mangle or generate:
        # Date parsing
        tokens = extract_parse_dates(tokens, language)
        base_tokens = deepcopy(tokens)

        # Replacing polish specific letters with english equivalents
        if language == Language.POLISH:
            tokens = [Token(unidecode(token.text), token.binary_mask) for token in tokens]

    # Mangling of the tokens
    if mangle:
        user_config = parse_yaml(config_file)

        print("Mangling tokens...")
        tokens = mangle_tokens(user_config, tokens, False, max_length)
        save_tokens(tokens, "mangled_tokens.csv")
        print(f"Mangled {len(tokens)} tokens")
        if verbose:
            for tok in sorted(tokens):
                print(token_to_str(tok))

        if not generate:
            save_result_to_txt(tokens, output_filename)
            print(
                f"Saved result with {len(tokens)} only mangled passwords to {output_filename} file"
            )
            return

    # Generating new tokens using AI
    if generate:
        print("Generating passwords...")
        from model import TemplateBasedPasswordModel, tokens_to_seeds

        seeds = tokens_to_seeds(base_tokens, max_length)
        std_dev, samples_count = get_model_props_from_config(config_file)

        print(f"Number of tokens entering password generator: {len(seeds)}")
        print(f"For every token generator will generate at most {samples_count} passwords")

        model = TemplateBasedPasswordModel(samples_count, std_dev)
        generated_tokens = model.sample_model_based_on_templates(seeds)
        save_tokens(generated_tokens, "generated_tokens.csv")
        print(f"Generated {len(generated_tokens)} tokens")
        if verbose:
            for tok in sorted(generated_tokens):
                print(token_to_str(tok))

        if not mangle:
            save_result_to_txt(generated_tokens, output_filename)
            print(
                f"Saved result with {len(generated_tokens)} only generated passwords to {output_filename} file"
            )
            return

        # Cutting out duplicates and saving the complete password list
        # save_tokens(merge_token_duplicates(tokens+generated_tokens), output_filename)

        save_result_to_txt(
            merge_token_duplicates(tokens + generated_tokens), output_filename
        )
        print(
            f"Saved result with {len(merge_token_duplicates(tokens + generated_tokens))} passwords to {output_filename} file"
        )


def read_evidence(evidence_files: list[str], language: Language) -> list[Token]:
    text = ""
    for file_name in evidence_files:
        text = text + " " + clear_text(extract_text_from_file(file_name))

    tokens = recognize_email_addresses(text)
    print("Tokenizing text...")
    tokens += recognize_data_strings(text, language)

    return tokens


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="password_guesser",
        description="This program generates a dictionary of passwords using the provided evidence. "
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
        help="Output file with result passwords",
        default="out.txt",
    )
    parser.add_argument(
        "-l",
        "--language",
        choices=["EN", "PL"],
        help="Language of the evidence (default: EN)",
        default="EN",
    )
    parser.add_argument(
        "-c", "--config", type=str, help="User config file", default="config.yaml"
    )
    parser.add_argument(
        "-m",
        "--mangle",
        action="store_true",
        default=False,
        help="Use password mangling",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        default=False,
        help="Use password generation model",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Flag for printing verbose output",
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
        mangle=args.mangle,
        generate=args.generate,
        verbose=args.verbose,
    )
