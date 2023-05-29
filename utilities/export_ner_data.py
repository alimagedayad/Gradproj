import json
import os
import re
import spacy

nlp = spacy.load("../ner-training-v2/spacy_ner_model_v2")


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


ops = []
banks = []
locations = []
vendorss = []

with open("../data/vendors.txt") as f:
    vendors = f.read().splitlines()

    for vendor in vendors:
        cleaned_vendor = clean_text(vendor)
        doc = nlp(cleaned_vendor)
        detected_entities = []

        for ent in doc.ents:
            detected_entities.append({"entity": ent.label_, "value": ent.text})
            print(detected_entities)

        for ent in doc.ents:
            if ent.label_ == "OP":
                ops.append(ent.text)
            elif ent.label_ == "LOCATION":
                locations.append(ent.text)
            elif ent.label_ == "BANK":
                banks.append(ent.text)
            elif ent.label_ == "VENDOR":
                vendorss.append(ent.text)

print("Ops: ", ops)
print()
print("Banks: ", banks)
print()
print("Locations: ", locations)
print()
print("Vendors: ", vendorss)

print("Ops: ", len(ops))
print("Banks: ", len(banks))
print("Locations: ", len(locations))

# with open("../data/split.txt", "w") as f:
#    f.write("\n".join(map(str, ops)))
#    f.write("\n".join(map(str, vendorss)))
