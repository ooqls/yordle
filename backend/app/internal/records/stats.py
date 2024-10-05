from sql import SQLConn
from sqllite import SQLliteConn
import json

class GameStat:
  player_id: int = 0
  start_time: str = ""
  end_time: str = ""
  num_of_guesses: int = 0
  guesses: list[str] = []
  won: bool = False
  
  def __init__(self, player_id: int, start_time: str, end_time: str, num_of_guesses: int, guesses: list[str], won: bool):
    self.player_id = player_id
    self.start_time = start_time
    self.end_time = end_time
    self.num_of_guesses = num_of_guesses
    self.guesses = guesses
    self.won = won
  
  def get_sql_tuple(self) -> tuple:
    return (self.player_id, self.start_time, self.end_time, self.num_of_guesses, json.dumps(self.guesses), self.won)
    
    
class PlayerStat:
  number_of_games: int = 0
  wins: int = 0
  losses: int = 0
  
  win_rate: float = 0.0

  def __init__(self, id: int, number_of_games: int, wins: int, losses: int, win_rate: float):
    self.id = id
    self.number_of_games = number_of_games
    self.wins = wins
    self.losses = losses
    self.win_rate = win_rate
    
  def update_stats(self, game: GameStat):
    self.number_of_games += 1
    if game.won:
      self.wins += 1
    else:
      self.losses += 1
    self.win_rate = self.wins / self.number_of_games
  
  def get_sql_tuple(self) -> tuple:
    return (self.id, self.number_of_games, self.wins, self.losses, self.win_rate)

class StatsDB:
  conn: SQLConn
  def __init__(self, conn: SQLConn):
    self.conn = conn
        
  def create_db(self):
    tx = self.conn.transaction()
    tx.execute("CREATE TABLE IF NOT EXISTS games (player_id INTEGER, start_time TEXT, end_time TEXT, num_of_guesses INTEGER, guesses TEXT, won BOOLEAN)")
    tx.execute("CREATE INDEX IF NOT EXISTS player_id_index ON games (player_id)")
    tx.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, number_of_games INTEGER, wins INTEGER, losses INTEGER, win_rate REAL)")
    tx.commit()
    tx.close()

  def get_stats(self) -> dict[str, PlayerStat]:
    tx = self.conn.transaction()
    tx.execute("SELECT * FROM players")
    stats = tx.fetchall()
    all_stats = dict()
    
    for stat in stats:
        all_stats[stat[0]] = PlayerStat(stat[0], stat[1], stat[2], stat[3], stat[4])
    tx.close()
    return all_stats
    
  def get_stat(self, id: int) -> PlayerStat:
    tx = self.conn.transaction()
    tx.execute("SELECT * FROM players WHERE id = ?", (id,))
    stat = tx.fetchone()
    tx.close()
    if stat is None:
        return None
    else:
      return PlayerStat(stat[0], stat[1], stat[2], stat[3], stat[4])

  def add_stat(self, id: str, stat: GameStat):
    player: PlayerStat = self.get_stat(id)
    if player is None:
        player = PlayerStat(id, 0, 0, 0, 0.0)
    
    player.update_stats(stat)
    
    tx = self.conn.transaction()
    tx.execute("INSERT INTO games(player_id, start_time, end_time, num_of_guesses, guesses, won) VALUES (?, ?, ?, ?, ?, ?)", stat.get_sql_tuple())
    tx.execute("INSERT OR REPLACE INTO players (id, number_of_games, wins, losses, win_rate) VALUES (?, ?, ?, ?, ?)", player.get_sql_tuple())
    tx.commit()
    tx.close()
      
if __name__ == "__main__":
  c = SQLliteConn("stats.db")
  s = StatsDB(c)
  s.create_db()
  s.add_stat(1, GameStat(1, "", "", 1, [], True))
  stats = s.get_stats()
  print(stats)