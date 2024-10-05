from riotwatcher import LolWatcher, ApiError
import sys
import json

lol: LolWatcher = None
def init(api_key: str):
  global lol
  lol = LolWatcher(api_key)

def get_heros() -> list[str]:
  heros = {}
  with open("heros.json", "r") as f:
    heros = json.load(f)
  hero_dict = heros['data']
  
  return [k for k in hero_dict.keys()]
  

def get_updated_heros() -> list[str]:
  heros = []
  my_region = 'na1'
  try:
    versions = lol.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']
    heros = lol.data_dragon.champions(champions_version)
    
    # print(heros)
  except ApiError as e:
    print(e)
    sys.exit(1)
  
  return heros


if __name__ == "__main__":
  init(sys.argv[1])
  heros = get_updated_heros()
  with open("heros.json", "w") as f:
    json.dump(heros, f)
  print(heros)