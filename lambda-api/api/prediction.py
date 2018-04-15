#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 01:53:28 2018

@author: darshit
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:49:52 2018

@author: darshit
"""
from sklearn.externals import joblib
from flask import Flask
from flask import request
from flask import json
from boto.s3.key import Key
import boto
from sklearn.feature_extraction.text import CountVectorizer
import warnings
import numpy as np

BUCKET_NAME = 'heavywaterml'
MODEL_FILE_NAME = 'sgd_model3.pkl'
VOCAB_FILE_NAME = 'vocab_tuple.pkl'
CV_NAME = 'count_vect'
MODEL_LOCAL_PATH = MODEL_FILE_NAME
VOCAB_LOCAL_PATH = VOCAB_FILE_NAME
CV_LOCAL_PATH = CV_NAME
AWS_S3_HOST = 's3.us-east-1.amazonaws.com'

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    body_dict = request.get_json(silent=True)
    data = body_dict['data']

    prediction = predict(data)

    result = {'prediction': prediction[0], 'confidence': prediction[1]}
    return json.dumps(result)


@app.route('/model',methods=['GET'])
def save_model_locally():
    load_model()
    resp = {'model': 'loaded'}
    return json.dumps(resp)


@app.route('/vocab',methods=['GET'])
def save_vocab_locally():
    load_vocab()
    resp = {'vocab': 'loaded'}
    return json.dumps(resp)


#   Load the trained model from S3
def load_model():
    conn = boto.connect_s3(host=AWS_S3_HOST)
    bucket = conn.get_bucket(BUCKET_NAME)
    key_obj = Key(bucket)
    key_obj.key = MODEL_FILE_NAME
    contents = key_obj.get_contents_to_filename(MODEL_LOCAL_PATH)
    model = ""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        model = joblib.load(MODEL_FILE_NAME)
    return model


#   Load vocabulary from S3 
def load_vocab():
    conn = boto.connect_s3(host=AWS_S3_HOST)
    bucket = conn.get_bucket(BUCKET_NAME)
    key_obj = Key(bucket)
    key_obj.key = VOCAB_FILE_NAME
    contents = key_obj.get_contents_to_filename(VOCAB_LOCAL_PATH)
    vocab = ""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        vocab = joblib.load(VOCAB_FILE_NAME)
    return vocab


#   Get CountVectorizer, to transform
#   input words to matrix
def get_Count_Vect():
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            vocab = joblib.load(VOCAB_FILE_NAME)
    except:
        vocab = load_vocab()
        
    cv = CountVectorizer()
    cv.fit(vocab)
    return cv


#   Prediction, 
#   data : Array of String
#   result : Predicted document, Confidence
def predict(data):
    cv = get_Count_Vect()
    
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            model = joblib.load(MODEL_FILE_NAME)
    except:
        model = load_model()
    data = cv.transform(data)

    prob_mat = model.predict_proba(data)
    confidence = np.amax(prob_mat, axis=1)
    prediction =  [model.predict(data).tolist(), confidence.tolist()]
    return prediction


if __name__ == '__main__':
    # listen on all IPs
    app.run(host='0.0.0.0')