import spacy
import json
import re
import numpy as np
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

nlp = spacy.load("spacy_ner_model")

app = Flask(__name__)
api = Api(app)

def clean_text(string):
    cleaned_text = []
    cib_ref_number_regex = r"^FT.{12}$"
    cib_ref_number_pattern = re.compile(cib_ref_number_regex)

    generic_ref_regex = r"\w*\d\w*[a-zA-Z]\w*|\w*[a-zA-Z]\w*\d\w*"
    generic_ref_pattern = re.compile(generic_ref_regex)

    numbers_regex = r"\d+"
    numbers_pattern = re.compile(numbers_regex)

    ipn_regex = r"^FT\w{10}\s-\sPayee Name:"
    cib_online_transfer = "Online Transfer-"

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

class Ner(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text", type=str, help="Text to be processed")
        args = parser.parse_args()
        text = args["text"]
        if text is None:
            return jsonify({"error": "No text provided"})

        text = clean_text(text)
        doc = nlp(text)
        detected_entities = []
        response = [(ent.text, ent.label_) for ent in doc.ents]
        for res in response:
            detected_entities.append(res[1])
        detected_entities = np.unique(detected_entities)
        response = jsonify({
            "response": response,
            "detected_entities": detected_entities.tolist()
        })
        return response


api.add_resource(Ner, "/ner")

if __name__ == "__main__":
    app.run(debug=True)
