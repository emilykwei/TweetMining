import json
import re
import string

# Data pre-processing
from ftfy import fix_text
from unidecode import unidecode
from langdetect import detect

keywords = ["goes to", "award", "best", "receive", "honor", "grant", "present", "nomin", "host", "giv"]

red_carpet_terms = ["dress", "outfit", "red", "carpet", "fit"]

def filter(tweet):
    pattern = "|".join(map(re.escape, keywords))
    regex = re.compile(pattern)
    result = regex.search(tweet)
    if result:
        return tweet
    
def get_redcarpet(tweet):
    pattern = "|".join(map(re.escape, red_carpet_terms))
    regex = re.compile(pattern)
    result = regex.search(tweet)
    if result:
        return tweet

# Removes URL and double spacing
# If entire text is URL, then returns ""
def remove_url(text):
    result = re.sub(
        r'\s*http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\s*', ' ', text)
    result = re.sub(r'\s+', ' ', result).strip()
    return result

# Determines if a tweet is a retweet
def is_retweet(tweet):
    # Case 1: Simple retweet
    simple_rt_pattern = re.compile(r'^RT @')
    if simple_rt_pattern.match(tweet):
        return True

    # Case 2: Simple quote tweet
    simple_qt_pattern = re.compile(r'.+ RT @')
    if simple_qt_pattern.search(tweet):
        return True

    # Case 3: Retweet/quote tweet of existing retweets/quote tweets
    nested_rt_qt_pattern = re.compile(r'^RT @[\w]+: RT @')
    if nested_rt_qt_pattern.match(tweet):
        return True

    # Case 4: Other QT formats
    other_qt_pattern = re.compile(r'.+ “[^”]*@[\w]+[^”]*”')
    if other_qt_pattern.search(tweet):
        return True

    return False

# Returns the text portion of a retweet
def parse_retweet(text):
    # Keep removing leading retweets until there are no more
    while re.match(r'^RT @[^\s:]+:', text):
        text = re.sub(r'^RT @[^\s:]+:', '', text).strip()

    # Remove any embedded retweets
    text = re.sub(r' RT @[^\s:]+:', '', text)

    return text.strip()

# Remove hastag
def remove_hashtag(text):
    result = re.sub(r'#\w+', '', text)
    result = re.sub(r'\s+', ' ', result).strip()
    return result

def parse_hashtag_at(text):
    try:
        text = re.sub(r'[@#]', ' ', text)

        text = text.replace('_', ' ')

        # Camel Case
        text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
        text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)

        return text

    except:
        pass

# Remove all non-English
def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

def is_quote(text):
    try:
        # Look for quotes with more than 4 words inside
        pattern = re.compile(r'"([\w\W\s\S]+?\s+){4,}[\w\W\s\S]+?"')
        return bool(pattern.search(text))
    except:
        return False

def parse_quote(text):
    pattern = re.compile(r'"([\w\W\s\S]+?)"')
    match = pattern.search(text)

    if match:
        return match.group(1)
    else:
        return text

def is_quote_or_retweet(text):
    return is_quote(text) or is_retweet(text)

def remove_punctuation(text):
    # Make a translator that maps each punctuation character to a space
    translator = str.maketrans(
        string.punctuation, ' ' * len(string.punctuation))

    # Use this translator to replace all punctuation in the text with spaces
    return text.translate(translator)

def clean_file(filename):
    file = open(filename)
    data = json.load(file)
    text = []
    retweet = []
    redcarpet = []

    # Fixes the strings and remove duplicates
    strings = set([fix_text(unidecode(d["text"])) for d in data])

    for s in strings:
        # contains keyword?
        result = filter(s)
        if result is not None:
            # Remove URL
            no_url = remove_url(s)
            if len(no_url) == 0:
                continue

            # Filter retweets and quotes
            if is_retweet(no_url):
                # Parse retweet
                parsed = parse_retweet(no_url)
                is_text = False

            elif is_quote(no_url):
                # Parse quote
                parsed = parse_quote(no_url)
                is_text = False

            else:
                parsed = no_url
                is_text = True

            # Change all # and @ to text
            hashtag = parse_hashtag_at(parsed)

            # Remove punctuation
            # punctuation = remove_punctuation(hashtag)
            punctuation = hashtag  # not removing for now

            # Remove extra whitespaces
            # Keep tabs/newline characters
            space = re.sub(' +', ' ', " ".join(punctuation.split()))

            # Remove all short tweets that cannot hold relevant information
            if len(space.split()) < 5:
                continue

            # Remove non-English tweets
            if not is_english(space):
                continue

            if is_text:
                text.append(space)

            else:
                retweet.append(space)

            if get_redcarpet(s) is not None:
                redcarpet.append(space)

    text_file = "text.json"
    retweet_file = "retweet.json"
    redcarpet_file = "redcarpet.json"

    with open(text_file, 'w') as f:
        # Dump the list to the file
        json.dump(text, f)

    with open(retweet_file, 'w') as f:
        # Dump the list to the file
        json.dump(retweet, f)

    with open(redcarpet_file, 'w') as f:
        # Dump the list to the file
        json.dump(redcarpet, f)
