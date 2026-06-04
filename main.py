import requests
import json
from pathlib import Path

#* Functions:

# Prints the downloading message, with a progress bar and padding to overwrite the previous message.
def downloading_message(pokemon_number, pokemon_total, pokemon, last_length):

      message = f"[{pokemon_number}/{pokemon_total}] Downloading {pokemon['name']}'s data..."

      padding = " " * max(0, last_length - len(message))

      print(f"\r{message}{padding}", end="", flush=True)

      return message

def types_fetcher(pokemon_url):

      response = requests.get(pokemon_url)
      pokemon_data = response.json()

      types = []
      for type in pokemon_data['types']:
            types.append(type['type']['name'])

      return types

#* Dicts:

pokemon_types_databank = {}

#* Variables:

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "cache"

response = requests.get(
      'https://pokeapi.co/api/v2/pokemon'
      )
data = response.json()

pokemon_number = 0
pokemon_total = data['count']

last_length = 0

running = True

#* Main loop:

while running:

      if Path.exists(DATA_DIR / "pokemon_types_databank.json") == False:

            for pokemon in data['results']:
                  
                  pokemon_number += 1

                  message = downloading_message(pokemon_number, pokemon_total, pokemon, last_length)

                  last_length = len(message)

                  pokemon_types_databank[pokemon['name']] = types_fetcher(pokemon['url'])

            if data['next'] != None:
                  response = requests.get(data['next'])
                  data = response.json()
            else:
                  DATA_DIR.mkdir(parents=True, exist_ok=True)

                  json.dump(pokemon_types_databank, open(DATA_DIR / "pokemon_types_databank.json", "w"), indent=4)

                  print()
                  print("\nDone!")
      else:
            print("Data already exists. Loading from file...")
            running = False