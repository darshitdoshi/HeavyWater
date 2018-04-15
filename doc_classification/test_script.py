#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 14:13:37 2018

@author: darshit
"""

import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

file = pd.read_csv("shuffled-full-set-hashed.csv")

#Select the labels and features from file
label = file.iloc[:,0]
all_strings = file.iloc[:,1]
#Typecast each element in all_strings to string (remove np.nan)
all_strings = all_strings.apply(lambda x : str(x))

#Get a sparse matrix of documents mapped to words
count_vect = CountVectorizer()
X_train_sparse = count_vect.fit_transform(all_strings.tolist())
#X_train_counts.shape

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
        X_train_sparse, label, test_size=0.33, random_state=42)

# =============================================================================
# #Bad accuracy
# #Perform TF-IDF to approriately weight each term 
# #
# #tfidf_transformer = TfidfTransformer()
# #X_train_tfidf = tfidf_transformer.fit_transform(X_train)
# =============================================================================

# =============================================================================
# #Train NB
# clf = MultinomialNB()
# clf.fit(X_train, y_train)
# #Predict NB
# predicted = clf.predict(X_test)
# print(" NB Accuracy on Train set: %s" % np.mean(predicted == y_test))
# 
# =============================================================================

# =============================================================================
# nn_clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
# nn_clf.fit(X_train, y_train)
# predicted = nn_clf.predict(X_test)
# print(" Neural Network Accuracy on Train set: %s" % np.mean(predicted == y_test))
# 
# =============================================================================
#Train SVM
svm_clf = SGDClassifier(loss='log', penalty='l2',alpha=1e-2, n_iter=5, random_state=42)
svm_clf.fit(X_train, y_train)
#Predict SVM
predicted_mat = svm_clf.predict_proba(X_test)
prediction = svm_clf.predict(X_test)
print(" SVM Accuracy on Train set: %s" % np.mean(predicted == y_test))
