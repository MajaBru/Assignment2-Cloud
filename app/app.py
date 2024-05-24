from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pymysql
import os
import re

app = Flask(__name__, template_folder='../front-end', static_folder='../front-end/static')

app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@db/redditdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import db, User, Post, Like

# In-memory structure to store like counts
like_batch = {}

# Initialize database
def create_database():
    connection = pymysql.connect(host='db', user='root', password='')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS redditdb")
    connection.close()

def create_tables():
    with app.app_context():
        db.create_all()

# Background task to process like batches
def process_likes():
    with app.app_context():
        for post_id, like_count in like_batch.items():
            post = Post.query.get(post_id)
            if post:
                post.likes_count += like_count
                db.session.commit()
        like_batch.clear()

# Scheduler to run the background task every minute
scheduler = BackgroundScheduler()
scheduler.add_job(func=process_likes, trigger="interval", seconds=60)
scheduler.start()

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

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

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
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['loggedin'] = True
            session['username'] = user.username
            session['email'] = user.email
            return redirect('/home')
        else:
            msg = 'Invalid username or password!'

    return render_template('login.html', msg=msg)

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
            return render_template('home.html', username=username)
    return redirect('/login')


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at} for user in users]
    return jsonify(user_list)

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(user_id=data['user_id'], text=data['text'], category=data['category'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'New post created!'})

@app.route('/posts', methods=['GET'])
def get_posts():
    category = request.args.get('category')
    if category:
        posts = Post.query.filter_by(category=category).all()
    else:
        posts = Post.query.all()
    post_list = [{'id': post.id, 'user_id': post.user_id, 'text': post.text, 'created_at': post.created_at, 'likes_count': post.likes_count, 'category': post.category} for post in posts]
    return jsonify(post_list)

@app.route('/likes', methods=['POST'])
def like_post():
    data = request.get_json()
    post_id = data['post_id']
    like_batch[post_id] = like_batch.get(post_id, 0) + 1
    return jsonify({'message': 'Post liked!'})

@app.route('/likes', methods=['GET'])
def get_likes():
    likes = Like.query.all()
    like_list = [{'id': like.id, 'user_id': like.user_id, 'post_id': like.post_id, 'created_at': like.created_at} for like in likes]
    return jsonify(like_list)

@app.route('/posts/dogs', methods=['GET', 'POST'])
def posts_dogs():
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            text = request.form['text']
            new_post = Post(user_id=user_id, text=text, category='dogs')
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts/dogs')
        return redirect('/login')
    posts = Post.query.filter_by(category='dogs').all()
    return render_template('posts.html', posts=posts, category='Dogs')

@app.route('/posts/cats', methods=['GET', 'POST'])
def posts_cats():
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            text = request.form['text']
            new_post = Post(user_id=user_id, text=text, category='cats')
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts/cats')
        return redirect('/login')
    posts = Post.query.filter_by(category='cats').all()
    return render_template('posts.html', posts=posts, category='Cats')

@app.route('/posts/bunnies', methods=['GET', 'POST'])
def posts_bunnies():
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            text = request.form['text']
            new_post = Post(user_id=user_id, text=text, category='bunnies')
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts/bunnies')
        return redirect('/login')
    posts = Post.query.filter_by(category='bunnies').all()
    return render_template('posts.html', posts=posts, category='Bunnies')

if __name__ == '__main__':
    create_database()
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
