import sqlite3
import json
import datetime
from internal.records.sqllite import SQLliteConn
from internal.records.sql import SQLConn, SQLTransaction

champ_db = None

def init_champ_db(hero_file: str = "internal/records/heros.json"):
  global champ_db
  conn: SQLConn = SQLliteConn("champ.db")
  champ_db = ChampDB(conn)
  champ_db.create_database()
  champ_db.load_json(hero_file)

def get_champ_db():
  global champ_db
  return champ_db


class ChampDB:
  db: SQLConn
  
  def __init__(self, c: SQLConn):
    self.db: SQLConn = c
  
  def create_database(self):
    tx: SQLTransaction = self.db.transaction()
    tx.execute("CREATE TABLE IF NOT EXISTS champs (champ_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT) ")
    tx.commit()
    tx.close()
    
  def load_json(self, json_file: str) -> None:
    heros = list()
    with open(json_file, "r") as f:
      data = json.load(f)
      for name in data["data"].keys():
        heros.append(name)
        
    self.add_champions(heros)
  
  def add_champion(self, champ: str) -> None:
    tx: SQLTransaction = self.db.transaction()
    tx.execute("INSERT INTO champs(name) VALUES (?)", [champ])
    tx.commit()
    tx.close()
  
  def add_champions(self, champs: list[str]) -> None:
    tx: SQLTransaction = self.db.transaction()
    tx.executemany("INSERT INTO champs(name) VALUES (?)", [[h] for h in champs])
    tx.commit()
    tx.close()
    
  def get_all_champions(self, limit: int = 10, offset: int = 0) -> list[str]:
    tx: SQLTransaction = self.db.transaction()
    tx.execute("SELECT * FROM champs LIMIT ? OFFSET ?", [limit, offset])
    res = tx.fetchall()
    tx.close()
    champs = list()
    
    for c in res:
      champs.append(c[1])
    return champs
  
  def count_champions(self) -> int:
    tx: SQLTransaction = self.db.transaction()
    tx.execute("SELECT COUNT(*) FROM champs")
    res = tx.fetchone()
    tx.close()
    return res[0]
  
  def get_todays_champion(self) -> str:
    # Get the current date
    current_date = datetime.datetime.now()

    # Get the day of the year
    day_of_year = current_date.timetuple().tm_yday
    n_champs = self.count_champions()
    champ_index = day_of_year % n_champs
    champs = self.get_all_champions(limit=1, offset=champ_index)
    print(champs)
    return champs[0]
    

  def close(self) -> None:
    self.db.close()
    
if __name__ == "__main__":
  conn: SQLConn = SQLliteConn("champ.db")
  
  c = ChampDB(conn)
  c.create_database()
  c.add_champion("test4")
  
  print(c.get_all_champions())
  print(c.count_champions())
      
  