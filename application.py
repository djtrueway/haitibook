import os

from flask import Flask, session, render_template ,redirect, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/login", methods=['GET','POST'])
def connexion():
    message = []
    title = "Sign up or Login"
    if request.method == 'GET':
        return render_template('login.html', title=title)
    else:
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if full_name and username and password and email:
            if password == password2:
                password = generate_password_hash(password)
                connect = db.execute("INSERT INTO users (full_name, username, email, password) VALUES (:full_name, :username, :email, :password)",
                            {"full_name":full_name ,"username":username , "email":email , "password":password})
                db.commit()
                if connect:
                    rows = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()

                    session["user_id"] = rows[0]

                return redirect('/')
            else:
                msg = "password don't match "
                message.append(msg)
                return render_template('login.html',message=message)
        else:
            msg = 'please give us all informations'
            message.append(msg)
            return render_template('login.html',message=message)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':

        if session.get('user_id') != None:
            user_id = session.get('user_id')
            user_data = db.execute('SELECT * FROM users WHERE id = :id',{'id': user_id}).fetchone()
            return render_template('index.html', user_data=user_data)
        else:
            message = []
            msg = "login or sign up for more experience"
            message.append(msg)
            return redirect('/login')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user_data = db.execute('SELECT * FROM users WHERE username = :username',{'username': username}).fetchone()
            if user_data:               
                print(check_password_hash(user_data.password, password))

                if check_password_hash(user_data.password, password):
                    session['user_id'] = user_data[0]
                    return render_template('index.html', user_data=user_data)

                else:
                    message = []
                    msg ="password don't match"
                    message.append(msg)
                    return render_template('login.html', message=message)

            else:
                message = []
                msg ="don't have this account in our databases"
                message.append(msg)
                return render_template('login.html', message=message)
                
        else:
            message = []
            msg ="missing username or password !!!"
            message.append(msg)
            return render_template('login.html', message=message)

@app.route('/search/book', methods=['GET'])
def search():
    if request.method == 'GET':
        if session.get('user_id') != None:
            user_id = session.get('user_id')
            user_data = db.execute('SELECT * FROM users WHERE id = :id',{'id': user_id}).fetchone()

            book = request.form.get('search_book')
            msg = []
            msg.append(book)
            return render_template('index.html',msg=msg , user_data=user_data)
            """
            all_book = db.execute("SELECT * FROM book WHERE isbn = :isbn ",
                                    {"isbn": book}).fetchall()
            if all_book == None:
                all_book = db.execute("SELECT * FROM book WHERE author = :author ",
                                        {"author": book}).fetchall()
            if all_book == None:
                all_book = db.execute("SELECT * FROM book WHERE title = :title ",
                                        {"title": book}).fetchall()
            else:
                msg = []
                msg.append(book)
                return render_template('index.html',msg=msg , all_book=all_book , user_data=user_data)

            return render_template('index.html',all_book=all_book, user_data=user_data) """



@app.route('/book/<int:book_id>')
def book(book_id):
    if session.get('user_id') != None:
        user_id = session.get('user_id')
        user_data = db.execute('SELECT * FROM users WHERE id = :id',{'id': user_id}).fetchone()
        try :
            book = db.execute("SELECT * FROM book WHERE id = :id",{"id":book_id}).fetchone()
        except ValueError:
            return "bad id ", 404
        if book:
            isbn = str(book.isbn)
            res = requests.get("https://www.goodreads.com/book/review_counts.json", 
                                params={"key": "lpkJKa68w5R7gbidLakSw", "isbns": isbn })
            if res.status_code == 200:
                data = res.json()
                return render_template('book.html',book=book, data=data, user_data=user_data)
            else:
                data = []
                return render_template('book.html',book=book, data=data, user_data=user_data)

            
    else:
        return redirect('/login')
    




@app.route('/api/<string:isbn>')
def api(isbn):
    pass

