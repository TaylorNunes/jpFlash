import sqlite3 
from sqlite3 import Error

def make_db():
  databasePath = "db/testdatabase.db"
  conn = sqlite3.connect(databasePath)
  return conn

# check in the table exists
def check_table(curr, name: str):
  qry_check = ''' \
  SELECT count(name) \
  FROM sqlite_master WHERE type='table' \
  AND name='{0}' \
  '''
  curr.execute(qry_check.format(name));
  if curr.fetchone()[0]==1: 
    return True
  else:
    return False

def make_table(curr, name: str):
  qry_create = ''' \
  CREATE TABLE {0} (id INT AUTO_INCREMENT PRIMARY KEY, \
  source VARCHAR(255),\
  sentence VARCHAR(255),\
  sentence_reading VARCHAR(255),\
  translation VARCHAR(255),\
  target_word VARCHAR(255),\
  word_reading VARCHAR(255),\
  definition VARCHAR(255))\
  '''
  curr.execute(qry_create.format(name))
  return

def insert_row(curr, name: str, values):
  qry_insert = "INSERT INTO {0}(source,sentence,translation,target_word) values(?, ?, ?, ?)".format(name)
  curr.execute(qry_insert, values)
  return

def get_values(curr, name: str, source: str):
  return curr.execute("SELECT * FROM {0} WHERE source='{1}'".format(name,source)).fetchall()
