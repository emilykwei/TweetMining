import json
import spacy
from collections import defaultdict
from textblob import TextBlob
# from utils import merge
spacy_model = spacy.load("en_core_web_sm")


def find_sentiment(winners, tweets, retweets):
    answers = defaultdict(list) # map name of a winner to sentiment?
    scores = defaultdict(str) # map name of a winner to sentiment?
    for winner in winners:
        for tweet in tweets:
            if winner in tweet:
                blob = TextBlob(tweet.lower())
                score = blob.sentiment.polarity
                # print(tweet,score)
                answers[winner].append(score)
                
        for rt in retweets:
            if winner in rt:
                blob = TextBlob(rt.lower())
                score = blob.sentiment.polarity
                answers[winner].append(score)
                
    
    for winner in winners:
        if len(answers[winner]) == 0:
            continue
        score = sum(answers[winner])/len(answers[winner])
        # print(score)
        if score > .3:
            scores[winner] = f"Positive sentiment, {score}"
        elif score < -.3:
            scores[winner] = f"Negative sentiment, {score}"
        else:
            scores[winner] = f"Neutral sentiment, {score}"
        # print(answers)
        # print(scores)
    for x,y in scores.items():
        print(f"Winner {x} has {y}")
    
    with open("sentiment.json", 'w') as f:
        json.dump(scores, f)



    # answer["best dressed"] = [key for key, _ in best_dressed][0] if best_dressed else "N/A"

    # with open("winner_sentiment.json", 'w') as f:
    #     # Dump the dictionary to the file
    #     json.dump(answer, f)

# with open("text.json", "r") as file:
#     text = json.load(file)
# with open("retweet.json", "r") as file:
#     retweet = json.load(file)
# find_sentiment(["ben affleck","daniel day-lewis","maggie smith","argo"], text, retweet)