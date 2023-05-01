from flask import Flask, render_template, request, jsonify

import requests

app = Flask(__name__)

rasa_server_url = 'http://localhost:5005/webhooks/rest/webhook'

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])

def chatbot():
    data = request.json
    message = data['message']
    response = requests.post(rasa_server_url, json={'message': message}).json()
    return jsonify(response)

if __name__ == '__main__':
    app.run()



