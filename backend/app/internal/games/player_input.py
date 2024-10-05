class PlayerInput:
  action: str = ""
  data: any
  
  def __init__(self, action: str, data: any):
    self.action = action
    self.data = data
  
  def get_action(self) -> str:
    return self.action

  def get_data(self) -> any:
    return self.data