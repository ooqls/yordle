from internal.records.sqllite import SQLliteConn
from internal.records.words import WordDB
from random import randint

words = ["test1", "test2", "test3", "test4", "test5"]


def new_test_word_db() -> WordDB:
  n = randint(0, 1_000_000)
  conn = SQLliteConn("/tmp/{}-test.db".format(n))
  db = WordDB(conn)
  db.create_database()
  db.add_words(words)
  
  return db