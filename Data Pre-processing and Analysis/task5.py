""" 
COMP20008 Semester 2
Assignment 1 Task 5
"""

# Task 5 - Preliminary Analysis (1 mark)
import pandas as pd
import re
import json
from collections import defaultdict
import matplotlib.pyplot as plt

def task5(dataset_filename, json_output_filename, plot_output_filename):
    # Implement Task 5 here
    df = pd.read_csv(dataset_filename)
    # Remove all non-alphabetic characters other than space from 'title'
    df['title'] = df['title'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))
    # Convert all capital letters to lower case
    df['title'] = df['title'].str.lower()
    # Tokenize each title into a list of words
    words = df['title'].apply(lambda x: x.split())
    
    # Create a dictionary to get the vocabulary of all words from "words" and the times appeared
    word_occurrences = defaultdict(int)
    # Create a set to get the words that appear in at least five article titles
    processed_word_occurrences = defaultdict(int)
    # To store encountered words in each word list
    word_lists_encountered = set()  
    for words_list in words:
        # Set to keep track of words in this word list
        word_list_encountered = set()  
        for word in words_list:
            # Only count the word once per word list
            if word not in word_list_encountered:  
                word_list_encountered.add(word)
                processed_word_occurrences[word] += 1
                if processed_word_occurrences[word] >= 5:
                    word_lists_encountered.add(word)
    # Create a dictionary to get the total number of views according to the word selected
    views_count = defaultdict(int)
    for word in word_lists_encountered:
        for view, word_present in zip(df['views'], words.apply(lambda x: word in x)):
            if word_present:
                views_count[word] += view
    # Get the average number of views and store them in a dictionary 
    word_avg_views = {}
    for word, value in views_count.items():
        word_avg_views[word] = round(value/processed_word_occurrences[word])
    # Serialize the dictionary and write to json file
    with open(json_output_filename, "w") as outfile:
        json.dump(word_avg_views, outfile, indent=4)

    # Sort the words by average views and select the top 5
    top_words = sorted(word_avg_views.items(), key=lambda x: x[1], reverse=True)[:5]
    top_words, top_avg_views = zip(*top_words)
    
    # Create a bar chart
    plt.figure(figsize=(12,7))
    plt.rc('font', size=14)
    plt.bar(top_words, top_avg_views)
    plt.xlabel('Words')
    plt.ylabel('Average Views')
    plt.title('Top 5 Words with Highest Average Views')
    
    # Save the bar chart
    plt.tight_layout()
    plt.savefig(plot_output_filename)
    return 

