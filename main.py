# This file takes information from the user, and imports the code from the sentimental_analysis file to analyze
# the user's inputted files
"""
CS1026a 2023
Assignment 03 Sentiment Analysis - main.txt
Allison Ye
251339668
aye28
November 17, 2023
 """


# Import the sentiment_analysis module
from sentiment_analysis import *

def main():
    # Asks user to input a .tsv file to save it into a keyword dictionary
    keyword_file_name = input("Input file name (.tsv file): ")
    # Makes sure the file is a .tsv file
    if not keyword_file_name.endswith('.tsv'):
        raise Exception("Must have tsv file extension!")

    # Asks user to input a .csv file to analyze
    tweet_file_name = input("Input tweet file name (.csv file): ")
    # Makes sure the file is a .csv file
    if not tweet_file_name.endswith('.csv'):
        raise Exception("Must have csv file extension!")

    # Asks user to input a .txt file to return the report into
    report_file_name = input("Input filename to output report in (.txt file): ")
    # Makes sure the file is a .txt file
    if not report_file_name.endswith('.txt'):
        raise Exception("Must have txt file extension!")

    # Calls the functions involving the keywords and the information of the tweet
    keyword_dict = read_keywords(keyword_file_name)
    tweet_list = read_tweets(tweet_file_name)
    # In the case the list or dictionary is empty
    if not keyword_dict or not tweet_list:
        raise Exception("Tweet list or keyword dictionary is empty!")

    # calls the function that writes the report
    report = make_report(tweet_list, keyword_dict)
    write_report(report, report_file_name)

# calls the main function
main()
