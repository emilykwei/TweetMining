import re
import json
import spacy
from collections import defaultdict
import utils

def nominees(category, text, retweet):
    patterns = []
    patterns.append(r'(?i)([a-z\s]+)(?:wins|winning|won) best ([a-z\s]+)\.')
    # patterns.append(r'(?i)([a-z\s]+)(?:wins|winning|won) best ([a-z\s]+)\.')
    i = 0
    for t in text:
        i+=1
        print("original: ", t)
        t = utils.clean_text(t)
        print("cleaned: ", t)
        if (i>20):
            break
        # for pattern in patterns:
        #     for match in re.finditer(pattern, t):
        #         match_text = match.group(0)
        #         pattern_counts[match_text] += 1
        #         matches_dict[match_text] = pattern_counts[match_text]



    # nominee = []
    # return nominee

