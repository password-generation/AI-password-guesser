import textract
import re


def extract_text_from_file(file_path: str) -> str:
    """
    Returns plain text read from provided file.
    Supported extensions: pdf, odt, docx, txt
    """
    if file_path.split(".")[-1] != "txt":
        text = textract.process(file_path).decode("utf8")
    else:
        with open(file_path, "rb") as f:
            text = f.read().decode("utf8")
    return text


def clear_text(text: str) -> str:
    """
    Clears the text from punctuation by replacing every character
    specified in the regrex with a space .
    """
    return re.sub("[^A-Za-z0-9ĘęÓóĄąŚśŁłŻżŹźĆćŃń ]+", " ", text)


if __name__ == "__main__":
    import sys
    # Argument Checking
    if len(sys.argv) != 2:
        print("Provide only one name of file in this directory as program argument")
    file_name = sys.argv[1]

    # Extracting and clearing text
    text = extract_text_from_file(file_name)
    text = clear_text(text)

    # Lemmatiziation and couting of words
    words = text.split()
    print(words)
