# HeavyWater Machine Learning Problem

### Document Classifier

- The machine learning model has been developed using sklearn and python.
- The Document Classifier has been trained using SGDClassifier with log loss.
- CountVectorizer is used to convert array of document strings to a sparse matrix of word counts. This is also used to convert input document string into appropriate representation for making predictions.

- The trained model and vocabulary of words has been pickled and stored on AWS S3.


### AWS Lambda Function (Prediction Webservice)

- AWS Lambda is employed for making predictions with good scalability.
- RESTful API for prediction requests and response.
- Prediction performed loading the model from S3 and extracting the document string from the request.
- The JSON response includes 2 fields : 'prediction', 'confidence'

- The prediction webservice can be employed to make prediction on multiple documents in a single API call by passing an array of document strings in the JSON request field 'data' : 
```
{"data": ["Document1", "Document2", "Document3"]}
```
This is much faster than making separate API calls for each document.
**Note:** The functionality to add multiple documents in a single prediction API call has not been implemented on the front end.


### Web Service

- The website is hosted on AWS Beanstalk. 
- The web page takes a string of document words and fires a POST request to Lambda service upon submission.
- The results are 
