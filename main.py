import requests
import json
from pathlib import Path

#* Functions:

# Prints the downloading message, with a progress bar and padding to overwrite the previous message.
def downloading_message(pokemon_number, pokemon_total, last_length):

      message = f"[{pokemon_number}/{pokemon_total}] Downloading Pokémon data from PokeAPI..."

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

databank_file = DATA_DIR / "pokemon_types_databank.json"

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

print("Checking for cached data...")

if Path.exists(databank_file) == False:
      print("\nNo cached data found. Starting download...")
      print()
else:
      print('\nCached data found. Loading...')
      print('\nLoading complete!')
      print('\nStarting the program...')
      print()

while running:

      if Path.exists(databank_file) == False:

            for pokemon in data['results']:
                  
                  pokemon_number += 1

                  message = downloading_message(pokemon_number, pokemon_total, last_length)

                  last_length = len(message)

                  pokemon_types_databank[pokemon['name']] = types_fetcher(pokemon['url'])

            if data['next'] != None:
                  response = requests.get(data['next'])
                  data = response.json()
            else:
                  DATA_DIR.mkdir(parents=True, exist_ok=True)

                  json.dump(pokemon_types_databank, open(DATA_DIR / "pokemon_types_databank.json", "w"), indent=4)

                  print()
                  print("\nDownload complete!")
                  print("\nChecking for cached data...")
                  print('\nCached data found. Loading...')
                  print('\nLoading complete!')
                  print('\nStarting the program...')
                  print()
      else:
            

            pokemon_types_databank = json.load(open(databank_file, "r"))

            pokemon_input = input('Enter a Pokémon name or type "exit" to quit >>> ').lower()

            if pokemon_input in pokemon_types_databank:
                  print(f"{pokemon_input}'s type(s) is/are: {pokemon_types_databank[pokemon_input]}")
                  print()

            elif pokemon_input == "exit":
                  print("Exiting the program...")
                  running = False
                  print()

            else:
                  print(f'"{pokemon_input}" is not in the databank. ')
                  print()