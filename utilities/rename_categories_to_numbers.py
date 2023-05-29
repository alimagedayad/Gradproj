import csv

filename = "../data/vendor_operation_categories_labelling.csv"

with open("../data/vendor_operation_categories_labelling.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

    for text in reader:
        print(text["transaction_category"])
        if text["transaction_category"] == "Groceries":
            text["transaction_category"] = 0
        if text["transaction_category"] == "Shopping":
            text["transaction_category"] = 1
        if text["transaction_category"] == "Restaurants":
            text["transaction_category"] = 2
        if text["transaction_category"] == "Transportation":
            text["transaction_category"] = 3
        if text["transaction_category"] == "Travel":
            text["transaction_category"] = 4
        if text["transaction_category"] == "Entertainment":
            text["transaction_category"] = 5
        if text["transaction_category"] == "Utilities":
            text["transaction_category"] = 6
        if text["transaction_category"] == "Health":
            text["transaction_category"] = 7
        if text["transaction_category"] == "Services":
            text["transaction_category"] = 8
        if text["transaction_category"] == "Transfers":
            text["transaction_category"] = 9
        if text["transaction_category"] == "Cash":
            text["transaction_category"] = 10
        if text["transaction_category"] == "General":
            text["transaction_category"] = 11
        if text["transaction_category"] == "Insurance":
            text["transaction_category"] = 12
        if text["transaction_category"] == "Investment":
            text["transaction_category"] = 13
        if text["transaction_category"] == "Gifts":
            text["transaction_category"] = 14
        if text["transaction_category"] == "Charity":
            text["transaction_category"] = 15
        if text["transaction_category"] == "Other":
            text["transaction_category"] = 16

        id2label = {
            0: "Groceries",
            1: "Shopping",
            2: "Restaurants",
            3: "Transportation",
            4: "Travel",
            5: "Entertainment",
            6: "Utilities",
            7: "Health",
            8: "Services",
            9: "Transfers",
            10: "Cash",
            11: "General",
            12: "Insurance",
            13: "Investment",
            14: "Gifts",
            15: "Charity",
            16: "Other",
        }

        label2id = {
            "Groceries": 0,
            "Shopping": 1,
            "Restaurants": 2,
            "Transportation": 3,
            "Travel": 4,
            "Entertainment": 5,
            "Utilities": 6,
            "Health": 7,
            "Services": 8,
            "Transfers": 9,
            "Cash": 10,
            "General": 11,
            "Insurance": 12,
            "Investment": 13,
            "Gifts": 14,
            "Charity": 15,
            "Other": 16,
        }

        with open(
            "../data/renamed_vendor_operation_categories_labelling.csv", "a", newline=""
        ) as new_csvfile:
            writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)
            if new_csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(text)
