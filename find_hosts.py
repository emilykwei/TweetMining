import re
import json
import spacy
from collections import defaultdict 
import utils

def find_host_tweets(strings):
    result = []
    for s in strings:
        pattern = re.escape("host")
        regex = re.compile(pattern)
        substrings = re.split(r'[.!?]', s) # if one string contains two sentences (contains char './!/?'), this line breaks them into two
        for sub in substrings:
            if regex.search(sub):
                result.append(sub)
    return result

def add_host_tweets(text, retweet, file):
    all_host_tweets = find_host_tweets(text) + find_host_tweets(retweet)

    # initiating potential answers dictionary
    hosts = defaultdict(int)

    spacy_model = spacy.load("en_core_web_sm") # <- english
    for tweet in all_host_tweets:
        spacy_output = spacy_model(tweet)
        for token in spacy_output.ents:
            if token.label_ == "PERSON":
                hosts[token.text] += 1

    # check result
    hosts_counter = utils.merge(hosts)
    top_keys = [key for key, _ in hosts_counter.most_common(2)] # select top two candidate

    answer = {"hosts": top_keys}

    with open(file, 'w') as f:
        # Dump the dictionary to the file
        json.dump(answer, f)