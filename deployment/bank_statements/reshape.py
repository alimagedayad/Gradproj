import csv
import os

# Get the current directory
current_directory = os.getcwd()

# Iterate over all files in the current directory
for file in os.listdir(current_directory):
    # If the file is a CSV file
    if file.endswith(".csv"):
        # Read the original CSV file
        with open(file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            transactions = list(reader)

        # Create a new CSV file
        new_file_name = file.replace(".csv", "_updated.csv")
        with open(new_file_name, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "txn date", "clean_narrative", "value"])
            for transaction in transactions:
                # Get the clean narrative
                clean_narrative = transaction[-1]

                # Write the transaction to the new CSV file
                writer.writerow(
                    [transaction[0], transaction[1], clean_narrative, transaction[3]]
                )

        # Delete the original CSV file
        os.remove(file)
        os.rename(new_file_name, file)
