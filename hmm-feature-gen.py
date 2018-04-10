"""
Generate new features based on existing list of features
"""

from __future__ import print_function

import random
from datetime import datetime
import argparse
import numpy as np

from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder
from hmmlearn import hmm


def build_model(num_states=8):
    """
    Build hidden markov model
    :param num_states: number of states
    :return: a Multinomial hidden markov model
    """
    model = hmm.MultinomialHMM(n_components=num_states)
    return model


def gen_features(model, le, num_features):
    """
    generate new feature from trained hidden markov model
    :param model: trained HMM model
    :param le:
    :param num_features: number of features to generate
    :return: None
    """

    random.seed(datetime.now().microsecond)

    for num in range(num_features):
        random_len = random.randint(10, 16) # generate features containing 10 - 15 words
        symbols, _states = model.sample(random_len, random_state=datetime.now().microsecond+random_len)

        output = le.inverse_transform(np.squeeze(symbols))
        print("feature {}:".format(num), end=" ")
        for word in output:
            print(word, end=" ")
        print()


def main():
    args = argparse.ArgumentParser(description="generate new software features based on existing ones")
    args.add_argument("-input", required=True, help="features input file")
    args.add_argument("--num-features", type=int, default=10, help="number of features to generate")
    # args.add_argument("--num-words", type=int, default=15, help="number of words that represents features")

    args = args.parse_args()
    with open(args.input) as f:
        lines = [line.split() for line in f]
    lengths = [len(line) for line in lines]
    words = [word.lower() for line in lines for word in line]

    alphabet = set(words)  # get set of distinct words from requirements
    le = LabelEncoder()
    le.fit(list(alphabet))

    words2encoding = le.transform(words)
    features = np.fromiter(words2encoding, np.int64)
    features = np.atleast_2d(features).T

    model = build_model()
    model.fit(features, lengths)

    gen_features(model, le, args.num_features)
    # save model to file
    joblib.dump(model, 'model.pkl')


main()

