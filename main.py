# -*- coding: utf-8 -*- 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import re
import csv

from nltk import word_tokenize

import dill as pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.metrics import classification_report, confusion_matrix

import os.path

from util.process import preprocess, process_text, resample
from util.pipeline import TextSelector, StemmedTfidfVectorizer, SentiVectorizer
from util.visualize import plot_classification_report
from util.const import DATA_PATH, ZIP_PATH, PICKLE_PATH, SIZE, SEED

from pprint import PrettyPrinter as PrettyPrinter
pp = PrettyPrinter(indent=4)

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.main_window_class import MainWindow

num_feat = ['caps', 'posicon', 'negicon', 'excl', 'length', 'Review Votes']
numeric = FunctionTransformer(lambda x: x[num_feat], validate=False)

ppl = Pipeline([
    ('feat', FeatureUnion([
        ('tfidf_feat', Pipeline([
            ('tokens', TextSelector(key='proc')),
            ('tfidf',  StemmedTfidfVectorizer(ngram_range=(1, 2)))
        ])),
        ('senti_feat', Pipeline([
            ('tokens', TextSelector(key='proc')),
            ('senti',  SentiVectorizer(ngram_range=(1, 2)))
        ])),
        ('numeric', Pipeline([
            ('select', numeric),
            ('std',    StandardScaler())
        ]))
    ])),
    ('cls', RandomForestClassifier())
])

def main():
    global ppl

    if not os.path.isfile(PICKLE_PATH):
        if not os.path.isfile(DATA_PATH):
            # Process data
            print("Processing")
            df = pd.read_csv(ZIP_PATH, compression='zip')
            df = preprocess(df, SIZE)
            df.to_csv('proc.csv', encoding='utf-8', index=False, quoting=csv.QUOTE_NONNUMERIC)
            df = pd.read_csv(DATA_PATH)
        else:
            # Import data
            df = pd.read_csv(DATA_PATH)

        # Select columns
        x = df.drop(df.columns[[0]], axis=1)
        y = df.iloc[:, [0]]

        x, y = resample(df, x, y)

        # Split into train and test
        X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=SEED)

        # Train model
        ppl.fit(X_train, Y_train.values.ravel())

        # Serialize model
        pickle.dump(ppl, open(PICKLE_PATH, 'wb'))
    else:
        # Import data
        df = pd.read_csv(DATA_PATH)

        # Select columns
        x = df.drop(df.columns[[0]], axis=1)
        y = df.iloc[:, [0]]

        x, y = resample(df, x, y)

         # Split into train and test
        X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=SEED)

        # Load model
        ppl = pickle.load(open(PICKLE_PATH, 'rb'))

    y = ppl.predict(X_test)
    print(classification_report(Y_test, y))
    print(confusion_matrix(Y_test, y))

    plot_classification_report(classification_report(Y_test, y))
    plt.savefig('test_plot_classif_report.png', dpi=200, format='png', bbox_inches='tight')
    plt.close()

    print(ppl.predict(process_text("Excellent!")))
    print(ppl.predict(process_text("Pretty bad :( I WANT MY MONEY BACK!!!")))
    print(ppl.predict(process_text("It's battery life is great. It's very responsive to touch. The only issue is that sometimes the screen goes black and you have to press the top button several times to get the screen to re-illuminate.")))

if __name__ == '__main__':
    main()
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(ppl)
    form.show()
    app.exec_()