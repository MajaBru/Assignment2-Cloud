from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
import re, os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import pymysql
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_user, logout_user, login_required, LoginManager, UserMixin
from models import db, User, Post
from uuid import uuid4
import atexit

app = Flask(__name__, template_folder='../front-end', static_folder='../front-end/static')

app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/redditdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'sessions')
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
            login_user(new_user)  # Login the user after successful registration

    return render_template('register.html', msg=msg)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        # Check if the user exists
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('login.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/home', methods=['GET'])
def home():
    posts = db.session.query(Post, User).join(User).order_by(Post.created_at.desc()).limit(10).all()
    return render_template('home.html', posts=posts, current_user=current_user)



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at} for user in users]
    return jsonify(user_list)

@app.route('/posts', methods=['POST'])
@login_required  # Require login to create a post
def create_post():
    data = request.get_json()
    if current_user.is_authenticated:  # Ensure user is authenticated
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
        user = User.query.get(post.user_id)
        if user:
            username = user.username
            
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
        likes_count = data.get('likes_count', 0)

        if post_id and likes_count >= 0:
            post = Post.query.get(post_id)
            if post:
                post.likes_count += likes_count
                db.session.commit()
                return jsonify({'success': True, 'message': 'Post liked successfully!'})
            else:
                return jsonify({'success': False, 'message': 'Post not found!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid data provided!'})
    else:
        return jsonify({'success': False, 'message': 'Unsupported Media Type'}), 415



@app.route('/dogs', methods=['GET', 'POST'])
@login_required
def dogs_subreddit():
    if request.method == 'POST':
        text = request.form['text']
        new_post = Post(user_id=current_user.id, text=text, category='Dogs')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/dogs')
    
    # Fetch both Post and User objects
    posts = db.session.query(Post, User).join(User).filter(Post.category == 'Dogs').order_by(Post.created_at.desc()).limit(10).all()
    return render_template('subreddit.html', category='Dogs', posts=posts, username=current_user.username)



@app.route('/cats', methods=['GET', 'POST'])
@login_required
def cats_subreddit():
    if request.method == 'POST':
        text = request.form['text']
        new_post = Post(user_id=current_user.id, text=text, category='Cats')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/cats')
    
    # Fetch both Post and User objects
    posts = db.session.query(Post, User).join(User).filter(Post.category == 'Cats').order_by(Post.created_at.desc()).limit(10).all()
    return render_template('subreddit.html', category='Cats', posts=posts, username=current_user.username)


@app.route('/bunnies', methods=['GET', 'POST'])
@login_required
def bunnies_subreddit():
    if request.method == 'POST':
        text = request.form['text']
        new_post = Post(user_id=current_user.id, text=text, category='Bunnies')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/bunnies')
    
    # Fetch both Post and User objects
    posts = db.session.query(Post, User).join(User).filter(Post.category == 'Bunnies').order_by(Post.created_at.desc()).limit(10).all()
    return render_template('subreddit.html', category='Bunnies', posts=posts, username=current_user.username)




@app.route('/user/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        if current_user.is_authenticated and current_user.username == username:
            return render_template('user_profile.html', user=user, is_own_profile=True)
        else:
            return render_template('user_profile.html', user=user, is_own_profile=False)
    else:
        return render_template('user_not_found.html', username=username)
    
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    
    # Generate unique identifier for deleted account
    unique_identifier = str(uuid4()).replace('-', '')[:8]  # Example: 'a1b2c3d4'
    
    # Update username and email to unique identifier
    user.username = f'[deleted-{unique_identifier}]'
    user.email = f'deleted_{unique_identifier}@example.com'
    
    # Commit changes to the database
    db.session.commit()
    
    # Log out the user
    logout_user()
    
    # Redirect to index page
    return redirect(url_for('index'))  # Redirect to the index route


def create_tables():
    with app.app_context():
        db.create_all()
        print('Tables created')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
