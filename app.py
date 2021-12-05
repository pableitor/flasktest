from flask import Flask, render_template, request

app = Flask(__name__)

subscribers = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    names = ['John', 'Mary', 'Wes','Annie','Suzy']

    return render_template('about.html', names = names) # passing variable to a web page

@app.route('/subscribe')
def subscribe():
    
    return render_template('subscribe.html')

@app.route('/form', methods=["POST"]) # estamos posteando info a form.html
def form():
    
    first_name = request.form.get("first_name") #recibe las variables name del formulario
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    
    if not first_name or not last_name or not email:
        error_statement = "All form fields required ..."
        return render_template( "subscribe.html", error_statement = error_statement, 
                               first_name=first_name, last_name=last_name, email=email)
    subscribers.append(f"{first_name} {last_name} {email}")
    return render_template('form.html', subscribers = subscribers)
