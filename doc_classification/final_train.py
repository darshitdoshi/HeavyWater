#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 22:33:50 2018

@author: darshit
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib

file = pd.read_csv("shuffled-full-set-hashed.csv")

#Select the labels and features from file
label = file.iloc[:,0]
all_strings = file.iloc[:,1]
#Typecast each element in all_strings to string (remove np.nan)
all_strings = all_strings.apply(lambda x : str(x))

#Get a sparse matrix of documents mapped to words
count_vect = CountVectorizer(stop_words=[" "])
X_train_sparse = count_vect.fit_transform(all_strings.tolist())
dict_list = count_vect.get_feature_names()

dl = " ".join(dict_list)
dl = (dl,)
joblib.dump(dl, 'vocab_tuple.pkl')

svm_clf = SGDClassifier(loss='log', penalty='l2',alpha=1e-2, n_iter=5, random_state=42)
svm_clf.fit(X_train_sparse, label)

joblib.dump(svm_clf, 'sgd_model3.pkl')