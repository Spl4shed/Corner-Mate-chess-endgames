import os
import csv
from collections import Counter

folder_path = os.getcwd()  # Use the current directory as the folder path

# Create a new CSV file to store the results
output_file = "summary.csv"
output_folder = os.path.abspath(os.path.join(os.path.dirname(folder_path), output_file))

# Define the header for the output CSV file
header = ["Filename", "Game Over", "Game Over (Relative)", "Is Check", "Is Check (Relative)", "Is Checkmate", "Is Checkmate (Relative)"]

# Define the pieces in the desired order
pieces_order = ['P', 'R', 'Q', 'K', 'B', 'N']

# Write the header and pieces order to the output CSV file
with open(output_folder, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header + pieces_order)

    # Get the list of CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

    # Process the CSV files
    for item in csv_files:
        item_path = os.path.join(folder_path, item)

        print(f"Processing file: {item}")  # Print the name of the file being opened

        # Initialize counters
        game_over_count = 0
        is_check_count = 0
        is_checkmate_count = 0
        total_rows = 0
        piece_counts = Counter()
        total_pieces = 0
        unique_game_ids = set()

        # Read the CSV file
        with open(item_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                total_rows += 1

                # Count occurrences of '1' in respective columns
                game_over = int(row.get('is_game_over', 0))
                is_check = int(row.get('is_check', 0))
                is_checkmate = int(row.get('is_check_mate', 0))
                piece = row.get('piece', '')
                game_id = row.get('game_id', '')

                game_over_count += game_over
                is_check_count += is_check
                is_checkmate_count += is_checkmate

                # Count occurrences of each piece
                piece_counts[piece] += 1
                total_pieces += 1

                # Add unique game ID to the set
                unique_game_ids.add(game_id)

        # Calculate relative frequencies
        game_over_freq = game_over_count / len(unique_game_ids) if len(unique_game_ids) != 0 else 0
        is_check_freq = is_check_count / total_rows if total_rows != 0 else 0
        is_checkmate_freq = is_checkmate_count / len(unique_game_ids) if len(unique_game_ids) != 0 else 0

        # Generate row data with initial values for each column
        row_data = [item,
                    f"{game_over_count}/{len(unique_game_ids)}",
                    f"{game_over_freq:.2f}",
                    f"{is_check_count}/{total_rows}",
                    f"{is_check_freq:.2f}",
                    f"{is_checkmate_count}/{len(unique_game_ids)}",
                    f"{is_checkmate_freq:.2f}"]

        # Generate a list of relative frequencies for each piece
        piece_freqs = [f"{(piece_counts[piece] / total_pieces):.2f}" for piece in pieces_order]

        # Add the piece frequencies to the row data
        row_data.extend(piece_freqs)

        writer.writerow(row_data)

print(f"Results have been written to {output_file}.")
