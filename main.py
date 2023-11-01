import argparse
import sys
import json

import clean_file
import find_hosts
import find_categories
import find_nominees
import find_presenters
import find_winners
import find_pwn


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

    clean_file.clean_file(query)

    find_hosts.add_host_tweets(text, retweet, answers_file)

    answers = {"award_data": {}}
    # answers = {}

    c = find_categories.find_categories(text+retweet)
    # c += find_categories.find_categories(retweet)

    if not categories:
        categories = c

    c = categories

    for c in categories:
        # print(c)
        # print(c.split()[1])
        
        # n = find_nominees.nominees(c, text, retweet)
        # all_nominees.append(n)

        # p = find_presenters.presenters(c, text, retweet)

        # # winner must be in nominees
        # # string edit distance approach
        # # co occurence
        # w = find_winners.winners(c, text, retweet)

        # a = {"nominees": n, "presenters": p, "winner": w}

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
