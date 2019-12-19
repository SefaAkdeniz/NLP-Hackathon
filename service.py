# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 14:15:07 2019

@author: sefa
"""
from keras.models import model_from_json
import numpy as np
from TurkishStemmer import TurkishStemmer
import re
import pandas as pd
import nltk
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from nltk.corpus import stopwords
import tensorflow as tf
from keras import backend as k

def load_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    global model
    model = model_from_json(loaded_model_json)
    model.load_weights("model.h5")
    global graph
    graph=tf.get_default_graph()
    
tokenizer = Tokenizer()

df=pd.read_csv("df.csv")
X=list(df.reviewText)
tokenizer.fit_on_texts(X)

#json_file = open('model.json', 'r')
#loaded_model_json = json_file.read()
#json_file.close()
#loaded_model = model_from_json(loaded_model_json)
## load weights into new model
#loaded_model.load_weights("model.h5")
#loaded_model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
print("Loaded model from disk")
int2label = { 0: "Olumsuz", 1: "Olumlu"}



def get_predictions(text):
    k
    load_model()    
    
   
    text = re.sub("\W"," ",text)
    text = re.sub("[0-9]"," ",text)
    text = text.lower()   # buyuk harftan kucuk harfe cevirme
    text = nltk.word_tokenize(text)
    text = [ word for word in text if not word in set(stopwords.words("turkish"))]
    kokbul = TurkishStemmer()
    text = [ kokbul.stem(word) for word in text]
    text = " ".join(text)
   
    sequence = tokenizer.texts_to_sequences([text])
    # pad the sequence
    sequence = pad_sequences(sequence, maxlen=100)
    # get the prediction
  
    with graph.as_default():
        prediction=model.predict(sequence)[0]
        
    
    print(prediction)
    # one-hot encoded vector, revert using np.argmax
    return int2label[np.argmax(prediction)]

from flask import Flask
app = Flask(__name__)





@app.route('/<string:Comment>')
def index(Comment):
    k.clear_session()
    response=get_predictions(Comment)
    k.clear_session()
    return response
    
       
if __name__ == '__main__':
    app.run(debug=True)