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
                # print(doc.similarity(spacy_model(match1.group(2))), match1.group(0))
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
                            if any(token.ent_type_ == "PERSON" for token in chunk):
                                continue
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
                    # print(doc.similarity(spacy_model(match1.group(1))), match1.group(0))
                    group = match1.group(2)
                    if "actor" in category or "actress" in category or "director" in category:
                        for ent in spacy_model(match1.group(2)).ents:
                            winners[ent.text] += 1
                    else:
                        doc2 = spacy_model(match1.group(2))
                        for chunk in doc2.noun_chunks:
                            win = chunk.text.lstrip()
                            if any(token.ent_type_ == "PERSON" for token in chunk):
                                continue
                            winners[win] += 1
    for s in text:
        win_helper(s)
    for s in retweet:
        win_helper(s)

    winners = merge(winners)
    # for x,y in winners.items():
    #     if y>1:
    #         print(x,y)
    winner = ""
    max_frequency = 0
    # go through winners and choose top one, maybe apply more filtering?
    for key, frequency in winners.items():
        if frequency > max_frequency:
            if len(key)==1: #why is this even capturing single letters?
                continue
            max_frequency = frequency
            winner = key
    return winner

# print(winners("best screenplay - motion picture", text, retweet)) #django unchained
# print(winners("best director - motion picture", text, retweet)) #ben affleck
# print(winners("best performance by an actress in a television series - comedy or musical", text, retweet)) #lena dunham
# print(winners("best foreign language film", text, retweet)) #amour
# print(winners("best performance by an actor in a supporting role in a motion picture", text, retweet)) #christoph waltz
# print(winners("best performance by an actress in a supporting role in a series, mini-series or motion picture made for television", text, retweet)) #maggie smith



# x= winners("best performance by an actress in a television series - comedy or musical", text, retweet)
# x= winners("best foreign language film", text, retweet) # gives argo which is wrong..
# x= winners("best performance by an actress in a supporting role in a series, mini-series or motion picture made for television", text, retweet) # gives argo which is wrong..
# print(x)

# TODO:  #add retweets
# update the group to be the actual entity #done i think
# figure out how to make this more accurate... ... 
# merge dictionary to combine entries   # should be good
# return the top winner?
