from email import utils

import requests
import json
from pathlib import Path
from modules.terminal_messages import (
      downloading_message,
      starting_message,
      pokemon_answer_message,
      show_cache_status
)
from modules.pokeapi_utils import types_fetcher
from modules.json_utils import dict_to_json

#* Functions:

#* Dicts:

pokemon_types_databank = {}

#* Variables:

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "cache"

databank_file = DATA_DIR / "pokemon_types_databank.json"

response = requests.get(
      'https://pokeapi.co/api/v2/pokemon'
      )
data = response.json()

pokemon_number = 0
pokemon_total = data['count']

last_length = 0

running = True

#* Main loop:

show_cache_status(databank_file)

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
                  dict_to_json(
                        pokemon_types_databank, 
                        databank_file
                  )

                  print()
                  print("\nDownload complete!")
                  print("\nChecking for cached data...")
                  starting_message()
      else:
            

            pokemon_types_databank = json.load(open(databank_file, "r"))

            pokemon_input = input('Enter a Pokémon name or type "exit" to quit >>> ').lower()

            print(pokemon_answer_message(
                  pokemon_input,
                  pokemon_types_databank
            ))
            print()

            if pokemon_input == "exit":
                  running = False