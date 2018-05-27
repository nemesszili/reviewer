# -*- coding: utf-8 -*- 

import pandas as pd
import numpy as np

import re

from nltk import word_tokenize
from nltk.corpus import stopwords

from imblearn.under_sampling import RandomUnderSampler
from const import SEED

import langid

DATA_PATH = '../amazon-reviews-unlocked-mobile-phones.zip'

EMOTICONS_POS = r"""
    (?:
      [<>]?
      [:;=8]              # eyes
      [\-o\*\']?          # optional nose
      [\)\]dDpP\}]        # mouth
      |
      [\)\]dDpP\}]        # mouth
      [\-o\*\']?          # optional nose
      [:;=8]              # eyes
      [<>]?
      |
      <3                  # heart
    )"""

EMOTICONS_NEG = r"""
    (?:
      [<>]?
      [:;=8]              # eyes
      [\-o\*\']?          # optional nose
      [\(\[/\{@\|\\]      # mouth
      |
      [\(\[/\{@\|\\]      # mouth
      [\-o\*\']?          # optional nose
      [:;=8]              # eyes
      [<>]?
    )"""

EMOTICON_POS_RE = re.compile(EMOTICONS_POS, re.VERBOSE | re.I | re.UNICODE)
EMOTICON_NEG_RE = re.compile(EMOTICONS_NEG, re.VERBOSE | re.I | re.UNICODE)

def _pos_emoticons(text):
    return len(re.findall(EMOTICON_POS_RE, text.decode('utf8')))

def _neg_emoticons(text):
    return len(re.findall(EMOTICON_NEG_RE, text.decode('utf8')))

def _caps(text):
    return len(filter(lambda x: x.isupper(), text.decode('utf8').split()))

def _excl_marks(text):
    return len([i for i, letter in enumerate(text.decode('utf8')) if letter == '!'])

def _tokenize(text):
    res = [w.lower() for w in word_tokenize(text.decode('utf8')) if w.isalnum()]
    return " ".join(filter(lambda x: x not in set(stopwords.words('english')), res))

def _detect(text):
    try:
        return langid.classify(text.decode('utf8'))[0]
    except:
        return 'xx'

##
#  Extract features
##
def preprocess(df, size):
    # Drop rows with empty reviews
    print('Removing empty reviews... '),
    df['Reviews'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Reviews'], inplace=True)
    print('done!')

    df = df.head(size)

    # Drop non-English reviews
    print('Removing non-English reviews... '),
    df.loc[:, 'lang'] = df['Reviews'].apply(lambda x: _detect(x))
    df = df[df['lang'] == 'en']
    print('done!')

    print('Extracting features...')
    
    # Number of caps words
    print('Number of caps words... '),
    df.loc[:, 'caps'] = df['Reviews'].apply(lambda x: _caps(x))
    print('done!')
    
    # Number of positive emoticons
    print('Number of positive emoticons... '),
    df.loc[:, 'posicon'] = df['Reviews'].apply(lambda x: _pos_emoticons(x))
    print('done!')

    # Number of negative emoticons
    print('Number of negative emoticons... '),
    df.loc[:, 'negicon'] = df['Reviews'].apply(lambda x: _neg_emoticons(x))
    print('done!')

    # Number of exclamation marks
    print('Number of exclamation marks... '),
    df.loc[:, 'excl'] = df['Reviews'].apply(lambda x: _excl_marks(x))
    print('done!')

    # Review length
    print('Review length... '),
    df.loc[:, 'length'] = df['Reviews'].apply(lambda x: len(x))
    print('done!')

    # Tokenize
    print('Tokenizing... '),
    df.loc[:, 'proc'] = df['Reviews'].apply(lambda x: _tokenize(x))
    print('done!')

    # Drop rows with empty processed reviews
    print('Removing empty processed reviews... '),
    df['proc'].replace('', np.nan, inplace=True)
    df.dropna(subset=['proc'], inplace=True)
    print('done!')

    # Remove unused columns
    df.drop(df.columns[[0, 1, 2, 4]], inplace=True, axis=1)
    df.drop('lang', inplace=True, axis=1)

    # Replace NaN with 0
    df.fillna(0, inplace=True)

    return df

##
#  Process text for classification
##
def process_text(text):
    print(text)
    d = {'Reviews': [text], 'Review Votes': [0.0]}
    df = pd.DataFrame(data=d)

    # Number of caps words
    df.loc[:, 'caps'] = df['Reviews'].apply(lambda x: _caps(x))
    
    # Number of positive emoticons
    df.loc[:, 'posicon'] = df['Reviews'].apply(lambda x: _pos_emoticons(x))

    # Number of negative emoticons
    df.loc[:, 'negicon'] = df['Reviews'].apply(lambda x: _neg_emoticons(x))

    # Number of exclamation marks
    df.loc[:, 'excl'] = df['Reviews'].apply(lambda x: _excl_marks(x))

    # Review length
    df.loc[:, 'length'] = df['Reviews'].apply(lambda x: len(x))

    # Tokenize
    df.loc[:, 'proc'] = df['Reviews'].apply(lambda x: _tokenize(x))

    return df

##
#  Resample data
## 
def resample(df, x, y):
    x_i = x.index.values.reshape(-1, 1)
    _, _, i = RandomUnderSampler(ratio='all', return_indices=True, random_state=SEED).fit_sample(x_i, y.values.ravel())
    return x.loc[df.index.isin(i)], y.loc[df.index.isin(i)]
