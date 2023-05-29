import random

file_path = "../data/renamed_vendor_operation_categories_labelling.csv"

with open(file_path) as f:
    lines = f.readlines()

random.shuffle(lines)

split_index = int(0.8 * len(lines))

train = lines[:split_index]
test = lines[split_index:]

with open("../data/train.txt", "w") as f:
    f.writelines(train)

with open("../data/test.txt", "w") as f:
    f.writelines(test)
