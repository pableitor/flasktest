from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = "John Elder's Blog"
    return render_template('index.html', title = title)

@app.route('/about')
def about():
    names = ['John', 'Mary', 'Wes','Annie','Suzy']
    title = "About"
    return render_template('about.html', names = names, title= title) # passing variable to a web page
