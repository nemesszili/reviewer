# -*- coding: utf-8 -*- 

import pandas as pd
import numpy as np

import re

from nltk import word_tokenize

import dill
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier

import os.path

from util.process import preprocess
from util.pipeline import TextSelector, StemmedTfidfVectorizer

from pprint import PrettyPrinter as PrettyPrinter
pp = PrettyPrinter(indent=4)

DATA_PATH   = './proc.csv'
ZIP_PATH    = '../amazon-reviews-unlocked-mobile-phones.zip'
PICKLE_PATH = './pipeline.pkl'
SIZE        = 1000
SEED        = 42

num_feat = ['caps', 'posicon', 'negicon', 'excl', 'length', 'Review Votes']
numeric = FunctionTransformer(lambda x: x[num_feat], validate=False)

ppl = Pipeline([
    ('feat', FeatureUnion([
        ('tfidf_feat', Pipeline([
            ('tokens', TextSelector(key='proc')),
            ('tfidf',  StemmedTfidfVectorizer(ngram_range=(1, 2)))
        ])),
        ('numeric', Pipeline([
            ('select', numeric),
            ('std',    StandardScaler())
        ]))
    ])),
    ('logit', OneVsRestClassifier(LogisticRegression()))
])

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

        # Train model
        ppl.fit(X_train, Y_train.values.ravel())

        # Serialize model
        pickle.dump(ppl, open(PICKLE_PATH, 'wb'))
    else:
        # Import data
        df = pd.read_csv(DATA_PATH)

        # Load model
        ppl = pickle.load(open(PICKLE_PATH, 'rb'))

        # Select columns
        x = df.drop(df.columns[[0, 1]], axis=1)
        y = df.iloc[:, [0]]

        # Split into train and test
        X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=SEED)

    pp.pprint(X_test)
    y = ppl.predict(X_test)
    print(classification_report(y, Y_test))
    
if __name__ == '__main__':
    main()