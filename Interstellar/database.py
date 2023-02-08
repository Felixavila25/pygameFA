import sqlite3
from sqlite3 import Error

DB_FILE = "sqlite.db"

# create connectiom to specified database and if it is no exist then it is created
def create_connection():
   conn = None
   try:
      conn = sqlite3.connect(DB_FILE)
   except Error as e:
      print(e)

   return conn

# create table in database
def create_table(conn, create_table_sql):
   try:
      c = conn.cursor()
      c.execute(create_table_sql)
   except Error as e:
      print(e)

# create connection
def init_database():
   sql = "CREATE TABLE IF NOT EXISTS scores (id integer PRIMARY KEY, name text NOT NULL, score integer NOT NULL);"

   # create a database connection
   conn = create_connection()

   if conn is not None:
      # create scores table
      create_table(conn, sql)
      conn.close() # close connection
   else:
      print("Error! cannot create the database connection.")

# this get the scores sorted by score
def get_scores(conn):
   sql = "SELECT * FROM scores ORDER BY score DESC;"
   cur = conn.cursor()
   cur.execute(sql)
   rows = cur.fetchall()
   return rows

# insert a score in database
def insert_score(conn, score):
   sql = "INSERT INTO scores (name, score) VALUES(?, ?)"
   cur = conn.cursor()
   cur.execute(sql, score)
   conn.commit()
   return cur.lastrowid
