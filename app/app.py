from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pymysql


app = Flask(__name__, template_folder='../front-end')
api = Api(app)

db = pymysql.connect("localhost", "root", "root", "redditdb")





# setup mysql connection
""" def dbconn():
    config = {
        'host': "129.114.27.249",
        'port': "3306",
        'user': "group4",
        'password': "root123",
        'database': "redditdb"
    }

    connection = mysql.connector.connect(**config)
    # cursor can be used to do operations on the database
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results """


@app.route('/')
def index():
    return render_template('index.html')
    """ return jsonify(dbconn()) """


# If ran (not just imported from elsewhere), launch the server.
""" if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
 """

 if __name__ == '__main__':
    app.run(debug=True)