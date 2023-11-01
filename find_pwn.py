import spacy
import utils
import re
# from textblob import TextBlob
from collections import defaultdict


def find_pwn(category, text, retweet):
    award_not_for_human = True

    if 'actor' in category or 'actress' in category or 'director' in category:
        award_not_for_human = False

    # Load the spaCy model
    spacy_model = spacy.load("en_core_web_md")
    # Loop through each category

    p = ["introduce", "present", "announce", "give"]
    p = [
        "introduce", "present", "announce", "unveil", "hand out", "give",
        "award", "host", "on stage", "welcome", "kick off",
        "reveal", "honor", "celebrate", "nab"
    ]

    n = ["nomin", "chosen", "up for", "select", "shortlist", "in the running"]
    w = [
        "win", "takes home", "brings home", "award", "honor",
        "victor", "triumph", "congrat", "accept", "receive", "clinch",
        "nab", "scoop", "secure", "earn", "dedicate", "celebrate", "got", "won", "goes to"
    ]

    n = [
        "nomin", "chosen", "up for", "select", "shortlist", "in the run",
        "contender", "candidate", "acknowledge", "recognize", "on the list",
        "potential winner", "finalist", "belong", "wish", "luck",
        "beat", "deserve", "should", "would", "angry", "sorry","didn", "not"
    ]

    # stop_words = ['i', 'you', 'he', 'she', 'this', 'that', 'they', 'somebody', 'goldenglobes', 'golden', 'globes',
    #               'everyone', 'it', 'me', 'guys', 'any', 'all', 'what', 'award', 'anything', 'mom', 'nominee',
    #               'best', 'who', 'wife', 'stage', 'congratulations', 'night', 'win', 'another', 'drama', 'motion', 'ovation', 'a',
    #               'people', 'tv', 'talk', 'musical', 'we', 'foreign', 'word', 'fingers', 'idk', 'favorite', 'u', 'comedy', 
    #               'night', 'none', 'congrats', 'game', 'changer', 'nominations', 'film', 'films', 'more', 'your', 'god', 'themselves', 
    #               'movies', 'subtitles', 'trailers', 'director', 'movie', 'good', 'awards', 'same', 'category', 'comedy', 'mtv', 'fav', 
    #               'girls', 'boys', 'ladies', 'aaaaand', 'kid', 'angry', 'her', 'opinion', 'animated', 'attention', 'kids', 'musicals', 
    #               'life', 'my', 'rest', 'bad', 'anyone', 'comedies', 'expensive']

    stop_words = ['i','you','he','she','this','that','they','the','somebody','goldenglobes','golden globes',
                    'the golden globes', 'everyone', 'it', 'me','guys','any','all']

    presenters = defaultdict(int)
    winners = defaultdict(int)
    nominees = defaultdict(int)
    category_doc = spacy_model(category)
    def win_helper(s):
        threshold = .7
        s = s.replace("golden globes","").replace("goldenglobes","").lower()
        match1 = re.search(r'(?i)([a-z\s]+)(?:wins|winning|won) (best [a-z\s]+)', s)
        if match1:
            if category_doc.similarity(spacy_model(match1.group(2))) > threshold:
                if "actor" in category or "actress" in category or "director" in category:
                    for ent in spacy_model(match1.group(1)).ents:
                        winners[ent.text] += 1
                else:
                    doc2 = spacy_model(match1.group(1))
                    for chunk in doc2.noun_chunks:
                            win = chunk.text.lstrip() 
                            if any(token.ent_type_ == "PERSON" for token in chunk):
                                continue
                            winners[win] += 1
        else:
            match1 = re.search(r'(?i)(best [a-z\s]+) goes to ([a-z\s]+)', s)
            if match1:
                if category_doc.similarity(spacy_model(match1.group(1))) > threshold:
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
        t = utils.clean_text(t, False)
        if keyword1 in t and (keyword2 in t or keyword3 in t):
            has_p = any(word in t for word in p)
            # has_w = any(word in t for word in w)
            has_n = any(word in t for word in n)

            # if not (has_p or has_w or has_n):
            if not (has_p or has_n):
                continue

            doc = spacy_model(t)
            # Find the start and end index of the category in the text
            start_idx = t.find(keyword1)
            end_idx = start_idx + len(keyword1)



            # Loop through noun chunks
            for chunk in doc.noun_chunks:
                if chunk.end_char <= start_idx:
                    if has_p:
                        if chunk.label_ == "PERSON" or chunk.text.istitle():
                            # if all(word.lower() not in stop_words for word in chunk.text.split()):
                            if chunk.text.lower() not in stop_words:
                                presenters[chunk.text.lower()] += 1

                    if has_n:
                        if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                            # if all(word.lower() not in stop_words for word in chunk.text.split()):
                            if chunk.text.lower() not in stop_words:
                                nominees[chunk.text.lower()] += 1

                    # if has_w:
                    #     if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                    #         if all(word.lower() not in stop_words for word in chunk.text.split()):
                    #             winners[chunk.text.lower()] += 1

                # elif chunk.end_char >= start_idx:
                #     if has_p:
                #         if chunk.label_ == "PERSON" or chunk.text.istitle():
                #             # if all(word.lower() not in stop_words for word in chunk.text.split()):
                #             if chunk.text.lower() not in stop_words:
                #                 presenters[chunk.text.lower()] += 1

                #     if has_n:
                #         if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                #             # if all(word.lower() not in stop_words for word in chunk.text.split()):
                #             if chunk.text.lower() not in stop_words:
                #                 nominees[chunk.text.lower()] += 1

                    # if has_w:
                    #     if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                    #         if all(word.lower() not in stop_words for word in chunk.text.split()):
                    #             winners[chunk.text.lower()] += 1
            # helper for winner
            win_helper(t)

    for t in retweet:

        # Check if the category exists in the text
        t = utils.clean_text(t, False)
        if keyword1 in t and (keyword2 in t or keyword3 in t):
            has_p = any(word in t for word in p)
            # has_w = any(word in t for word in w)
            has_n = any(word in t for word in n)

            # if not (has_p or has_w or has_n):
            if not (has_p or has_n):
                continue

            doc = spacy_model(t)
            # Find the start and end index of the category in the text
            start_idx = t.find(keyword1)
            end_idx = start_idx + len(keyword1)

            # Loop through noun chunks
            for chunk in doc.noun_chunks:
                if chunk.end_char <= start_idx:
                    if has_p:
                        if chunk.label_ == "PERSON" or chunk.text.istitle():
                            # presenters[chunk.text.lower()] = presenters.get(chunk.text.lower(), 0) + 1
                            # if all(word.lower() not in stop_words for word in chunk.text.split()):
                            if chunk.text.lower() not in stop_words:
                                presenters[chunk.text.lower()] += 2

                    if has_n:
                        if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                            # if all(word.lower() not in stop_words for word in chunk.text.split()):
                            if chunk.text.lower() not in stop_words:
                                nominees[chunk.text.lower()] += 2

                    # if has_w:
                    #     if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                    #         if all(word.lower() not in stop_words for word in chunk.text.split()):
                    #             winners[chunk.text.lower()] += 2

                # elif chunk.end_char >= start_idx:
                #     if has_p:
                #         if chunk.label_ == "PERSON" or chunk.text.istitle():
                #             # presenters[chunk.text.lower()] = presenters.get(chunk.text.lower(), 0) + 1
                #             if all(word.lower() not in stop_words for word in chunk.text.split()):
                #                 presenters[chunk.text.lower()] += 2

                #     if has_n:
                #         if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                #             if all(word.lower() not in stop_words for word in chunk.text.split()):
                #                 nominees[chunk.text.lower()] += 2

                    # if has_w:
                    #     if chunk.label_ == "PERSON" or award_not_for_human or chunk.text.istitle():
                    #         if all(word.lower() not in stop_words for word in chunk.text.split()):
                    #             winners[chunk.text.lower()] += 2
            # helper for winner
            win_helper(t)

    pc = utils.merge(presenters)
    wc = utils.merge(winners)
    nc = utils.merge(nominees)

    presenters = [key for key, _ in pc.most_common(2)]
    winners = [key for key, _ in wc.most_common(1)]
    nominees = [key for key, _ in nc.most_common(4)]

    if len(winners) == 0:
        winners = [key for key, _ in nc.most_common(1)]

    return presenters, winners, nominees
