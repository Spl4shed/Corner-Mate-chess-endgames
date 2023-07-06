import pandas as pd
from scipy.stats import pearsonr

# Read the CSV file
df = pd.read_csv('summary.csv')

# Calculate the Pearson correlation for each column
correlation_values = []
columns = df.columns[2:]
for column in columns:
    correlation, _ = pearsonr(df['Skill'], df[column])
    correlation_values.append(correlation)

# Append the "Correlation" row to the dataframe
correlation_row = ['Correlation'] + [''] * (len(df.columns) - 1)
correlation_row[2:] = correlation_values
df = df.append(pd.Series(correlation_row, index=df.columns), ignore_index=True)

# Save the updated dataframe to the CSV file
df.to_csv('summary.csv', index=False)
