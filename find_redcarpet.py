import json
import spacy
from collections import defaultdict
from textblob import TextBlob
from utils import merge


def find_redcarpet(redcarpet):
    answer = {"best dressed": "",
              "worst dressed": "",
              "most discussed": "",
              "most controversial": ""}
    
    stop_words = ["golden", "globes", "globe", "goldenglobe", "goldenglobes"]

    best_dressed = defaultdict(int)
    worst_dressed = defaultdict(int)
    discussed = defaultdict(int)
    controversial = defaultdict(int)

    spacy_model = spacy.load("en_core_web_md")

    for rc in redcarpet:
        
        spacy_output = spacy_model(rc)
        blob = TextBlob(rc)
        sentiment_polarity = blob.sentiment.polarity

        for token in spacy_output.ents:
            if (token.label_ == "PERSON" or token.text.istitle()) and all(word.lower() not in stop_words for word in token.text.split()):
                discussed[token.text] += 1

                if sentiment_polarity > 0.5 or sentiment_polarity < -0.5:
                    controversial[token.text] += 1

                elif sentiment_polarity > 0.2:
                    best_dressed[token.text] += 1

                elif sentiment_polarity < 0.15:
                    worst_dressed[token.text] += 1

    best_dressed = merge(best_dressed).most_common(1)
    worst_dressed = merge(worst_dressed).most_common(1)
    discussed = merge(discussed).most_common(1)
    controversial = merge(controversial).most_common(1)

    answer["best dressed"] = [key for key, _ in best_dressed][0] if best_dressed else "N/A"
    answer["worst dressed"] = [key for key, _ in worst_dressed][0] if worst_dressed else "N/A"
    answer["most discussed"] = [key for key, _ in discussed][0] if discussed else "N/A"
    answer["most controversial"] = [key for key, _ in controversial][0] if controversial else "N/A"

    with open("redcarpet.json", 'w') as f:
        # Dump the dictionary to the file
        json.dump(answer, f)