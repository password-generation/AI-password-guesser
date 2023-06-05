import textract
import sys
import re
import nltk
import morfeusz2  # Needs a license copy within our repo i think :d
import spacy
import pandas as pd
import os
from collections import Counter

    # BEFORE YOU RUN THIS CODE
    # nltk.download('wordnet') 
    # nltk.download('punkt') 
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

    # Clearing the text from punctuation 
    # (or rather, every character that's specified in the regrex below - cuts out characters not used in Polish or English)
    text = re.sub('[^A-Za-z0-9ĘęÓóĄąŚśŁłŻżŹźĆćŃń ]+', ' ', text)

    # Important data recognition Polish
    important_polish_phrases = []
    nlpPL = spacy.load("pl_core_news_lg")
    important_text_polish = nlpPL(text)
    for ent in important_text_polish.ents:
        # print(ent.text, ent.label_)
        important_polish_phrases.append(ent.text)
    
    # Important data recognition Engish
    important_english_phrases = []
    nlpEN = spacy.load("en_core_web_lg")
    important_text_english = nlpEN(text)
    for ent in important_text_english.ents:
        # print(ent.text, ent.label_)
        important_english_phrases.append(ent.text)

    # Creating a list of lemmatized words with their counted appearances
    # At the moment, two models are used to lemmatize gathered words consecutively, first for polish, second for english lemmatization
    words = text.split()
    lemmatized_words = []
    # POLISH
    morf = morfeusz2.Morfeusz() 
    last_i = -1
    for i, j, interp in morf.analyse(' '.join(words)):
        # using last_i number to only save the first interpretation of a word
        if last_i < i:
            lemmatized_words.append(interp[1].split(":")[0])
            last_i = i
    # ENGLISH
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in lemmatized_words]
    # Counting
    word_count_dict = dict(Counter(lemmatized_words).items())
    # Creating a list of words sorted by the occurance number
    sorted_word_count = [(k, word_count_dict[k]) for k in sorted(word_count_dict, key=word_count_dict.get, reverse=True)]
    
    # Creating output folder
    if not os.path.exists("./output"):
        os.makedirs("./output")

    # Saving the tokens and their count
    data = {'word': [word for (_, word) in sorted_word_count], 'count': [count for (count, _) in sorted_word_count]}
    df = pd.DataFrame(data)
    df.to_csv("./output/WordCount.csv")

    # Saving extracted important phrases
    data = {'phrases': important_polish_phrases}
    df = pd.DataFrame(data)
    df.to_csv("./output/PolishPhrases.csv")
    data = {'phrases': important_english_phrases}
    df = pd.DataFrame(data)
    df.to_csv("./output/EnglishPhrases.csv")