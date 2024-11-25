# This assignment takes tweets, analyzes them, and returns a report based on the tweet's sentimental information
"""
CS1026a 2023
Assignment 03 Sentiment Analysis - sentiment_analysis.py
Allison Ye
251339668
aye28
November 17, 2023
 """


# Creates a dictionary with the sentimental words taken from the file and, their corresponding value
def read_keywords(keyword_file_name):
    # Initializing a dictionary for the keywords
    keyword_dictionary = {}
    try:
        with open(keyword_file_name) as file:
            # reads one line at a time, creating a dictionary with the key as the word,
            # and the value as the sentimental value
            for line in file:
                values = line.strip().split('\t')
                keyword = values[0]
                value = int(values[1])
                # connects the keyword and value together within the dictionary
                keyword_dictionary[keyword] = value
    # In the case the file could not be opened
    except IOError:
        print("Could not open file {}!".format(keyword_file_name))

    return keyword_dictionary

# Cleans up the tweet by only keeping alphabet characters and space,
# so that it can be analyzed and directly compared with sentimental words
def clean_tweet_text(tweet_text):
    # Initializing a string for the cleaned up tweet
    new_text = ''
    for char in tweet_text:
        # Only keeps alphabet characters or space and adds it to the new text
        if char.isalpha() or char.isspace():
            new_text += char
    # Converts the text into lowercase, as the keywords are all lowercase
    new_text = new_text.lower()
    return new_text

# Calculates the sentiment score for the tweet
def calc_sentiment(tweet_text, keyword_dict):
    # Initializing the sentiment score, starting from 0
    sentiment_score = 0
    tweet_word_list = tweet_text.split()

    # Compares the words from the tweet to the keyword dictionary,
    # if the word has a value, it is added to the sentiment score total
    for word in tweet_word_list:
        if word in keyword_dict:
            sentiment_score += keyword_dict[word]

    return sentiment_score

