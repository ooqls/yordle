import sqlite3

class SQLliteTransaction:
  cursor: sqlite3.Cursor
  conn: sqlite3.Connection
  
  def __init__(self, con: sqlite3.Connection, cursor: sqlite3.Cursor):
    self.cursor = cursor
    self.conn = con
    
  def execute(self, stmt: str, params: list[any] = []) -> None:
    self.cursor.execute(stmt, params)
  
  def executemany(self, stmt: str, params: list[list[any]] = []) -> None:
    self.cursor.executemany(stmt, params)
  
  def fetchall(self) -> list[any]:
    res = self.cursor.fetchall()
    return res

  def fetchone(self) -> list[any]:
    res = self.cursor.fetchone()
    return res
  
  def commit(self):
    self.conn.commit()
  
  def close(self):
    self.cursor.close()
  

class SQLliteConn:
  conn: sqlite3.Connection
  
  def __init__(self, db_path: str):
    self.db_path = db_path
    self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
  
  def transaction(self) -> SQLliteTransaction:
    c = self.conn.cursor()
    return SQLliteTransaction(self.conn, c)
  
  def close(self) -> None:
    self.conn.close()


