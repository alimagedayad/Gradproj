import spacy
import json
import re
import os
import csv
import datetime
import numpy as np
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
import tensorflow as tf
from utils import load_csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

save_directory = "./bert"

loaded_tokenizer = DistilBertTokenizer.from_pretrained(save_directory)
loaded_model = TFDistilBertForSequenceClassification.from_pretrained(save_directory)
spacy = spacy.load("spacy_ner_model_v2")


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


def get_entities(text):
    doc = spacy(text)
    entities = []

    for ent in doc.ents:
        entities.append({"entity": ent.label_, "value": ent.text})

    return entities


def get_category(text):
    value_to_label = {
        0: "Cash",
        1: "Entertainment",
        2: "General",
        3: "Groceries",
        4: "Health",
        5: "Investment",
        6: "Others",
        7: "Restaurants",
        8: "Services",
        9: "Shopping",
        10: "Transfers",
        11: "Transportation",
        12: "Travel",
        13: "Utilities",
    }
    predict_input = loaded_tokenizer.encode(
        text, truncation=True, padding=True, return_tensors="tf"
    )
    output = loaded_model(predict_input)[0]
    prediction_value = tf.argmax(output, axis=1).numpy()[0]
    return value_to_label[prediction_value]


class Predict(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text", type=str)
        args = parser.parse_args()

        text = args["text"]
        return jsonify({"category": get_category(text)})


class Ner(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text", type=str)
        args = parser.parse_args()

        text = args["text"]
        entities = get_entities(text)

        return jsonify({"entities": entities})


# Create a route that takes in a csv file and returns a json file
class CsvToJson(Resource):
    def post(self):
        uuid = uuid4()

        if "file" not in request.files:
            return "No file uploaded.", 400

        file = request.files["file"]
        if file.filename == "":
            return "No file selected.", 400

        file.save(f"cache/{uuid}.csv")
        csv_data = load_csv(f"cache/{uuid}.csv")

        response = []

        for i, data in enumerate(csv_data):
            if i == 0:
                continue

            found_entites = {}

            date, txn_date, description, value = data[0], data[1], data[2], data[3]
            # convert date and txn_date to timestamp without pandas
            ddm_regex = r"\d{1,2}-\d{1,2}"
            ddm_pattern = re.compile(ddm_regex)

            # print("matched regex: ", re.match(date, ddm_pattern))
            if re.match(ddm_pattern, date):
                date = datetime.datetime.strptime(f"{date}-2023", "%d-%m-%Y").strftime(
                    "%d/%m/%Y"
                )

            if re.match(ddm_pattern, txn_date):
                txn_date = datetime.datetime.strptime(
                    f"{txn_date}-2023", "%d-%m-%Y"
                ).strftime("%d/%m/%Y")

            entites = get_entities(description)

            for entity in entites:
                found_entites[entity["entity"]] = entity["value"]

            if "OP" in found_entites.keys() and "VENDOR" not in found_entites.keys():
                category = get_category(found_entites["OP"])

            elif (
                "OP" in found_entites.keys()
                and "BANL" in found_entites.keys()
                and not "VENDOR" not in found_entites.keys()
            ):
                category = get_category(found_entites["OP"])

            elif "OP" in found_entites.keys() and "VENDOR" in found_entites.keys():
                print(
                    "OP and VENDOR: ",
                    description,
                    " detected entities: ",
                    entites,
                    " found entities: ",
                    found_entites,
                )
                category = get_category(found_entites["VENDOR"])

            elif "VENDOR" in found_entites.keys():
                category = get_category(found_entites["VENDOR"])

            else:
                category = "Others"

            response.append(
                {
                    "type": found_entites["OP"]
                    if "OP" in found_entites.keys()
                    else None,
                    "amount": value,
                    "merchant": found_entites["VENDOR"]
                    if "VENDOR" in found_entites.keys()
                    else None,
                    "tran_category": category,
                    "date": txn_date,
                    "bank": found_entites["BANK"]
                    if "BANK" in found_entites.keys()
                    else None,
                }
            )

            print(f"{found_entites}")

        os.remove(f"cache/{uuid}.csv")

        return response

        # results = []
        # try:
        #     load_csv(file)
        #     print(load_csv)

        # except csv.Error as e:
        #     print(e)
        #     return "Invalid CSV file.", 400

        # return results


api.add_resource(Predict, "/predict")
api.add_resource(Ner, "/ner")
api.add_resource(CsvToJson, "/csv")

if __name__ == "__main__":
    app.run(debug=True)
