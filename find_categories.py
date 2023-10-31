def find_categories(text, retweet):
    categories = []
    
    return categories

# def extract_award_categories(texts):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    patterns = [
        [{'LOWER': 'best'}, {'POS': {'IN': ['NOUN', 'ADJ', 'PROPN']}}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': {'IN': ['NOUN', 'PROPN']}, 'OP': '+'}],
        [{'LOWER': 'best'}, {'POS': 'NOUN', 'OP': '+'}, {'LOWER': 'by'}, {'POS': 'DET', 'OP': '?'}, {'POS': 'NOUN', 'OP': '+'}],
        [{'LOWER': 'best'}, {'POS': 'ADJ', 'OP': '?'}, {'POS': 'NOUN', 'OP': '+'}]
    ]
    matcher.add('AWARD_CATEGORY', patterns)

    categories = []
    for text in texts:
        # Disregard hyphens
        text = text.replace('-', ' ')
        print(text)
#         doc = nlp(text)
#         matches = matcher(doc)
#         if matches:
#             # Sort matches by length and get the longest one
#             longest_match = max(matches, key=lambda match: match[2] - match[1])
#             categories.append(doc[longest_match[1]:longest_match[2]].text)
#     return categories

texts = [
    "best screenplay - motion picture",
    "best director - motion picture",
    "best performance by an actress in a television series - comedy or musical",
    "best foreign language film",
    "best performance by an actor in a supporting role in a motion picture",
    "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television",
    "best motion picture - comedy or musical",
    "best performance by an actress in a motion picture - comedy or musical",
    "best mini-series or motion picture made for television"
]