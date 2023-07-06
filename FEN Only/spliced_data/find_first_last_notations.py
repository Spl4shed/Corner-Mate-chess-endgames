import os
import csv
from collections import Counter
import re

folder_path = os.getcwd()  # Use the current directory as the folder path

# Get the list of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

output_data_white = []
output_data_black = []
start_notations = []  # List to store start notations
end_notations = []  # List to store end notations

# Process the CSV files
for item in csv_files:
    item_path = os.path.join(folder_path, item)

    # Check if the item is a regular file and ends with '.csv'
    if os.path.isfile(item_path) and item.endswith(".csv"):
        print(f"Processing file: {item}")  # Print the name of the file being opened

        # Create a dictionary to store the start and end notations
        start_notation_counts = Counter()
        end_notation_counts = Counter()

        # Read the CSV file and modify the notations, and collect the notations for the start and end rows
        with open(item_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            row_number = 0

            for row in reader:
                notation = row["notation"]

                # Modify the notation by removing "x" if it's at the second index and removing special characters
                notation = re.sub(r"^(.)(x)(.+)$", r"\1\3", notation)
                notation = re.sub(r"^(.{2})(x)(.+)$", r"\1\3", notation)
                notation = re.sub(r"[^\w\s]", "", notation)

                if row_number % 2 == 0:
                    start_notation_counts[notation] += 1
                    start_notations.append(notation)  # Add the modified notation to start_notations list
                else:
                    end_notation_counts[notation] += 1
                    end_notations.append(notation)  # Add the modified notation to end_notations list

                row_number += 1

        # Get the two most common start and end notations and their frequencies
        start_notation_common = start_notation_counts.most_common(2)
        end_notation_common = end_notation_counts.most_common(2)

        # Determine section based on the file name
        section = "White" if item.endswith("_W_modified.csv") else "Black" if item.endswith("_B_modified.csv") else "Other"

        # Prepare the data for output
        output_row = [section, item]
        for notation, freq in start_notation_common:
            rel_freq = freq / row_number
            output_row.extend([notation, freq, rel_freq])
        for notation, freq in end_notation_common:
            rel_freq = freq / row_number
            output_row.extend([notation, freq, rel_freq])

        if section == "White":
            output_data_white.append(output_row)
        elif section == "Black":
            output_data_black.append(output_row)

# Prepare the header row for the final output CSV file
header_row = ["Section", "Original File"]
for i in range(2):
    header_row.extend([f"Most common start notation {i+1}", f"Most common start notation freq {i+1}", f"Most common start notation rel freq {i+1}"])
for i in range(2):
    header_row.extend([f"Most common end notation {i+1}", f"Most common end notation freq {i+1}", f"Most common end notation rel freq {i+1}"])

# Create the output folder path
output_folder = os.path.abspath(os.path.join(os.path.dirname(folder_path), "notation_summaries"))

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Write the output to the final CSV file
output_file = "notation_summaries.csv"
output_path = os.path.join(output_folder, output_file)

with open(output_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header_row)

    # Write the white section statistics
    writer.writerow(["White Section"])
    writer.writerows(output_data_white)

    # Add an empty row
    writer.writerow([])

    # Write the black section statistics
    writer.writerow(["Black Section"])
    writer.writerows(output_data_black)

print(f"File '{output_file}' written in the '{output_folder}' folder.")
