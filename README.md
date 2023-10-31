# TweetMining
CS 337: Tweet Mining and the Golden Globes
Partners: Qinyan Li, Derek Yu, Emily Zhang

Before you run the code, you should install the packages necessary by going to the root directory of this repository and running:

``pip install -r requirements.txt``

Then you should run 

``python main.py "{filename}.json"``

or 

``python main.py "{filename}.json" --categories {category1} {category2}``

Note that the filen must be in json format and must be in the same directory. There can be an arbitrary number of category inputs.

The answer will be in ``{filename}answers.json``.

The categories found by the program will be in ``categories.json``.
