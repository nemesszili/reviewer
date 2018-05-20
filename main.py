# -*- coding: utf-8 -*- 
# Based on: https://www.nltk.org/_modules/nltk/tokenize/casual.html

import pandas as pd
import numpy as np

import re

from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

import os.path

from util.process import preprocess

from pprint import PrettyPrinter as PrettyPrinter
pp = PrettyPrinter(indent=4)

DATA_PATH   = './proc.csv'
ZIP_PATH    = '../amazon-reviews-unlocked-mobile-phones.zip'
PICKLE_PATH = './pipeline.pkl'
SIZE        = 1000
SEED        = 42

# ppl = Pipeline([
#     ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
#     ('logit', LogisticRegression())
# ])

ppl = LogisticRegression()

def main():
    global ppl

    if not os.path.isfile(PICKLE_PATH):
        if not os.path.isfile(DATA_PATH):
            # Process data
            df = pd.read_csv(ZIP_PATH, compression='zip')
            df = preprocess(df, SIZE)
            df.to_csv('proc.csv', encoding='utf-8', index=False)
        else:
            # Import data
            df = pd.read_csv(DATA_PATH)

        # Select columns
        x = df.drop(df.columns[[0, 1]], axis=1)
        y = df.iloc[:, [0]]

        # Split into train and test
        X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=SEED)

        pp.pprint(X_train)
        pp.pprint(Y_train)

        # Train model
        ppl.fit(X_train, Y_train.values.ravel())

        # Serialize model
        joblib.dump(ppl, PICKLE_PATH)
    else:
        # Load model
        ppl = joblib.load(PICKLE_PATH)

    

if __name__ == '__main__':
    main()