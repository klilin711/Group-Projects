""" 
COMP20008 Semester 2
Assignment 1 Task 3
"""

# Task 3 - Preliminary Visualisation (1 mark)
import pandas as pd
import matplotlib.pyplot as plt

def task3(dataset_filename, output_filename):
    # Implement Task 3 here
    df = pd.read_csv(dataset_filename)
    df = df[df['when'] <= 14400]
    plt.figure(figsize=(12, 7))
    plt.scatter(x=df['when'],
                y=df['views'],
                color='blue', 
                alpha=0.3,
                label='Number of Views vs Minutes Ago'
                )
    # More formatting options
    plt.grid()
    plt.xlabel('Minutes Ago')
    plt.ylabel('Number of Views')
    plt.title('Article Views vs Time Since Publication')
    plt.legend()
    # Saving the file
    plt.savefig(output_filename)                             
    return 
