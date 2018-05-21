# -*- coding: utf-8 -*- 
# Based on: 
# - https://github.com/scikit-learn/scikit-learn/blob/a24c8b46/sklearn/feature_extraction/text.py#L1125
# - https://www.kaggle.com/metadist/work-like-a-pro-with-pipelines-and-feature-unions
# - https://www.kaggle.com/baghern/a-deep-dive-into-sklearn-pipelines

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd

import Stemmer
st = Stemmer.Stemmer('en')

from textblob import TextBlob

class TextSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]

class NumberSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]

class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: st.stemWords(analyzer(doc))

class SentiVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, ngram_range=(1, 1), stop_words=None):
        self.stop_words = stop_words
        self.ngram_range = ngram_range

    def _word_ngrams(self, tokens):
        """Turn tokens into a sequence of n-grams after stop words filtering"""
        tokens = tokens.split()
        # handle stop words
        if self.stop_words is not None:
            tokens = [w for w in tokens if w not in self.stop_words]

        # handle token n-grams
        min_n, max_n = self.ngram_range
        if max_n != 1:
            original_tokens = tokens
            if min_n == 1:
                # no need to do any slicing for unigrams
                # just iterate through the original tokens
                tokens = list(original_tokens)
                min_n += 1
            else:
                tokens = []

            n_original_tokens = len(original_tokens)

            # bind method outside of loop to reduce overhead
            tokens_append = tokens.append
            space_join = " ".join

            for n in xrange(min_n,
                            min(max_n + 1, n_original_tokens + 1)):
                for i in xrange(n_original_tokens - n + 1):
                    tokens_append(space_join(original_tokens[i: i + n]))

        return tokens

    def _sentiment(self, text):
        text = map(lambda x: x.decode('utf8'), text)
        return TextBlob(' '.join(text)).sentiment.polarity

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self._word_ngrams).apply(self._sentiment).apply(pd.Series).fillna(0)