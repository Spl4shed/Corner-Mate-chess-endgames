import os
import csv
from collections import OrderedDict

folder_path = os.getcwd()  # Use the current directory as the folder path

# Get the list of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

# Process the CSV files
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    print(f"Processing file: {file}")

    # Read the CSV file and remove duplicate rows
    with open(file_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]

    unique_rows = list(OrderedDict.fromkeys(tuple(row.items()) for row in rows))
    num_duplicates = len(rows) - len(unique_rows)

    # Write the unique rows back to the CSV file
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows([dict(row) for row in unique_rows])

    print(f"Duplicate rows removed: {num_duplicates}")

print("Duplicate rows removal completed.")
