import sqlite3
import json
import datetime
from internal.records.sqllite import SQLliteConn
from internal.records.sql import SQLConn, SQLTransaction
from random import randint

word_db = None

def init_word_db(hero_file: str = "internal/records/heros.json"):
  global word_db
  conn: SQLConn = SQLliteConn("champ.db")
  word_db = WordDB(conn)
  word_db.create_database()
  word_db.load_json(hero_file)
  
def set_word_db(sql_path: str):
  global word_db
  conn: SQLConn = SQLliteConn(sql_path)
  word_db = WordDB(conn)

def get_word_db():
  global word_db
  return word_db


class WordDB:
  db: SQLConn
  
  def __init__(self, c: SQLConn):
    self.db: SQLConn = c
  
  def create_database(self):
    tx: SQLTransaction = self.db.transaction()
    tx.execute("CREATE TABLE IF NOT EXISTS words (word_id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT) ")
    tx.commit()
    tx.close()
    
  def load_json(self, json_file: str) -> None:
    heros = list()
    with open(json_file, "r") as f:
      data = json.load(f)
      for name in data["data"].keys():
        heros.append(name)
        
    self.add_words(heros)
  
  def add_word(self, word: str) -> None:
    tx: SQLTransaction = self.db.transaction()
    tx.execute("INSERT INTO words(word) VALUES (?)", [word])
    tx.commit()
    tx.close()
  
  def add_words(self, words: list[str]) -> None:
    tx: SQLTransaction = self.db.transaction()
    tx.executemany("INSERT INTO words(word) VALUES (?)", [[h] for h in words])
    tx.commit()
    tx.close()
    
  def get_all_words(self, limit: int = 10, offset: int = 0) -> list[str]:
    tx: SQLTransaction = self.db.transaction()
    tx.execute("SELECT * FROM words LIMIT ? OFFSET ?", [limit, offset])
    res = tx.fetchall()
    tx.close()
    words = list()
    
    for c in res:
      words.append(c[1])
    return words
  
  def count_words(self) -> int:
    tx: SQLTransaction = self.db.transaction()
    tx.execute("SELECT COUNT(*) FROM words")
    res = tx.fetchone()
    tx.close()
    return res[0]
  
  def get_todays_word(self) -> str:
    # Get the current date
    current_date = datetime.datetime.now()

    # Get the day of the year
    day_of_year = current_date.timetuple().tm_yday
    n_words = self.count_words()
    word_index = day_of_year % n_words
    words = self.get_all_words(limit=1, offset=word_index)
    print(words)
    return words[0]
  
  def get_random_word(self) -> str:
    n_words = self.count_words()
    word_index = randint(0, n_words-1)
    words = self.get_all_words(limit=1, offset=word_index)
    return words[0]
  
  def get_random_word_list(self, n: int) -> list[str]:
    n_words = self.count_words()
    words = list()
    for i in range(n):
      word_index = randint(0, n_words)
      word = self.get_all_words(limit=1, offset=word_index-1)
      words.append(word[0])
    return words
    

  def close(self) -> None:
    self.db.close()
    
if __name__ == "__main__":
  conn: SQLConn = SQLliteConn("fewfew.db")
  
  c = WordDB(conn)
  c.create_database()
  c.add_word("test4")
  
  print(c.get_all_words())
  print(c.count_words())
  print(c.get_random_word())
      
  