# classifies different sentimental scores as positive, negative or neutral
def classify(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"

# Reads the tweets from the csv file, and save them into a list
def read_tweets(tweet_file_name):
    # initializes a list for the tweet data
    tweet_list = []
    try:
        with open(tweet_file_name) as file:
            for line in file:
                # Splits up the words from the tweet to be put into its key value pair
                values = line.strip().split(',')
                # Initializes a dictionary for the data from the tweet
                data = {}

                # Save the tweet value into its corresponding key
                data['date'] = values[0]
                data['text'] = clean_tweet_text(values[1])
                data['user'] = values[2]
                data['retweet'] = int(values[3])
                data['favorite'] = int(values[4])
                data['lang'] = values[5]
                data['country'] = values[6]
                data['state'] = values[7]
                data['city'] = values[8]
                # Checks to see if the latitude is defined
                if not values[9] == 'NULL':
                    data['lat'] = float(values[9])
                else:
                    data['lat'] = 'NULL'

                # Checks to see if the longitude is defined
                if not values[10] == 'NULL':
                    data['lon'] = float(values[10])
                else:
                    data['lon'] = 'NULL'

                # Adds all tweet data into the list
                tweet_list.append(data)

    # In the case the file could not be opened
    except IOError:
        print(f"Could not open file {tweet_file_name}!")

    return tweet_list

# Prepares the information that will be late added to the outputted report
def make_report(tweet_list, keyword_dict):
    # Initializes the values that will be added to the report
    sum_favorite = 0
    sum_negative = 0
    sum_neutral = 0
    sum_positive = 0
    sum_retweet = 0
    sum_tweets = len(tweet_list)
    total_sentiment_score = 0.0
    favorite_sentiment_score = 0.0
    retweet_sentiment_score = 0.0
    country_sentiment_dict = {}

    # calculating each value from the tweet data list
    for one_tweet in tweet_list:

        # Calculates the total sentiment of all tweets, by taking sentiment values from the dictionary
        sentiment_score = calc_sentiment(one_tweet['text'], keyword_dict)
        total_sentiment_score += sentiment_score

        # Calculates the number of tweets that have been liked at least once
        if one_tweet['favorite'] > 0:
            sum_favorite += 1
            favorite_sentiment_score += sentiment_score

        # Calculates the average sentimental value of the tweets in the tweet list
        # that have been favorited/liked at least once.
        if sum_favorite > 0:
            avg_favorite_sentiment = round(favorite_sentiment_score / sum_favorite, 2)
        # If the value is 0
        else:
            avg_favorite_sentiment = "NAN"

        # Calculates the number of tweets in the tweet list that have been retweeted at least once
        if one_tweet['retweet'] > 0:
            sum_retweet += 1
            retweet_sentiment_score += sentiment_score

        # The average sentiment value of all tweets that have been retweeted at least once
        if sum_retweet > 0:
            avg_retweet_sentiment = round(retweet_sentiment_score / sum_retweet, 2)
        # If the value is 0
        else:
            avg_retweet_sentiment = "NAN"

        # Calculating the average total sentiment score
        if sum_tweets > 0:
            avg_total_sentiment = round(total_sentiment_score / sum_tweets, 2)
        else:
            avg_total_sentiment = "NAN"

        # Checking with classification the sentiment score is
        if classify(sentiment_score) == "positive":
            sum_positive += 1
        elif classify(sentiment_score) == "negative":
            sum_negative += 1
        elif classify(sentiment_score) == "neutral":
            sum_neutral += 1

        # Create a country sentiment dictionary that holds the country and is related sentiment score
        country = one_tweet['country']
        if not country == 'NULL':
            # if this country is counted for the first time, its key/values is added in the dictionary
            if country not in country_sentiment_dict:
                country_sentiment_dict[country] = {'country_sum_sentiment': sentiment_score, 'country_sum_tweets': 1,
                                                   'country_average_sentiment': sentiment_score}
            # if this country is not counted for the first time
            else:
                country_sentiment_dict[country]['country_sum_sentiment'] += sentiment_score
                country_sentiment_dict[country]['country_sum_tweets'] += 1
                country_sentiment_dict[country]['country_average_sentiment'] = country_sentiment_dict[country][
                                                                                   'country_sum_sentiment'] / \
                                                                               country_sentiment_dict[country][
                                                                                   'country_sum_tweets']

    # Sorting the country's average sentiment from highest to lowest
    sorted_by_country_average_sentiment = sorted(country_sentiment_dict.items(),
                                                 key=lambda i: i[1]['country_average_sentiment'], reverse=True)

    # Take the top five countries and save them into a list
    top_five_countries = []
    for i in sorted_by_country_average_sentiment[:5]:
        country_name = i[0]
        top_five_countries.append(country_name)

    # Prepare the top five countries string to be printed in the output file
    top_five_country_names_str = ', '.join(top_five_countries)

    # Adds each value to its corresponding key
    report = {
        'avg_favorite': avg_favorite_sentiment,
        'avg_retweet': avg_retweet_sentiment,
        'avg_sentiment': avg_total_sentiment,
        'num_favorite': sum_favorite,
        'num_negative': sum_negative,
        'num_neutral': sum_neutral,
        'num_positive': sum_positive,
        'num_retweet': sum_retweet,
        'num_tweets': sum_tweets,
        'top_five': top_five_country_names_str
    }

    return report

# Takes the report information, and save them into an output file
def write_report(report, output_file):
    try:
        # Opens the file that will be used to save the information,
        # printing out each line indicating the sentiment analysis result
        with open(output_file, 'w') as file:
            file.write("Average sentiment of all tweets: {}".format(report['avg_sentiment']))
            file.write("\nTotal number of tweets: {}".format(report['num_tweets']))
            file.write("\nNumber of positive tweets: {}".format(report['num_positive']))
            file.write("\nNumber of negative tweets: {}".format(report['num_negative']))
            file.write("\nNumber of neutral tweets: {}".format(report['num_neutral']))
            file.write("\nNumber of favorited tweets: {}".format(report['num_favorite']))
            file.write("\nAverage sentiment of favorited tweets: {}".format(report['avg_favorite']))
            file.write("\nNumber of retweeted tweets: {}".format(report['num_retweet']))
            file.write("\nAverage sentiment of retweeted tweets: {}".format(report['avg_retweet']))
            file.write("\nTop five countries by average sentiment: {}".format(report['top_five']))

        # Informing the user that the report has been made
        print("Wrote report to {}".format(output_file))

    # In the case the file could not be opened
    except IOError:
        print("Could not open file {}".format(output_file))