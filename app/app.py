from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import MySQLdb.cursors
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from models import db, User

app = Flask(__name__, template_folder='../front-end')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/redditdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


# retreive all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at} for user in users]
    return jsonify(user_list)  


# make db if it doesnt exist
def create_database():
    connection = pymysql.connect(host='localhost', user='root')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS redditdb")
    connection.close()


# Initialize the database and create the tables
def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_database()
    create_tables()
    app.run(debug=True, port=5000)