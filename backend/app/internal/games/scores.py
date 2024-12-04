class Score:
  def __init__(self):
    self.score = 0
    self.multiplier = 1
  
  def add_multiplier(self, m: int):
    self.multiplier = max(self.multiplier+m, 1)
  
  def reset_multiplier(self):
    self.multiplier = 1
  
  def get_score(self) -> int:
    return self.score

  def add_score(self, pts: int):
    self.score = max(0, self.score + (pts * self.multiplier))
  
  def subtract_score(self, pts: int):
    self.score = max(0, self.score - pts)
  