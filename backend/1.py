import mysql.connector
import uuid

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1111",
  database="mariadb"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Define the data to be inserted
data = [
    {'id': uuid.uuid4().hex, 'title': 'CyberPunk', 'genre': 'Crime', 'played': True}
]

# Insert the data into the "games" table
for row in data:
    sql = "INSERT INTO games (id, title, genre, played) VALUES (%s, %s, %s, %s)"
    val = (row['id'], row['title'], row['genre'], row['played'])
    mycursor.execute(sql, val)

# Commit the changes to the database
mydb.commit()

# Verify that the data was inserted correctly
mycursor.execute("SELECT * FROM games")
result = mycursor.fetchall()
for row in result:
    print(row)
