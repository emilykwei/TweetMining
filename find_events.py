from collections import defaultdict 
import utils

def find_parties(text, retweet):
    for t in text:
        t = utils.clean_text(t)
        if "party" in t or "parties" in t:
            

def find_performances(text, retweet):
    pass