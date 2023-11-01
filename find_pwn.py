import spacy
import utils
from collections import defaultdict 

def find_pwn(category, text, retweet):
    print("Category: ", category)
    award_not_for_human = True
    if 'actor' in category or 'actress' in category or 'director' in category:
        award_not_for_human = False
    # Load the spaCy model
    spacy_model = spacy.load("en_core_web_sm")
    # Loop through each category
    p = [
        "introduce", "present", "announce", "unveil", "hand out", "give", 
        "award", "host", "on stage", "welcome", "kick off", "opens with", 
        "reveal", "showcase", "honor", "celebrate", "nab"
    ]

    w= [
        "win", "takes home", "brings home", "reels in", "award", "honor",
        "victorious", "triumph", "congrat", "accept", "receive", "clinch",
        "nab", "scoop", "secure", "earn", "dedicate", "celebrate"
    ]

    n = [
        "nomin", "chosen", "up for", "select", "shortlist", "in the running",
        "contender", "candidate", "acknowledge", "recognize", "on the list",
        "potential winner", "made the cut", "finalist", "belong", "wish", "luck",
        "beat", "deserve", "should", "would", "angry", "sorry", "poor", "didn", "not"
    ]
    
    stop_words = ['i','you','he','she','this','that','they','the','somebody','goldenglobes','golden globes',
                    'the golden globes', 'everyone', 'it', 'me','guys','any','all']

    presenters = defaultdict(int)
    winners = defaultdict(int)
    nominees = defaultdict(int)
    if (category.split()[0] == "best"):
        keyword1 = category.split()[1]
        keyword2 = category.split()[-1]
        keyword3 = category.split()[-2]
    else:
        keyword1 = "cecil"
        keyword2 = "mille"
        keyword3 = "mille"
    # Loop through each text

    for t in text:

        # Check if the category exists in the text
        t = utils.clean_text(t,False)
        if keyword1 in t and (keyword2 in t or keyword3 in t):
            has_p = any(word in t for word in p)
            has_w = any(word in t for word in w)
            has_n = any(word in t for word in n)
            
            if not (has_p or has_w or has_n):
                continue
                
            doc = spacy_model(t)
            # print("doc: ", doc)
            # print("keyword: ", keyword)
            # Find the start and end index of the category in the text
            start_idx = t.find(keyword1)
            end_idx = start_idx + len(keyword1)
            
            # Loop through noun chunks
            for chunk in doc.noun_chunks:
                if chunk.end_char <= start_idx:
                    # print("chunk.text:", chunk.text)
                    if has_p:
                        if chunk.label_ == "PERSON" or chunk.text.istitle():
                            if chunk.text.lower() not in stop_words:
                                presenters[chunk.text.lower()] += 2

                    if has_n:
                        if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                            if chunk.text.lower() not in stop_words:
                                nominees[chunk.text.lower()] += 2

                            
                    if has_w:
                        if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                            if chunk.text.lower() not in stop_words:
                                winners[chunk.text.lower()] += 2


    for t in retweet:

        # Check if the category exists in the text
        t = utils.clean_text(t,False)
        if keyword1 in t and (keyword2 in t or keyword3 in t):
            has_p = any(word in t for word in p)
            has_w = any(word in t for word in w)
            has_n = any(word in t for word in n)
            
            if not (has_p or has_w or has_n):
                continue
                
            doc = spacy_model(t)
            # print("doc: ", doc)
            # print("keyword: ", keyword)
            # Find the start and end index of the category in the text
            start_idx = t.find(keyword1)
            end_idx = start_idx + len(keyword1)
            
            # Loop through noun chunks
            for chunk in doc.noun_chunks:
                if chunk.end_char <= start_idx:
                    # print("chunk.text:", chunk.text)
                    if has_p:
                        if chunk.label_ == "PERSON" or chunk.text.istitle():
                            # presenters[chunk.text.lower()] = presenters.get(chunk.text.lower(), 0) + 1
                            if chunk.text.lower() not in stop_words:
                                presenters[chunk.text.lower()] += 1

                    if has_n:
                        if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                            if chunk.text.lower() not in stop_words:
                                nominees[chunk.text.lower()] += 1

                            
                    if has_w:
                        if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                            if chunk.text.lower() not in stop_words:
                                winners[chunk.text.lower()] += 1


    pc = utils.merge(presenters)
    wc = utils.merge(winners)
    nc = utils.merge(nominees)
    
    presenters = [key for key, _ in pc.most_common(2)]
    winners = [key for key, _ in wc.most_common(1)]
    nominees = [key for key, _ in nc.most_common(4)]
    #2 1 4
    
    # print("Presenters:", presenters)
    # print("Winners:", winners)
    print("Nominees:", [(key,value) for key,value in nc.most_common(15)])
    return presenters,winners,nominees