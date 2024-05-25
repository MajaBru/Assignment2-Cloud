from flask import Flask, render_template, request, redirect, session, jsonify
import re, os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from flask_bcrypt import Bcrypt
from models import db, User, Post
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
            posts = Post.query.order_by(Post.created_at.desc()).all()  # Sort posts by created_at in descending order
            return render_template('home.html', username=session['username'], posts=posts)
    return redirect('/login')

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at} for user in users]
    return jsonify(user_list)

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    current_user = User.query.filter_by(username=session.get('username')).first()
    if current_user:
        new_post = Post(
            user_id=current_user.id,
            text=data['text'],
            category=data['category']
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'New post created!'})
    else:
        return jsonify({'error': 'User not found!'})


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    post_list = []
    for post in posts:
        # Get the username associated with the user_id of each post
        username = User.query.filter_by(id=post.user_id).first().username
        post_data = {
            'id': post.id,
            'user_id': post.user_id,
            'username': username,
            'text': post.text,
            'category': post.category,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'likes_count': post.likes_count
        }
        post_list.append(post_data)
    return jsonify(post_list)

@app.route('/likes', methods=['POST'])
def like_post():
    if request.is_json:
        data = request.json
        post_id = data.get('post_id')
        # Check if the post exists
        post = Post.query.get(post_id)
        if post:
            # Increment the likes_count of the post
            post.likes_count += 1
            db.session.commit()
            return jsonify({'message': 'Post liked successfully!'})
        else:
            return jsonify({'error': 'Post not found!'})
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415


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
    
    posts = Post.query.filter_by(category='Dogs').order_by(Post.created_at.desc()).all() 
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
    
    posts = Post.query.filter_by(category='Cats').order_by(Post.created_at.desc()).all() 
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
    
    posts = Post.query.filter_by(category='Bunnies').order_by(Post.created_at.desc()).all() 
    return render_template('subreddit.html', category='Bunnies', posts=posts, username=session['username'])

def create_tables():
    with app.app_context():
        db.create_all()
        print('Tables created')

if __name__ == '__main__':
    create_database()
    create_tables()
    app.run(debug=True, port=5000)
