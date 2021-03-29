from flask import Flask, render_template, request
import os
import random
import json
import torch
import requests
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from nltk.corpus import stopwords
import pandas as pd
en_stops = set(stopwords.words('english'))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


cuisines_data = []
stepword_data = []
city_name = []
cuisine_name = []

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

with open('cuisines.json') as data_file:    
    data = json.load(data_file)

for restaurant in data['cuisines']:
    cuisines_data.append(restaurant['cuisine']['cuisine_name'].lower())

city_all_data = pd.read_csv('list_of_cities_and_towns_in_india.csv')
city = list(city_all_data['Name of City'].str.lower().dropna())



FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

app = Flask(__name__)
app.static_folder = 'static'

def city_id(city_for_id):

    print("city id here city_for_id: ", city_for_id)
    url = "https://developers.zomato.com/api/v2.1/cities?q="+city_for_id+"&city_ids=12"
    payload={}
    headers = {
    'user-key': 'a60df80ddb6a197f5e37a95238aa3432',
    'Accept': 'application/json',
    'Cookie': 'fbcity=11; zl=en; fbtrack=04af5e1c51da190e6a97abfded40398a; AWSALBTG=aH7qBjGXIVmWZnTTw+ZRo8JAre0+NA1gz8EhnLSouxgj19nYPQMYyKpy1PlA88AG/WYflubsdTNQWtqZaIHzu0kIv4ck84U/ZiyqxHRqo1/GrtxKwarOW8OeVk7iMcdq/OspSQoUhr40vEh/VZf7L1CDbfcahgW+4qpcGl2ljbfPPL+18Gg=; AWSALBTGCORS=aH7qBjGXIVmWZnTTw+ZRo8JAre0+NA1gz8EhnLSouxgj19nYPQMYyKpy1PlA88AG/WYflubsdTNQWtqZaIHzu0kIv4ck84U/ZiyqxHRqo1/GrtxKwarOW8OeVk7iMcdq/OspSQoUhr40vEh/VZf7L1CDbfcahgW+4qpcGl2ljbfPPL+18Gg=; csrf=456f3dd286bbcfe3086aced18f1ef5d1'
    }   
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    print("city id here: ", result['location_suggestions'][0]['id'])
    return str(result['location_suggestions'][0]['id'])

def api_call(city_for_api,cuisine_for_api):
    
    print("city and cuisine ---------------------------------")
    print("api_call city:",city_for_api)
    print("api call cuisine",cuisine_for_api)
    city_id_Value = city_id(city_for_api)
    url = "https://developers.zomato.com/api/v2.1/search?entity_id="+city_id_Value+"&entity_type=city&q="+city_for_api+"&count=5&cuisine="+cuisine_for_api+"&sort=cost&order=asc"
    payload={}
    headers = {
    'user-key': 'a60df80ddb6a197f5e37a95238aa3432',
    'Accept': 'application/json',
    'Cookie': 'AWSALBTG=984V6S8oSJwJKd/NN5WkFyqy5GHKgtn87vS49ki4ZF5kyMwGaNzCbatW1kiNXAiUFJr0JEYH1qnhvJeoGrJVK5T/gFvMG/PTvhwFKntBnPCy2Vpm6MlC0rtSiUpwy6T1bh7t80J3FvhbfereBYNzjIZ6t3/q687oCGe26+Qom9OCsUGrYlA='
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    print('resilt_found', type(result['results_found']))
    if response.status_code != 200:
        return "Sorry try again later......"
    if result['results_found'] == 0:
        return 'No Restaurant Found'
    if result['results_found'] == 1:
        print("=======================================")
        msg_result = str("1. <b>Name:</b> "+ result['restaurants'][0]['restaurant']['name'] + "<br><b>Link:</b> " + result['restaurants'][0]['restaurant']['url'] + "<br><b>Phone Number: </b>" + result['restaurants'][0]['restaurant']['phone_numbers'] + "<br><b>Address: </b>" + result['restaurants'][0]['restaurant']['location']['address'])
        return msg_result
    if result['results_found'] == 2:
        msg_result = str("1. <b>Name:</b> "+ result['restaurants'][0]['restaurant']['name'] + "<br><b>Link:</b> " + result['restaurants'][0]['restaurant']['url'] + "<br><b>Phone Number: </b>" + result['restaurants'][0]['restaurant']['phone_numbers'] + "<br><b>Address: </b>" + result['restaurants'][0]['restaurant']['location']['address'] 
        +"<br><br>2. <br>Name:</b> "+ result['restaurants'][1]['restaurant']['name'] + "<br><b>Link:</b> " + result['restaurants'][1]['restaurant']['url'] + "<br><b>Phone Number: " + result['restaurants'][1]['restaurant']['phone_numbers'] + "<br><b>Address: " + result['restaurants'][1]['restaurant']['location']['address'])
        return msg_result
    else:
        print("=======================================")
        msg_result = str("1. <b>Name:</b> "+ result['restaurants'][0]['restaurant']['name'] + "<br><b>Link:</b> " + result['restaurants'][0]['restaurant']['url'] + "<br><b>Phone Number:</b> " + result['restaurants'][0]['restaurant']['phone_numbers'] + "<br><b>Address: </b>" + result['restaurants'][0]['restaurant']['location']['address'] 
        +"<br><br>2. <b>Name: </b>"+ result['restaurants'][1]['restaurant']['name'] + "<br><b>Link: </b>" + result['restaurants'][1]['restaurant']['url'] + "<br><b>Phone Number: </b>" + result['restaurants'][1]['restaurant']['phone_numbers'] + "<br><b>Address: </b>" + result['restaurants'][1]['restaurant']['location']['address']
        +"<br><br>3. <b>Name: </b>"+ result['restaurants'][2]['restaurant']['name'] + "<br><b>Link:</b> " + result['restaurants'][2]['restaurant']['url'] + "<br><b>Phone Number: </b>" + result['restaurants'][2]['restaurant']['phone_numbers'] + "<br><b>Address: </b>" + result['restaurants'][2]['restaurant']['location']['address'])
        return msg_result

def remove_stepword(sentence):
    stepword_data = []
    for word in sentence.split(' '): 
        if word not in en_stops:
            if word.lower() in city:
                print("remove_stepword",word)
                city_name.append(word)
                print(city_name)
            if word.lower() in cuisines_data:
                print("remove_stepword",word)
                cuisine_name.append(word)  
                print(cuisine_name)   

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/get")
def get_bot_response():
    sentence = request.args.get('msg')
    remove_stepword(sentence)
    if sentence == "quit":
        return str(f"See you soon...")
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return str((f"{random.choice(intent['responses'])}"))
    else:
        if city_name!=[] or cuisine_name!= []:
            print("city_name",city_name[0])
            print("cuisine_name",cuisine_name[0])
            api_result = api_call(city_name[0],cuisine_name[0])
            return api_result
        else:
            return "Can't found restaurants..."
    return str(f"I do not understand... Try again")

if __name__ == '__main__':
    app.run()