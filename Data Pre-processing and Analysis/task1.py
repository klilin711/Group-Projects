""" 
COMP20008 Semester 2
Assignment 1 Task 1
"""

# Task 1 - Summary Statistics (1 mark)
import pandas as pd

def task1(dataset_filename):
    # Implement Task 1 here
    # Import the CSV file
    df = pd.read_csv(dataset_filename)
    # Get the number of rows and columns
    row_count = len(df.index)
    column_count = len(df.columns)
    # Print the number of rows and columns
    num_rows = f"Number of rows: {row_count}"
    num_columns = f"Number of columns: {column_count}"
    return [num_rows, num_columns]
