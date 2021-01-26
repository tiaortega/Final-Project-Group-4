from flask import Flask, render_template, request
from flask import jsonify
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/energy')
def energy():
    return render_template('energy.html')    

@app.route('/strains', methods=['POST', 'GET'])
def strains():
    if request.method == 'POST':
       characteristics = request.form.getlist('favorite_vibe') 
       print(characteristics)

       dictionary_vibes = []
       for vibe in characteristics:
           formatted_vibe = get_vibe(request.form, vibe)
           dictionary_vibes.append(formatted_vibe)

       for dic_vibe in dictionary_vibes:
           print(dic_vibe)

       # insert code that sends the characteristics to the model and returns the recommended strains
       return render_template('strains.html', strains=strains)
       
    return render_template('strains.html')

@app.route('/handle_form', methods=['POST'])
def handle_form():
    energetic = ['energetic', 'creative', 'aroused',
     'happy', 'uplifted', 'focused', 'talkative', 'hungry'
     ]

    relaxed = ['relaxed', 'sleepy', 'euphoric', 'tingly']

    dict_request_form = request.form.to_dict(flat=False)

    for b in dict_request_form:
        vibes = dict_request_form[b]

    energetic_value = 0
    relaxed_value = 0
    for vibe in vibes:
        if vibe in energetic:
            energetic_value = energetic_value + 1

        if vibe in relaxed:
            relaxed_value = relaxed_value + 1

    json_response = {
        'energetic': energetic_value,
        'relaxed': relaxed_value,
        'vibes': vibes
    }

    cani = pd.read_csv("./Resources/Strain_Frame_Energy.csv")
    X = cani[['Energetic','Relax']].to_numpy()
    Y = cani['StrainType'].to_numpy()

    logreg = LogisticRegression(C=1e5)
    logreg.fit(X, Y)

    Z = logreg.predict([[json_response['energetic'], json_response['relaxed']]])
    print('Prediction')
    print(Z)

    # Grab the prediction, its in array format like: [3]
    prediction = Z[0]
    
    if prediction == 1:
        json_response['prediction'] = 'Hybrid'
    elif prediction == 2:
        json_response['prediction'] = 'Indica'
    elif prediction == 3:
        json_response['prediction'] = 'Sativa'
    
    return render_template('strains.html', strains=json_response)



@app.route('/resources')
def resources():
    return render_template('resources.html')


if __name__ == "__main__":
    app.run(debug=True)