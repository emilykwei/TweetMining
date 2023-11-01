import re
import json
from collections import defaultdict
import utils
import spacy
from spacy.matcher import Matcher
# import utils
# from collections import defaultdict 

# Initialize a dictionary to store the counts of each pattern
# pattern_counts = defaultdict(int)

# def clean_text(text):
#     # Convert text to lowercase
#     text = text.lower()
#     # Remove punctuation
#     text = re.sub(r'[^\w\s]', '', text)
#     # Replace multiple consecutive whitespaces with a single space
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def find_and_count_patterns(text):
#     text = utils.clean_text(text)
    
#     patterns = [
#         r'\bbest\b.*?\b(picture|drama|musical|film)\b',
#         r'\bbest (tv|television)\b.*?\b(drama|musical)\b',
#         r'\bcecil.*?\baward\b',
#         r'\bbest performance by\b.*?\b(musical|picture|tv|television|drama)\b'
#     ]
    
#     matches = []
#     for pattern in patterns:
#         for match in re.finditer(pattern, text):
#             match_text = match.group(0)
#             pattern_counts[match_text] += 1
#             matches.append((match_text, pattern_counts[match_text]))
            
#     return matches

# def find_categories(text, retweet):
#     patterns = [
#         r'\bbest\b.*?\b(picture|drama|musical|film)\b',
#         r'\bbest (tv|television)\b.*?\b(drama|musical)\b',
#         r'\bcecil.*?\baward\b',
#         r'\bbest performance by\b.*?\b(musical|picture|tv|television|drama)\b'
#     ]

#     matches_dict = {}
    
#     for t in text:
#         t = utils.clean_text(t)
    
#         for pattern in patterns:
#             for match in re.finditer(pattern, t):
#                 match_text = match.group(0)
#                 pattern_counts[match_text] += 1
#                 matches_dict[match_text] = pattern_counts[match_text]

#     for rt in retweet:
#         rt = utils.clean_text(rt)    

#         for pattern in patterns:
#             for match in re.finditer(pattern, rt):
#                 match_text = match.group(0)
#                 pattern_counts[match_text] += 2
#                 matches_dict[match_text] = pattern_counts[match_text]
    
#     categories_counter = utils.merge(matches_dict)
    
#     x = 15

#     # Initialize an empty list to store categories
#     categories = []

#     # Loop through the Counter object
#     for category, count in categories_counter.items():
#         if count > x:
#             categories.append(category)

#     answer = {"categories": categories}

#     with open("categories.json", 'w') as f:
#         # Dump the dictionary to the file
#         json.dump(answer, f)
    
#     return categories



def find_categories(retweet):
    categories_result = []
    categories = defaultdict(int)
    
    nlp = spacy.load('en_core_web_md')
    matcher = Matcher(nlp.vocab)

    stop_words = ['part','dress','golden','globe','thing','show','friend','host','awards']

    patterns = [
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'by'}, {'POS': 'DET', 'OP': '?'}, {'POS': {'IN': ['ADJ', 'NOUN']}, 'OP': '+'}, {'POS': 'ADP', 'OP': '?'}, {'POS': 'DET', 'OP': '?'}, {'POS': 'NOUN', 'OP': '+'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'by'}, {'POS': 'DET'}, {'POS': 'NOUN'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'in'}, {'POS': 'DET', 'OP': '?'}, {'POS': 'ADJ', 'OP': '+'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'in'}, {'POS': 'DET'}, {'POS': 'NOUN'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'in'}, {'POS': 'NOUN'}, {'POS': 'NOUN'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'in'}, {'POS': 'NOUN'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'by'}, {'POS': 'DET'}, {'POS': 'NOUN', 'OP': '+'}],
        [{'LOWER': 'best'}, {'POS': {'IN': ['ADJ', 'NOUN', 'PROPN']}, 'OP': '+'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'POS': 'PRON'}, {'POS': 'PRON'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'POS': 'PRON'}, {'POS': 'PRON'}, {'LOWER': 'or'}, {'POS': 'ADJ'}],
        [{'LOWER': 'best'}, {'POS': {'IN': ['ADJ', 'NOUN', 'PROPN']}, 'OP': '+'}],
        [{'LOWER': 'cecil'}, {'LOWER': 'b.'}, {'LOWER': 'demille'}, {'LOWER': 'award'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'POS': 'NOUN', 'OP': '?'}, {'POS': 'CCONJ', 'OP': '?'}, {'POS': 'ADJ|NOUN', 'OP': '?'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'LOWER': 'by'}, {'POS': 'DET', 'OP': '?'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN'}, {'POS': 'NOUN'}],
        [{'LOWER': 'best'}, {'POS': 'ADJ'}, {'POS': 'NOUN'}],
        [{'LOWER': 'best'}, {'POS': 'ADJ'}, {'POS': 'NOUN'}, {'LOWER': 'in'}, {'POS': 'NOUN', 'OP': '+'}, {'POS': 'NOUN', 'OP': '+'}],
        [{'LOWER': 'best'}, {'POS': 'ADJ'}, {'POS': 'NOUN'}, {'LOWER': 'in'}, {'POS': 'DET', 'OP': '?'}, {'POS': 'NOUN', 'OP': '+'}, {'POS': 'NOUN', 'OP': '+'}]
    ]
    matcher.add('AWARD_CATEGORY', patterns)

    for rt in retweet:
        # Disregard hyphens
        rt = rt.replace('-', ' ')
        rt = rt.split()
        rt = ' '.join(rt)
        # print(rt)
        doc = nlp(rt)
        matches = matcher(doc)
        if matches:
            # Sort matches by length and get the longest one
            longest_match = max(matches, key=lambda match: match[2] - match[1])
            text = doc[longest_match[1]:longest_match[2]].text.lower()
            stop=False
            for s in stop_words:
                if s in text:
                    stop=True
            if not stop:
                categories[text] += 1
    
#     for t in text:
#         # Disregard hyphens
#         t = t.replace('-', ' ')
#         doc = nlp(t)
#         matches = matcher(doc)

#         if matches:
#             # Sort matches by length and get the longest one
#             longest_match = max(matches, key=lambda match: match[2] - match[1])
#             categories.append(doc[longest_match[1]:longest_match[2]].text)
    c = utils.merge(categories)
    categories = [key for key, _ in c.most_common(30)]
    # print("categories:", [(key,value) for key,value in c.most_common(30)])
    # print("Categories: ",categories)
    
    return categories
