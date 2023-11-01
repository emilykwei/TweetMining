import json
import re
import spacy
from collections import defaultdict 
# from collections import Counter

# temp for easier testing purposes:
with open("text.json", "r") as file:
    text = json.load(file)
with open("retweet.json", "r") as file:
    retweet = json.load(file)

def winners(category, text, retweet):
    winners = defaultdict(int)
    spacy_model = spacy.load("en_core_web_sm")
    doc = spacy_model(category)
    threshold = 0.40
    p1 = r'(?i)([a-z\s]+)(?:wins|winning|won) (best [a-z\s]+)\.'
    p2 = r'(?i)(best [a-z\s]+) goes to ([a-z\s]+)\.'

    for s in text:
        s = s.lower()
        # if "claire danes" in s:
        #     print(s)
        match1 = re.search(p1, s)
        if match1:
            if doc.similarity(spacy_model(match1.group(2))) > threshold:
                # print(match1.group(1),"|", match1.group(2), "|", match1.group(0))
                winners[match1.group(1)] += 1
        else:
            match1 = re.search(p2, s)
            if match1:
                if doc.similarity(spacy_model(match1.group(1))) > threshold:
                    # print(match1.group(1),"|", match1.group(2), "|", match1.group(0))
                    winners[match1.group(2)] += 1
            else:
                
    return winners

x= winners("best performance by an actress in a television series ", text, retweet)
for w,count in x.items():
    print(w, count)

# TODO: add retweets
# update the group to be the actual entity
# figure out how to make this more accurate...
# merge dictionary to combine entries
