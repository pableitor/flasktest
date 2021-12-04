
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config[ 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize db
db = SQLAlchemy(app)

#Create DB model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    #Create a function to return a string when we add a friend
    def __repr__(self):
        return '<Name %r>' % self.id
 

subscribers = [] # lista de suscriptores

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was a problem deletint that friend"
        
@app.route('/update/<int:id>', methods = ["POST", "GET"] )
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was a problem updating that friend"
    else:
        return render_template('update.html', friend_to_update = friend_to_update)
        
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/about')
def about():
    names_list = ['John', 'Mary', 'Wes','Annie','Suzy']
    return render_template('about.html', names = names_list) # passing variable to a web page

@app.route('/friends' , methods = ["POST", "GET"]) # procesa datos del formulario friends.html
def friends():
    
    if request.method == "POST":
        friend_name = request.form['name']
        #friend_name = request.form.get('name')
        new_friend = Friends(name = friend_name)
        
        #Push to database
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding your friend"
            
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", friends = friends)

@app.route('/subscribe') #abre formulario 
def subscribe():

    return render_template('subscribe.html')

@app.route('/form', methods = ["POST"]) # procesa los datos del formulario que le ha enviado subscribe.html via POST
def form():
    first_name = request.form.get('first_name') # recibe  la variable first_name del input box
    last_name = request.form.get('last_name') # recibe  la variable last_name del input box
    email = request.form.get('email') # recibe  la variable first_name del input box
 
    
    if not first_name or not last_name or not email:
        error_statement = "All form fields required."
        return render_template("subscribe.html",  # faltan datos vuelve a la pag. subscribe
                                                   #y pasamos los valores que ha tecleado el user
                               error_statement =  error_statement,
                               first_name = first_name,
                               last_name = last_name,
                               email = email)
    
    subscribers.append(f"{first_name} {last_name} || {email}") #agrega los datos a la lista
    return render_template('form.html', subscribers = subscribers) # abre la pagina para procesar los datos

app.run(debug = False) # /desactiva/activa modo debug, detecta cambios en los ficheros de trabajo