from flask import Flask, render_template, request, redirect, session, jsonify
import re, os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from flask_bcrypt import Bcrypt
from models import db, User, Post, Like, LikeBatch
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__, template_folder='../front-end', static_folder='../front-end/static')

app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/redditdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'sessions')
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

db.init_app(app)
bcrypt = Bcrypt(app)

def create_database():
    connection = pymysql.connect(host='localhost', user='root')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS redditdb")
    cursor.close()
    connection.close()

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

@app.route('/likes', methods=['POST'])
def like_post():
    data = request.get_json()
    new_like = Like(user_id=data['user_id'], post_id=data['post_id'])
    db.session.add(new_like)
    new_like_batch = LikeBatch(status='pending', like_id=new_like.id, created_at=datetime.utcnow())
    db.session.add(new_like_batch)
    db.session.commit()
    return jsonify({'message': 'Post liked!'})

def process_like_batches():
    like_batches = LikeBatch.query.filter_by(status='pending').all()
    for like_batch in like_batches:
        post = Post.query.get(like_batch.like.post_id)
        post.likes_count += 1
        like_batch.status = 'processed'
    db.session.commit()
    db.session.close()

@app.route('/create_post.html')
def create_post_page():
    return render_template('create_post.html')

@app.route('/all_posts.html')
def all_posts_page():
    return render_template('all_posts.html')

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

@app.route('/dogs', methods=['GET', 'POST'])
def dogs_subreddit():
    if 'loggedin' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        text = request.form['text']
        user_id = User.query.filter_by(username=session['username']).first().id
        new_post = Post(user_id=user_id, text=text, category='Dogs')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/dogs')
    
    posts = Post.query.filter_by(category='Dogs').all()
    return render_template('subreddit.html', category='Dogs', posts=posts, username=session['username'])

@app.route('/cats', methods=['GET', 'POST'])
def cats_subreddit():
    if 'loggedin' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        text = request.form['text']
        user_id = User.query.filter_by(username=session['username']).first().id
        new_post = Post(user_id=user_id, text=text, category='Cats')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/cats')
    
    posts = Post.query.filter_by(category='Cats').all()
    return render_template('subreddit.html', category='Cats', posts=posts, username=session['username'])

@app.route('/bunnies', methods=['GET', 'POST'])
def bunnies_subreddit():
    if 'loggedin' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        text = request.form['text']
        user_id = User.query.filter_by(username=session['username']).first().id
        new_post = Post(user_id=user_id, text=text, category='Bunnies')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/bunnies')
    
    posts = Post.query.filter_by(category='Bunnies').all()
    return render_template('subreddit.html', category='Bunnies', posts=posts, username=session['username'])

def create_tables():
    with app.app_context():
        db.create_all()
        print('Tables created')

if __name__ == '__main__':
    create_database()
    create_tables()
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_like_batches, 'interval', minutes=1)
    scheduler.start()
    app.run(debug=True, port=5000)
