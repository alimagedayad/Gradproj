import json
import os

with open("../bank_statements/pre_annotated/yasseen.json", "r") as f:
    data = json.load(f)

train_data = data['annotations']
train_data = [tuple(x) for x in train_data if x]

for i, (_, entities) in enumerate(train_data):
    for x, entity in enumerate(entities['entities']):
        train_data[i][1]['entities'][x] = (entity[0], entity[1], entity[2].upper())

with open("../bank_statements/ready/yasseen.json", "w") as f:
    json.dump(train_data, f)
