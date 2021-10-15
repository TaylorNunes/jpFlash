import sqlite3 
from sqlite3 import Error

def make_db():
  databasePath = "db/testdatabase.db"
  conn = sqlite3.connect(databasePath)
  return conn

# check in the table exists
def check_table(cur, name: str):
  qry_check = ''' \
  SELECT count(name) \
  FROM sqlite_master WHERE type='table' \
  AND name='{0}' \
  '''
  cur.execute(qry_check.format(name));
  if cur.fetchone()[0]==1: 
    return True
  else:
    return False

def make_table(cur, name: str):
  qry_create = ''' \
  CREATE TABLE {0} (id INT AUTO_INCREMENT PRIMARY KEY, \
  source VARCHAR(255),\
  sentence VARCHAR(255),\
  sentence_reading VARCHAR(255),\
  translation VARCHAR(255),\
  target_word VARCHAR(255),\
  word_reading VARCHAR(255),\
  definition VARCHAR(255),\
  link VARCHAR(255))\
  '''
  cur.execute(qry_create.format(name))
  return

def insert_row(cur, name: str, values):
  qry_check  = "SELECT rowid FROM {0} WHERE target_word = '{1}'".format(name,values[3])
  cur.execute(qry_check)
  result_num = len(cur.fetchall())
  if result_num > 0:
    print("There are {0} entries for '{1}'. Skipping insert.".format(result_num,values[3]))
    return
  print("Inserting '{0}' into table".format(values[3]))
  qry_insert = "INSERT INTO {0}(source,sentence,translation,target_word,link) values(?, ?, ?, ?,?)".format(name)
  cur.execute(qry_insert, values)
  return

def get_values(cur, name: str, source: str):
  return cur.execute("SELECT * FROM {0} WHERE source='{1}'".format(name,source)).fetchall()
