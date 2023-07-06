import os
import pandas as pd

# Get the current directory where the script is located
folder_path = os.path.dirname(os.path.abspath(__file__))

# Define the column names
color_column_name = 'color'
notation_column_name = 'notation'

# Define the output folder path
output_folder = os.path.join(os.path.dirname(folder_path), 'split_fixed_notations')
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        output_file_base_name = os.path.splitext(file_name)[0]

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Modify notation based on color and piece
        df.loc[(df[color_column_name] == 'Black') & (df['piece'] == 'P') & (~df[notation_column_name].str.startswith(('P', 'p'))), notation_column_name] = 'p' + df[notation_column_name]
        df.loc[(df[color_column_name] == 'White') & (df['piece'] == 'P') & (~df[notation_column_name].str.startswith(('P', 'p'))), notation_column_name] = 'P' + df[notation_column_name]
        df.loc[df[color_column_name] == 'White', notation_column_name] = df.loc[df[color_column_name] == 'White', notation_column_name].str.capitalize()


        # Create separate DataFrames for black and white color
        black_df = df[df[color_column_name] == 'Black'].copy()
        white_df = df[df[color_column_name] == 'White'].copy()

        # Generate output file names for black and white dataframes
        black_output_file = f"{output_file_base_name}_B.csv"
        white_output_file = f"{output_file_base_name}_W.csv"

        # Define the output paths for black and white dataframes
        black_output_path = os.path.join(output_folder, black_output_file)
        white_output_path = os.path.join(output_folder, white_output_file)

        # Save black and white DataFrames to separate CSV files
        black_df.to_csv(black_output_path, index=False)
        white_df.to_csv(white_output_path, index=False)

print("Data has been split and modified based on color and piece. Modified files have been written in the 'split_fixed_notations' folder.")