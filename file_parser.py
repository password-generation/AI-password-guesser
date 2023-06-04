import textract
import sys
import re
import nltk
import morfeusz2  # Needs a license copy within our repo i think :d
import spacy
from collections import Counter

    # nltk.download('wordnet') 
    # nltk.download('punkt') 
    # pip install spacy
    # python -m spacy download pl_core_news_lg
    # python -m spacy download en_core_web_lg


if __name__ == "__main__":

    # Argument Checking
    if len(sys.argv) != 2:
        print("Provide only one name of file in this directory as program argument")
    file_name = sys.argv[1]

    # Retrieving plain text from given file
    if file_name.split(".")[-1] != "txt":
        text = textract.process(f"./test_files/{file_name}").decode('utf8')
    else:
        with open(f"./test_files/{file_name}", "rb") as f:
            text = f.read().decode('utf8')

    # Clearing the text from punctuation (or rather every character that's specified in the regrex below)
    text = re.sub('[^A-Za-z0-9ĘęÓóĄąŚśŁłŻżŹźĆćŃń ]+', ' ', text)

    # Important data recognition Polish
    important_words = []
    nlpPL = spacy.load("pl_core_news_lg")
    important_text_polish = nlpPL(text)
    for ent in important_text_polish.ents:
        # print(ent.text, ent.label_)
        important_words.append(ent.text)
    # Important data recognition Engish
    nlpEN = spacy.load("en_core_web_lg")
    important_text_english = nlpEN(text)
    for ent in important_text_english.ents:
        if ent.label_ == "DATE":
            # print(ent.text, ent.label_)
            important_words.append(ent.text)

    # Creating a dictionary of lemmatized words with their counted appearances
    words = important_words
    lem_words = []
    # FOR POLISH
    morf = morfeusz2.Morfeusz() 
    last_i = -1
    for i, j, interp in morf.analyse(' '.join(words)):
        if last_i < i:
            lem_words.append(interp[1].split(":")[0])
            last_i = i
    # FOR ENGLISH
    lemmatizer = nltk.WordNetLemmatizer()
    lem_words = [lemmatizer.lemmatize(word) for word in lem_words]
    # COUNT
    word_count_dict = dict(Counter(lem_words).items())

    # Creating a list of words sorted by the occurance number
    sorted_word_count = [(k, word_count_dict[k]) for k in sorted(word_count_dict, key=word_count_dict.get, reverse=True)]

    for element in sorted_word_count:
        print(element)    
    