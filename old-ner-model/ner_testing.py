import spacy
import numpy as np
import re

nlp = spacy.load("spacy_ner_model")

def clean_text(string):
    cleaned_text = []
    cib_ref_number_regex = r"^FT.{12}$"
    cib_ref_number_pattern = re.compile(cib_ref_number_regex)

    generic_ref_regex = r"\w*\d\w*[a-zA-Z]\w*|\w*[a-zA-Z]\w*\d\w*"
    generic_ref_pattern = re.compile(generic_ref_regex)

    numbers_regex = r"\d+"
    numbers_pattern = re.compile(numbers_regex)

    string = string.split(" ")

    for str in string:
        if cib_ref_number_pattern.match(str):
            print("Matched CIB ref number: ", str)
            continue
        elif generic_ref_pattern.match(str):
            print("Matched generic ref number: ", str)
            continue
        elif numbers_pattern.match(str):
            print("Matched numbers: ", str)
            continue
        elif str == "-":
            print("Matched hyphen: ", str)
            continue
        else:
            cleaned_text.append(str)
    return " ".join(cleaned_text)

text = input("Enter text: ")
text = clean_text(text)
doc = nlp(text)
detected_entities = []

for ent in doc.ents:
    detected_entities.append({
        "entity": ent.label_,
        "value": ent.text
    }) 

print(detected_entities)