import json


def combine_json(file, file2, export_file):
    data = []
    with open(file, 'r') as f:
        data = json.load(f)
    with open(file2, 'r') as f:
        data.extend(json.load(f))
    with open(export_file, 'w') as f:
        json.dump(data, f)


combine_json("../bank_statements/ready/hema.json", "../bank_statements/ready/ali.json", "./dataset.json")
