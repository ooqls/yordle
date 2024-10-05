
class SQLTransaction:
  def execute(self, stmt: str, params: list[any]) -> None:
    pass
  def executemany(self, stmt: str, params: list[list[any]]) -> None:
    pass
  def commit(self) -> None:
    pass
  def close(self) -> None:
    pass
  def fetchall() -> list[any]:
    pass
  def fetchone() -> list[any]:
    pass

class SQLConn:
  def transaction(self) -> SQLTransaction:
    pass
  def close(self) -> None:
    pass


  
class SQLFactory:
  def new_conn() -> SQLConn:
    pass
  
