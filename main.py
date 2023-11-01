import argparse
import sys
import json

import clean_file
import find_hosts
import find_categories
import find_pwn
import find_redcarpet

def main(query, categories=None):
    query = query.strip()

    # Generate the new file name based on the input query
    if query.endswith('.json'):
        answers_file = query[:-5] + 'answers.json'

    else:
        print("Error: The query must be a JSON file name ending with '.json'.")
        sys.exit(1)

    with open("text.json", "r") as file:
        text = json.load(file)

    with open("retweet.json", "r") as file:
        retweet = json.load(file)

    with open("redcarpet.json", "r") as file:
        redcarpet = json.load(file)

    clean_file.clean_file(query)

    find_redcarpet.find_redcarpet(redcarpet)

    find_hosts.add_host_tweets(text, retweet, answers_file)

    answers = {"award_data": {}}

    c = find_categories.find_categories(text, retweet)

    if categories is None:
        categories = c

    for c in categories:
        p,w,n = find_pwn.find_pwn(c, text, retweet)
        answers["award_data"][c] = {"nominees": n, "presenters": p, "winner": w[0] if w else []}

    with open(answers_file, 'r') as f:
        data = json.load(f)

    # Update the content with the new data
    data.update(answers)

    with open(answers_file, 'w') as f:
        # Dump the dictionary to the file
        json.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tweet Mining")
    parser.add_argument("query", type=str, help="JSON File Name: ")
    parser.add_argument("--categories", nargs='*', type=str,
                        help="Optional list of award categories: ")
    args = parser.parse_args()
    main(args.query, args.categories)
