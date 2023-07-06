import os
import csv

folder_path = os.getcwd()  # Use the current directory as the folder path

# Define the output folder path
output_folder = os.path.join(os.path.dirname(folder_path), "spliced_data")
output_folder_path = os.path.abspath(output_folder)

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Get the list of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

# Process the CSV files
for item in csv_files:
    item_path = os.path.join(folder_path, item)

    print(f"Processing file: {item}")  # Print the name of the file being opened

    # Create a dictionary to store the rows for each game_id
    game_rows = {}

    # Read the CSV file and keep the rows with the lowest and highest move_no for each unique game_id
    with open(item_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            game_id = row["game_id"]
            move_no = int(row["move_no"])

            if game_id not in game_rows:
                # Initialize with the first row encountered for each game_id
                game_rows[game_id] = {"lowest_move_no": row, "highest_move_no": row}
            else:
                if move_no < int(game_rows[game_id]["lowest_move_no"]["move_no"]):
                    game_rows[game_id]["lowest_move_no"] = row
                elif move_no > int(game_rows[game_id]["highest_move_no"]["move_no"]):
                    game_rows[game_id]["highest_move_no"] = row

    # Create a new CSV file to store the results
    output_file = os.path.splitext(item)[0] + "_modified.csv"
    output_path = os.path.join(output_folder_path, output_file)

    # Write the rows to the output CSV file
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)

        # Write the header to the output CSV file
        writer.writeheader()

        # Write the rows to the output CSV file
        for game_id in game_rows:
            writer.writerow(game_rows[game_id]["lowest_move_no"])
            writer.writerow(game_rows[game_id]["highest_move_no"])

print("Spliced data has been written to the 'spliced_data' folder.")
