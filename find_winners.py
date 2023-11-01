import json
import re
import spacy
from collections import defaultdict 
from utils import merge
# from collections import Counter

# temp for easier testing purposes:
with open("text.json", "r") as file:
    text = json.load(file)
with open("retweet.json", "r") as file:
    retweet = json.load(file)

def winners(category, text, retweet):
    winners = defaultdict(int)
    spacy_model = spacy.load("en_core_web_sm")
    category = re.sub(r'[^\w\s]', '', category)
    # category = category.replace("-", "")
    category = category.replace("  ", " ")
    # print(category)
    doc = spacy_model(category)
    threshold = 0.70
    p1 = r'(?i)([a-z\s]+)(?:wins|winning|won) (best [a-z\s]+)'
    p2 = r'(?i)(best [a-z\s]+) goes to ([a-z\s]+)'
    # for s in text:
    def win_helper(s):
        s = s.replace("golden globes","").replace("goldenglobes","").lower()
        # if "claire danes" in s:
        #     print(s)
        match1 = re.search(p1, s)
        if match1:
            if doc.similarity(spacy_model(match1.group(2))) > threshold:
                # print(match1.group(1),"|", match1.group(2), "|", match1.group(0))
                if "actor" in category or "actress" in category or "director" in category:
                    for ent in spacy_model(match1.group(1)).ents:
                        winners[ent.text] += 1
                        # print(ent.text)
                        # print(ent.text, ent.label_)
                else:
                    # winners[match1.group(1)] += 1
                    doc2 = spacy_model(match1.group(1))
                    for chunk in doc2.noun_chunks:
                            win = chunk.text.lstrip() # remove leading white space
                            winners[win] += 1
                        # print(chunk.text)
                # for ent in spacy_model(match1.group(1)).ents:
                #     # print(ent.text, ent.label_)
                #     winners[ent.text] += 1
                # winners[match1.group(1)] += 1   
        else:
            match1 = re.search(p2, s)
            if match1:
                if doc.similarity(spacy_model(match1.group(1))) > threshold:
                    group = match1.group(2)
                    if "actor" in category or "actress" in category or "director" in category:
                        for ent in spacy_model(match1.group(2)).ents:
                            winners[ent.text] += 1
                    else:
                        doc2 = spacy_model(match1.group(2))
                        for chunk in doc2.noun_chunks:
                            win = chunk.text.lstrip()
                            winners[win] += 1
    for s in text:
        win_helper(s)
    for s in retweet:
        win_helper(s)
    return winners

x= winners("best screenplay - motion picture", text, retweet)
# print(x)
x = merge(x)
for w,count in x.items():
    if count>1:
        print(w, count)

# TODO: add retweets
# update the group to be the actual entity
# figure out how to make this more accurate...
# merge dictionary to combine entries
