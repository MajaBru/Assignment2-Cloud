from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    likes_count = db.Column(db.Integer, default=0)

    # Define a property to get the username dynamically
    @property
    def username(self):
        user = User.query.get(self.user_id)
        if user:
            return user.username
        else:
            return None

    def __repr__(self):
        return f"Post('{self.text}', '{self.category}', '{self.created_at}')"


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    post = db.relationship('Post', backref=db.backref('likes', lazy=True))

class LikeBatch(db.Model):
    __tablename__ = 'like_batch'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    like_id = db.Column(db.Integer, db.ForeignKey('like.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    like = db.relationship('Like', backref=db.backref('like_batches', lazy=True))