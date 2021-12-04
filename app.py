from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    names = ['John', 'Mary', 'Wes','Annie','Suzy']

    return render_template('about.html', names = names) # passing variable to a web page
