import json
import spacy
from collections import defaultdict
from textblob import TextBlob
# from utils import merge


def find_sentiment(winners, tweets, retweets):
    answers = defaultdict(list) # map name of a winner to sentiment?
    spacy_model = spacy.load("en_core_web_sm")
    for winner in winners:
        for tweet in tweets:
            if winner in tweet:
                blob = TextBlob(tweet)
                score = blob.sentiment.polarity
                answers[winner].append(score)
                
        for rt in retweets:
            if winner in rt:
                blob = TextBlob(rt)
                score = blob.sentiment.polarity
                answers[winner].append(score)
                
    
    for winner in winners:
        pass



    # answer["best dressed"] = [key for key, _ in best_dressed][0] if best_dressed else "N/A"

    # with open("winner_sentiment.json", 'w') as f:
    #     # Dump the dictionary to the file
    #     json.dump(answer, f)
find_sentiment(["Joaquin Phoenix"], ["Joaquin Phoenix is the best actor ever"], [])