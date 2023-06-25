import argparse
from file_parser import *


def main(
    nr_of_passwords: int, output_filename: str, language: str, evidence_files: list[str]
) -> None:
    # Printing arguments
    print(f"Generating {nr_of_passwords} passwords")
    print(f"Output file: {output_filename}")
    print(f"Evidence files: {evidence_files}")
    print(f"Language: {language}")
    # Gatering tokens from the evidence files
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
    sorted_word_count = count_and_sort_words(lemmatized_words)
    # TODO Use sorted word count and important phrases to generate passwords


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password_guessing.py",
        description="This program generates a dictionary of passwords using the provided evidence. \
                     Currently supported evidence formats are: .txt, .pdf, .docx, .odt",
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
        "string",
        metavar="FILENAME",
        type=str,
        nargs="+",
        help="Name of the file containing the evidence (can be a folder name)",
    )
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    arg_dict = vars(args)
    main(
        arg_dict["number"], arg_dict["output"], arg_dict["language"], arg_dict["string"]
    )
