# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request,redirect,session,url_for
from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)
app.secret_key = 'hello'
# name of database
app.config['MONGO_DBNAME'] = 'movies'
# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://movie_admin:6JWG6IlCwy3qBY2M@cluster0-4owxw.mongodb.net/movies?retryWrites=true&w=majority'
mongo = PyMongo(app)
# -- Routes section --
# INDEX
@app.route('/')
@app.route('/index')
def index():
    collection = mongo.db.entry
    entry = collection.find({})
    return render_template("index.html",entry=entry)
# ADD SONGS
@app.route('/add')
def add():
    # define a variable for the collection you want to connect to
    entry = mongo.db.entry
    # use some method on that variable to add/find/delete data
    entry.insert({"title":"Finding Nemo","genre": "Animation", "year":2003})
    # return a message to the user (or pass data to a template)
    return "Your movie has been added."
#add new movie through form
@app.route('/movie/new',methods=['GET','POST'])
def new_movie():
    if request.method == 'GET':
        return render_template("add_movie.html")
    else:
        movie_name = request.form['title']
        movie_genre = request.form['genre']
        movie_year = request.form['year']
    collection = mongo.db.entry
    #find all data
    collection.insert({"title":movie_name, "genre":movie_genre,"year":movie_year})
    return redirect('/')
#SIGN UP
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        users=mongo.db.users
        existing_user=users.find_one({'name' : request.form['username']})
        if existing_user is None:
            users.insert({'name': request.form['username'],'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username already exists! Try logging in.'
    return render_template('signup.html')
#LOGIN
@app.route('/login',methods=['POST'])
def login():
    users=mongo.db.users
    login_user = users.find_one({'name': request.form['username'] })
    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return 'Invalid username/password combination'
#Log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')