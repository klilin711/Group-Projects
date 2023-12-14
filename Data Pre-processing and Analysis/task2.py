""" 
COMP20008 Semester 2
Assignment 1 Task 2
"""

# Task 2 - Data Cleaning (2 marks)
import pandas as pd
import re

def task2(dataset_filename, output_filename):
    # Implement Task 2 here
    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(dataset_filename)
    # Apply the functions to the 'views' and 'when' columns
    df['views'] = df['views'].apply(get_views)
    df['when'] = df['when'].apply(get_minutes)
    # Save the modified dataframe to a new CSV file 
    df.to_csv(output_filename, index=False)
    return 

# Extract and convert views to integers
def get_views(views):
    views = views.split()[0]
    if 'K' in views:
        views = int(float(views.replace('K', '')) * 1000)
    elif 'M' in views:
        views = int(float(views.replace('M', '')) * 1000000)
    else:
        views = int(views)
    return views

# Convert the 'when' column to minutes 
def get_minutes(when):
    # Returns a list of tuples and access the first tuple in the list
    time, unit = re.findall(r'(\d+) (\w+) ago', when)[0]  
    # Time is used to perform calculations, hence it should be converted into integer
    time = int(float(time))
    if unit in ['minute', 'minutes']:
        return time
    elif unit in ['hour', 'hours']:
        return time * 60
    elif unit in ['day', 'days']:
        return time * 24 * 60
    elif unit in ['week', 'weeks']:
        return time * 7 * 24 * 60
    elif unit in ['month', 'months']:
        return time * 30 * 24 * 60
    elif unit in ['year', 'years']:
        return time * 12 * 30 * 24 * 60
    elif unit in ['second', 'seconds']:
        return 1  # Count any second as 1 minute
