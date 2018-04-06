'''
Generate new features based on existing list of features
'''

from sklearn.preprocessing import LabelEncoder
from pomegranate import *
import numpy as np

def prepare(f):
    words = []
    with open(f) as fr:
        words = [word for line in fr for word in line.split(' ')]

    vocabulary = set(words) # get all the distinct words specifying the features
    le = LabelEncoder()
    le.fit(list(vocabulary))

    vocab_seq = le.transform(words) # transform words to corresponding numeric category. eg. 'hello' -> 1

    return vocab_seq, vocabulary

vocab_seq, vocabulary = prepare('features.txt')
features = np.fromiter(vocab_seq, np.int64)
features = np.atleast_2d(features).T

model = HiddenMarkovModel.from_samples(MultivariateGaussianDistribution, n_components=100, X=features, max_iterations=100, verbose=True, n_jobs=4)

print(model)