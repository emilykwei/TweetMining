import re
import json
from collections import defaultdict
import utils

# Initialize a dictionary to store the counts of each pattern
pattern_counts = defaultdict(int)

def find_and_count_patterns(text):
    text = utils.clean_text(text)
    
    patterns = [
        r'\bbest\b.*?\b(picture|drama|musical|film)\b',
        r'\bbest (tv|television)\b.*?\b(drama|musical)\b',
        r'\bcecil.*?\baward\b',
        r'\bbest performance by\b.*?\b(musical|picture|tv|television|drama)\b'
    ]
    
    matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            match_text = match.group(0)
            pattern_counts[match_text] += 1
            matches.append((match_text, pattern_counts[match_text]))
            
    return matches

def find_categories(text, retweet):
    patterns = [
        r'\bbest\b.*?\b(picture|drama|musical|film)\b',
        r'\bbest (tv|television)\b.*?\b(drama|musical)\b',
        r'\bcecil.*?\baward\b',
        r'\bbest performance by\b.*?\b(musical|picture|tv|television|drama)\b'
    ]

    matches_dict = {}
    
    for t in text:
        t = utils.clean_text(t)
    
        for pattern in patterns:
            for match in re.finditer(pattern, t):
                match_text = match.group(0)
                pattern_counts[match_text] += 1
                matches_dict[match_text] = pattern_counts[match_text]

    for rt in retweet:
        rt = utils.clean_text(rt)    

        for pattern in patterns:
            for match in re.finditer(pattern, rt):
                match_text = match.group(0)
                pattern_counts[match_text] += 2
                matches_dict[match_text] = pattern_counts[match_text]
    
    categories_counter = utils.merge(matches_dict)
    
    x = 15

    # Initialize an empty list to store categories
    categories = []

    # Loop through the Counter object
    for category, count in categories_counter.items():
        if count > x:
            categories.append(category)

    answer = {"categories": categories}

    with open("categories.json", 'w') as f:
        # Dump the dictionary to the file
        json.dump(answer, f)
    
    return categories