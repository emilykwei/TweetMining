# TweetMining

CS 337: Tweet Mining and the Golden Globes
Partners: Qinyan Li, Derek Yu, Emily Zhang

Before you run the code, you should install the packages necessary by going to the root directory of this repository and running:

`pip install -r requirements.txt`

Then you should run

`python main.py "{filename}.json"`

or

`python main.py "{filename}.json" --categories {category1} {category2}`

Note that the filen must be in json format and must be in the same directory. There can be an arbitrary number of category inputs.

The answer will be in `{filename}answers.json`.

The categories found by the program will be in `categories.json`.

The informatin regarding the red carpet will be in `redcarpet.json`.

Approach

Cleaning
Given the amount of tweet data that we were given and the nature that most tweets didn’t contain much information that we are interested in, we decided to cut off most of them based on keywords as soon as we extracted all the tweets and retweets, which significantly decreased the running time. We put weights on tweets that are retweeted because we think that they are more likely to contain ‘correct’ information.

Spacy
Spacy is a powerful package that helped us tag words and chunk phrases together, although sometimes it was inaccurate and we had to put extra conditions to avoid missing out important pieces of information (for example, it does not always recognize a person as a “PERSON”, so we use the built-in istitle() function to check if the first letter is capitalized, which further affected the data cleaning since we cannot just lower() everything).

Merging
One of our main approaches is to count the number of appearances of certain entities. However, people mistype and abbreviate in their tweets, so comes the merge function in utils.py. It checks for similarities between two entities and merges them if they are above 80% similar to each other.

Hosts
If people tweet about hosts of Golden Globes, the tweet has to contain “host”, no matter if it is a noun or verb. Therefore we limit the search to all (cleaned) tweets containing “host”, and count all appearances of candidate entities that are labeled as “PERSON” by Spacy. The correct answers outbeats the other candidates by a lot.

Award/Category
By our inspection, all of the awards besides one start with the word ‘best’. Therefore we implemented several rules to locate them in the tweet. For example, one rule is “best” followed by an adjective followed by a noun (best original song). Another rule is “best” NOUN ADP(preposition) NOUN NOUN (best actor in motion picture). However, there could still be distractions like “best friend”, “best dress” and “best thing”. Therefore we have to put them in stop words.

Presenter & Nominee
We have tried a lot of approaches to presenters, nominees and winners. In order to balance the accuracy versus time efficiency, we decided to use a Spacy model to help us identify noun chunks in texts containing specific keywords (e.g. ‘win’). Then we locate the correct chunk by index. We also put restrictions on the token/phrase when it has to be a person’s name, for example, presenters in any award, winner and nominees for awards for actors and actresses. Finally, we use stop words to filter out irrelevant information. By recording and counting the number of possible answers, we select the top 1 for winner, 2 for presenter and 4 for nominee.

Winner
In order to find the winners of a category, we decided to use regex pattern matching to look for simple phrases that contained some key words or phrases such as “wins, won, goes to, etc.” Upon finding matches for this, we used a similarity score using what we parsed to be closest to the award in the tweet and the category we are looking for. Then we used the spacy library to try and find people names for awards that would go to a person, and noun chunks for non people. After finding these and storing them in a dictionary, we went with the most frequent answer as our winner.
