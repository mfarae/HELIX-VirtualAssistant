#from flask import Flask, render_template, request, jsonify
#
#import requests
#
#app = Flask(__name__)
#
#rasa_server_url = 'http://localhost:5005/webhooks/rest/webhook'
#
#@app.route('/')
#
#def index():
#    return render_template('index.html')
#
#@app.route('/chatbot', methods=['POST'])
#
#def chatbot():
#    data = request.json
#    message = data['message']
#    response = requests.post(rasa_server_url, json={'message': message}).json()
#    return jsonify(response)
#
##if __name__ == '__main__':
##    app.run()
#
#
#from flask import Flask, render_template, request, jsonify
#import requests
#import json
#import numpy as np
#import librosa
#import tensorflow as tf
#from keras.models import load_model
#
#app = Flask(__name__)
#
#rasa_server_url = 'http://localhost:5005/webhooks/rest/webhook'
#
#model = load_model('voice classification/checkpoints/voice_recognition_best_model_17.hdf5')
#
#@app.route('/')
#def index():
#    return render_template('index.html')
#
#@app.route('/chatbot', methods=['POST'])
#def chatbot():
#    data = request.json
#    message = data['message']
#    response = requests.post(rasa_server_url, json={'message': message}).json()
#    return jsonify(response)
#
#@app.route('/voice', methods=['POST'])
#def voice():
#    print("testing")
#    # Get audio data from request
#    audio_file = request.files['audio']
#    audio_data, sr = librosa.load(audio_file)
#
#    # Preprocess audio data
#    mfccs = librosa.feature.mfcc(audio_data, sr=sr, n_mfcc=40)
#    mfccs = np.mean(mfccs.T, axis=0)
#    test_data = np.expand_dims(mfccs, axis=0)
#
#    # Make prediction
#    prediction = model.predict(test_data)
#    print(prediction)
#
#    # Return result
#    return jsonify({'prediction': prediction.tolist()})
#
#if __name__ == '__main__':
#    app.run()

from flask import Flask, render_template, request, jsonify
from keras.models import load_model
import requests
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech (words per minute)
engine.setProperty("volume", 0.8) 
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

app = Flask(__name__)

rasa_server_url = 'http://localhost:5005/webhooks/rest/webhook'

model = load_model('voice classification/checkpoints/voice_recognition_best_model_17.hdf5')

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])

def chatbot():
    data = request.json
    message = data['message']
    response = requests.post(rasa_server_url, json={'message': message}).json()
    print(response)
    engine.say(response)
    engine.runAndWait()
    return jsonify(response)

if __name__ == '__main__':
    app.run()