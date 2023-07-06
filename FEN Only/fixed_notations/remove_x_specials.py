import os
import csv
import re

# Get the current directory where the script is located
folder_path = os.getcwd()

# Define the column names
color_column_name = 'color'
notation_column_name = 'notation'

# Define the output folder path
output_folder = os.path.join(os.path.dirname(folder_path), 'no_x_specials')

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        
        # Create a modified file name
        modified_file_name = f"modified_{file_name}"
        modified_file_path = os.path.join(output_folder, modified_file_name)
        
        with open(file_path, 'r', newline='') as file, open(modified_file_path, 'w', newline='') as modified_file:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(modified_file, fieldnames=reader.fieldnames)
            
            # Write the header row
            writer.writeheader()
            
            # Loop through each row in the CSV file
            for row in reader:
                # Remove special characters from the notation column
                row[notation_column_name] = re.sub(r'\W+', '', row[notation_column_name])
                
                # Check if the second or third character is 'x' and remove it
                if len(row[notation_column_name]) >= 3 and row[notation_column_name][1] == 'x':
                    row[notation_column_name] = row[notation_column_name][0] + row[notation_column_name][2:]
                elif len(row[notation_column_name]) >= 3 and row[notation_column_name][2] == 'x':
                    row[notation_column_name] = row[notation_column_name][0:2] + row[notation_column_name][3:]
                
                # Write the modified row to the modified file
                writer.writerow(row)

print("Modified files have been written in the 'no_x_specials' folder.")
