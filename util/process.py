# -*- coding: utf-8 -*- 
# Based on: https://www.nltk.org/_modules/nltk/tokenize/casual.html

import pandas as pd
import numpy as np

import re

from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
st = SnowballStemmer("english")

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

# REGEXPS = (
#     # ASCII Emoticons
#     EMOTICONS_POS,
#     EMOTICONS_NEG,
#     # Remaining word types:
#     r"""
#     (?:[^\W\d_](?:[^\W\d_]|['\-_])+[^\W\d_]) # Words with apostrophes or dashes.
#     |
#     (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
#     |
#     (?:[\w_]+)                     # Words without apostrophes or dashes.
#     |
#     (?:\S)                         # Everything else that isn't whitespace.
#     """
# )

# WORD_RE = re.compile(r"""(%s)""" % "|".join(REGEXPS), re.VERBOSE | re.I | re.UNICODE)

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
    return [st.stem(w.lower()) for w in word_tokenize(text.decode('utf8')) if w.isalnum()]

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
    df.dropna(subset=['Reviews'], inplace=True)
    print('done!')

    df = df.head(size)

    # Drop non-English reviews
    print('Removing non-English reviews... '),
    df.loc[:, 'lang'] = df['Reviews'].apply(lambda x: _detect(x))
    df = df[df['lang'] == 'en']
    print('done!')

    # Remove unused columns
    df.drop(df.columns[[0, 1, 2]], inplace=True, axis=1)
    df.drop('lang', inplace=True, axis=1)

    # Replace NaN with 0
    df.fillna(0, inplace=True)

    # # Tokenize
    # print('Tokenizing... '),
    # df['proc'] = df['Reviews'].apply(lambda x: _tokenize(x))
    # print('done!')

    print('Extracting features...')
    
    # Number of caps words
    print('Number of caps words... '),
    df.loc[:, 'caps'] = df['Reviews'].apply(lambda x: _caps(x))
    print('done!')
    
    # Number of positive emoticons
    print('Number of positive emoticons... '),
    df.loc[:, 'posticon'] = df['Reviews'].apply(lambda x: _pos_emoticons(x))
    print('done!')

    # Number of negative emoticons
    print('Number of negative emoticons... '),
    df.loc[:, 'negticon'] = df['Reviews'].apply(lambda x: _neg_emoticons(x))
    print('done!')

    # Number of exclamation marks
    print('Number of exclamation marks... '),
    df.loc[:, 'excl'] = df['Reviews'].apply(lambda x: _excl_marks(x))
    print('done!')

    # Review length
    print('Review length... '),
    df.loc[:, 'length'] = df['Reviews'].apply(lambda x: len(x))
    print('done!')

    return df