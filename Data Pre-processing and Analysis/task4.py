""" 
COMP20008 Semester 2
Assignment 1 Task 4
"""

# Task 4 - Text Preprocessing (1 mark)
import pandas as pd
import re

def task4(dataset_filename, output_filename):
    # Implement Task 4 here
    df = pd.read_csv(dataset_filename)
    # Save the original title 
    title = df['title']
    # Remove all non-alphabetic characters other than space from 'title'
    df['title'] = df['title'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))
    # Convert all capital letters to lower case
    df['title'] = df['title'].str.lower()
    # Tokenize each title into a list of words
    words = df['title'].apply(lambda x: x.split())
    # Create an additional column 'words'
    df['words'] = words
    # Keep the original title
    df['title'] = title
    # Save the modified dataframe to a new CSV file 
    df.to_csv(output_filename, index=False)
    return
