import mysql.connector

# setup mysql connection
mydb = mysql.connector.connect(
    host="mysql",
    user="group4",
    password="root123",
    database="redditdb"
)

my_cursor = mydb.cursor()

# create table
my_cursor.execute("CREATE TABLE messages (message_id INT AUTO_INCREMENT PRIMARY KEY, message TEXT)")