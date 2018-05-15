import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from pprint import PrettyPrinter as PrettyPrinter
pp = PrettyPrinter(indent=4)

DATA_PATH = '../amazon-reviews-unlocked-mobile-phones.zip'

ppl = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(2, 2))),
    ('logr', LogisticRegression()), 
])

def importData():
    df = pd.read_csv(DATA_PATH, compression='zip', usecols=[3, 4, 5])
    
    x = df.iloc[:, [1, 2]]
    y = df.iloc[:, [0]]

    return train_test_split(x, y, test_size=0.2)

def main():
    # Import data
    X_train, X_test, Y_train, Y_test = importData()

    pp.pprint(X_train)
    pp.pprint(Y_train)

if __name__ == '__main__':
    main()