from csv import reader


# Load the CSV file
def load_csv(filename):
    data = list()
    # Open file in read mode
    file = open(filename, "r")
    # Reading file
    lines = reader(file)
    csv_reader = reader(file)
    for row in csv_reader:
        if not row:
            continue
        data.append(row)

    return data
