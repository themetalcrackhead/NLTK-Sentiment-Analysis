import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


short_pos = open("Dataset/positive.txt", "r").read()
short_neg = open("Dataset/negative.txt", "r").read()

# documents = []
#
# for r in short_pos.split('\n'):
#     documents.append((r.lower(), "pos"))
#
# for r in short_neg.split('\n'):
#     documents.append((r.lower(), "neg"))

save_documents = open("Pickles/documents.pickle","rb")
documents = pickle.load(save_documents)
save_documents.close()

# all_words = []

# short_pos_words = word_tokenize(short_pos)
# short_neg_words = word_tokenize(short_neg)
#
# for w in short_pos_words:
#     all_words.append(w.lower())
#
# for w in short_neg_words:
#     all_words.append(w.lower())
#
# all_words = nltk.FreqDist(all_words)

save_all_words = open("Pickles/all_words.pickle", "rb")
all_words = pickle.load(save_all_words)
save_all_words.close()

# word_features = [w for (w,c) in all_words.most_common(5000)] #list(all_words.keys())[:3000]

save_word_features = open("Pickles/word_features.pickle","rb")
word_features = pickle.load(save_word_features)
save_word_features.close()


# def find_features(document):
#     words = word_tokenize(document)
#     features = {}
#     for w in word_features:
#         features[w] = (w in words)
#
#     return features
#
#
# featuresets = [(find_features(rev), category) for (rev, category) in documents]

save_featuresets = open("Pickles/featuresets.pickle", "rb")
featuresets = pickle.load(save_featuresets)
save_featuresets.close()

random.shuffle(featuresets)

training_set = featuresets[:10000]
testing_set = featuresets[10000:]

#classifier = nltk.NaiveBayesClassifier.train(training_set)

save_classifier = open("Pickles/NB.pickle","rb")
classifier = pickle.load(save_classifier)
save_classifier.close()
print("Original NB Accuracy:", (nltk.classify.accuracy(classifier,testing_set))*100)
classifier.show_most_informative_features(15)

# MNB_classifier = SklearnClassifier(MultinomialNB())

save_classifier = open("Pickles/MNB.pickle","rb")
MNB_classifier = pickle.load(save_classifier)
save_classifier.close()

# MNB_classifier.train(training_set)
print("MNB Accuracy:", (nltk.classify.accuracy(MNB_classifier,testing_set))*100)

# Bernoulli_classifier = SklearnClassifier(BernoulliNB())
# Bernoulli_classifier.train(training_set)

save_classifier = open("Pickles/Bernoulli_classifier.pickle","rb")
Bernoulli_classifier = pickle.load(save_classifier)
save_classifier.close()
print("Bernoulli NB Accuracy:", (nltk.classify.accuracy(Bernoulli_classifier,testing_set))*100)

# LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
# LogisticRegression_classifier.train(training_set)

save_classifier = open("Pickles/LogisticRegression_classifier.pickle","rb")
LogisticRegression_classifier = pickle.load(save_classifier)
save_classifier.close()
print("LogisticRegression Accuracy:", (nltk.classify.accuracy(LogisticRegression_classifier,testing_set))*100)

# SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
# SGDClassifier_classifier.train(training_set)

save_classifier = open("Pickles/SGDClassifier_classifier.pickle","rb")
SGDClassifier_classifier = pickle.load(save_classifier)
save_classifier.close()
print("SGDClassifier Accuracy:", (nltk.classify.accuracy(SGDClassifier_classifier,testing_set))*100)

# SVC_classifier = SklearnClassifier(SVC())
# SVC_classifier.train(training_set)
# print("SVC Accuracy:", (nltk.classify.accuracy(SVC_classifier,testing_set))*100)

# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(training_set)

save_classifier = open("Pickles/LinearSVC_classifier.pickle","rb")
LinearSVC_classifier = pickle.load(save_classifier)
save_classifier.close()
print("LinearSVC Accuracy:", (nltk.classify.accuracy(LinearSVC_classifier,testing_set))*100)

# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training_set)

save_classifier = open("Pickles/NuSVC_classifier.pickle","rb")
NuSVC_classifier = pickle.load(save_classifier)
save_classifier.close()
print("NuSVC Accuracy:", (nltk.classify.accuracy(NuSVC_classifier,testing_set))*100)

voted_classifier = VoteClassifier(classifier,
                                  MNB_classifier,
                                  Bernoulli_classifier,
                                  LogisticRegression_classifier,
                                  SGDClassifier_classifier,
                                  # SVC_classifier,
                                  LinearSVC_classifier,
                                  NuSVC_classifier)

print("Voted Classifier Accuracy:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)

print("Classification:", voted_classifier.classify(testing_set[0][0]),
      "Confidence:", voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:", voted_classifier.classify(testing_set[1][0]),
      "Confidence:", voted_classifier.confidence(testing_set[1][0])*100)
print("Classification:", voted_classifier.classify(testing_set[2][0]),
      "Confidence:", voted_classifier.confidence(testing_set[2][0])*100)
print("Classification:", voted_classifier.classify(testing_set[3][0]),
      "Confidence:", voted_classifier.confidence(testing_set[3][0])*100)
print("Classification:", voted_classifier.classify(testing_set[4][0]),
      "Confidence:", voted_classifier.confidence(testing_set[4][0])*100)
print("Classification:", voted_classifier.classify(testing_set[5][0]),
      "Confidence:", voted_classifier.confidence(testing_set[5][0])*100)