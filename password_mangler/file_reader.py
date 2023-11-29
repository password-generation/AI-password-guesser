from textract import process as textract_process
import re
from os import path, listdir


def extract_text_from_file(file_path: str) -> str:
    """
    Returns plain text read from provided file or files in a directory.
    Supported extensions: pdf, odt, docx, txt
    """
    if path.isdir(file_path):
        text = ""
        for filename in listdir(file_path):
            child_path = path.join(file_path, filename)
            text += " " + extract_text_from_file(child_path)
        return text
    elif file_path.split(".")[-1] != "txt":
        text = textract_process(file_path).decode("utf8")
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
