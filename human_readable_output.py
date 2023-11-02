import json
import spacy
import utils
from collections import defaultdict 


def human_readable_output(data):
    
    print("hosts: ",data["hosts"])
    for key in data["award_data"].keys():
        print("Award:",key)

        print("Presenters: ",data["award_data"][key]["presenters"])
        print("Nominees: ",data["award_data"][key]["nominees"])
        print("Winner: ",data["award_data"][key]["winner"])

    with open("redcarpet.json", 'r') as f:
        carpet = json.load(f)
        for key, value in carpet.items():
            print(key,": ",value)
