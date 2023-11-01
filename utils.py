import spacy
import re
import json
from collections import Counter
from collections import defaultdict

def clean_text(text, lowercase = True):
    # Convert text to lowercase
    if lowercase == True:
        text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Replace multiple consecutive whitespaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def merge(dict):
    nlp = spacy.load("en_core_web_md")

    threshold = 0.80
    sorted_items = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    merged_dict = {}

    for key1, count1 in sorted_items:
        inserted = False
        key1_doc = nlp(key1.lower())
        
        if not key1_doc.has_vector:
            continue
            
        for key2 in list(merged_dict.keys()):
            key2_doc = nlp(key2.lower())
            
            if not key2_doc.has_vector:
                continue
                
            similarity = key1_doc.similarity(key2_doc)
            
            if similarity > threshold:
                merged_dict[key2] += count1
                inserted = True
                break
                
        if not inserted:
            merged_dict[key1] = count1

    return Counter(dict)