# HeavyWater Machine Learning Problem

## Overview
### Document Classifier

- The machine learning model has been developed using scikit-learn and python.
- The Document Classifier has been trained using SGDClassifier with log loss.
- CountVectorizer is used to convert array of document strings to a sparse matrix of word counts. This is also used to convert input document string into appropriate representation for making predictions.

- Since the model along with the Lambda function is larger than the allowed deployable size, the model cannot be included in the deployment package.
- The trained model and vocabulary of words has been pickled and stored on AWS S3.


### AWS Lambda Function (Prediction Microservice)

- AWS Lambda is employed for making predictions with good scalability.
- Flask framework employed for RESTful API for prediction requests and response using AWS API Gateway.
- Prediction performed by loading the model from AWS S3 and extracting the document string from the JSON body of POST request.
- The JSON response includes 2 fields : 'prediction', 'confidence'

- The prediction webservice can be employed to make prediction on multiple documents in a single API call by passing an array of document strings in the JSON request field 'data' : 
```
Request : {"data": ["Document1", "Document2", "Document3"]}
Response : {"prediction": ["pred1", "pred2", "pred3"], "confidence": ["conf1", "conf2", "conf3"]}
```
This is much faster than making separate API calls for each document.
**Note:** The functionality to add multiple documents in a single prediction API call has not been implemented on the front end.

- The endpoint URL for making the prediction microservice : 
```
https://x41c47q7c7.execute-api.us-east-1.amazonaws.com/dev
```

### Web Service

- The website is hosted on AWS Beanstalk configured with Apache Tomcat.
- The Servlets are written in Java, compiled and packaged into war using Maven.

- The servlet displays the home page which has field for entering document and submitting.
- Upon submitting, a GET request with URL encoded "words" parameter is fired using '/prediction' as servlet path
- Upon receiving such a request, the same servlet makes a corresponding POST request with a JSON body to the AWS Lambda service.
- The prediction and confidence are displayed on the Result page. 
- URL for the Web Service :
```
http://default-environment.tyt99nzejm.us-east-1.elasticbeanstalk.com/
```

## Running the service

- Lambda suffers from coldstart as it deallocates large objects cached locally such as the model after some time of inactivity.
- Upon receiving an API call, the Lambda function can import the model and the vocabulary from S3 bucket if not found locally, but this takes a few seconds and the connection can timeout before predictions are made.
- It is best to load the model and vocabulary explicitly before making prediction API calls
- Loading the model :
GET (https://x41c47q7c7.execute-api.us-east-1.amazonaws.com/dev/model)

- Loading the vocabulary :
GET (https://x41c47q7c7.execute-api.us-east-1.amazonaws.com/dev/model)
