from flask import Flask, render_template, request

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

@app.route('/strains', methods=['POST', 'GET'])
def strains():
    if request.method == 'POST':
       characteristics = request.form.getlist('favorite_vibe') 
       print(characteristics)
    return render_template('strains.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')


if __name__ == "__main__":
    app.run(debug=True)