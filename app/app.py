from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import MySQLdb.cursors
import re, os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from models import db, User, Post, Like
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='../front-end', static_folder='../front-end/static')

app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/redditdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'sessions')
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

# Initialize
db.init_app(app)
bcrypt = Bcrypt(app)
connection = pymysql.connect(host='localhost', user='root', password='root', db='redditdb')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') #hashing with bcrypt

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            msg = 'You have successfully registered!'

    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # setting user session
            session['loggedin'] = True

            session['username'] = user.username
            session['email'] = user.email
            return redirect('/home')
        else:
            msg = 'Invalid username or password!'
            return render_template('login.html', msg=msg)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect('/login')


@app.route('/home', methods=['GET'])
def home():
    if session.get('loggedin') is True:
        username = session.get('username')
        email = session.get('email')
        if username and email:
            return render_template('home.html', username=session['username'])
    
    return redirect('/login')





# retreive all users json format
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at} for user in users]
    return jsonify(user_list)


# make db if it doesnt exist
def create_database():
    connection = pymysql.connect(host='localhost', user='root', password='root')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS redditdb")
    cursor.execute("SHOW DATABASES")

    for databases in cursor:
        print(databases)

    cursor.close()
    connection.close()


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(user_id=data['user_id'], text=data['text'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'New post created!'})

@app.route('/likes', methods=['POST'])
def like_post():
    data = request.get_json()
    new_like = Like(user_id=data['user_id'], post_id=data['post_id'])
    db.session.add(new_like)
    post = Post.query.get(data['post_id'])
    post.likes_count += 1
    db.session.commit()
    return jsonify({'message': 'Post liked!'})


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    post_list = [{'id': post.id, 'user_id': post.user_id, 'text': post.text, 'created_at': post.created_at, 'likes_count': post.likes_count} for post in posts]
    return jsonify(post_list)

@app.route('/likes', methods=['GET'])
def get_likes():
    likes = Like.query.all()
    like_list = [{'id': like.id, 'user_id': like.user_id, 'post_id': like.post_id, 'created_at': like.created_at} for like in likes]
    return jsonify(like_list)

# Initialize the database and create the tables
def create_tables():
    with app.app_context():
        db.create_all()
        print('Tables created')


if __name__ == '__main__':
    create_database()
    create_tables()
    app.run(debug=True, port=5000)