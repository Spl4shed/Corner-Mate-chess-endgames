import os
import csv

# Get the current directory where the script is located
folder_path = os.getcwd()

# Define the column names
color_column_name = 'color'
notation_column_name = 'notation'

# Define the output folder path
output_folder = os.path.join(os.path.dirname(folder_path), 'fixed_notations')

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
                # Check if the color is "Black" or "White"
                if row[color_column_name].lower() == 'black':
                    # Convert the first letter in the notation column to lowercase
                    if row['piece'] == 'P' and not row[notation_column_name].startswith(('P', 'p')):
                        row[notation_column_name] = 'p' + row[notation_column_name]
                    else:
                        row[notation_column_name] = row[notation_column_name][0].lower() + row[notation_column_name][1:]
                elif row[color_column_name].lower() == 'white':
                    # Convert the first letter in the notation column to uppercase
                    if row['piece'] == 'P' and not row[notation_column_name].startswith(('P', 'p')):
                        row[notation_column_name] = 'P' + row[notation_column_name]
                    else:
                        row[notation_column_name] = row[notation_column_name][0].upper() + row[notation_column_name][1:]
                
                # Write the modified row to the modified file
                writer.writerow(row)

print("Modified files have been written in the 'fixed_notations' folder.")
