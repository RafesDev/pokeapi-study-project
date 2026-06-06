import requests
import json
from pathlib import Path
from modules.terminal_messages import (
      downloading_message,
      starting_message,
      pokemon_answer_message,
      download_complete_msg,
      data_missing_msg
)
from modules.pokeapi_utils import types_fetcher
from modules.json_utils import dict_to_json
from collections import defaultdict

#* Functions:

#* Dicts:

pokemon_search_by_names_databank = {}
pokemon_search_by_types_databank = defaultdict(list)

#* Variables:

response = requests.get(
            'https://pokeapi.co/api/v2/pokemon'
            )

data = response.json()


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "cache"

pokemon_search_by_names_file = DATA_DIR / "pokemon_names_databank.json"
pokemon_search_by_types_file = DATA_DIR / "pokemon_types_databank.json"

last_length = 0

running = True

starting_message_alredy_printed = False

pokemon_total = data['count']

names_download_progress = pokemon_total
types_download_progress = pokemon_total

#* Main loop:
print("\nStarting data verification.")
print("\nChecking for cached data")

if Path.exists(pokemon_search_by_names_file) == False:
      names_download_progress = 0

if Path.exists(pokemon_search_by_types_file) == False:
      types_download_progress = 0

while running:
            
      if names_download_progress == 0 and types_download_progress == 0 or names_download_progress == pokemon_total and types_download_progress == 0 or names_download_progress == 0 and types_download_progress == pokemon_total:

            response = requests.get(
            'https://pokeapi.co/api/v2/pokemon'
            )

            data = response.json()

      if Path.exists(pokemon_search_by_names_file) == False or names_download_progress == 0:

            if names_download_progress == 0:
                  data_missing_msg("search by name feature")

            for pokemon in data['results']:
                  
                  names_download_progress += 1

                  message = downloading_message(names_download_progress, pokemon_total, last_length)

                  last_length = len(message)

                  pokemon_search_by_names_databank[pokemon['name']] = types_fetcher(pokemon['url'])

                   

            if data['next'] != None:
                  response = requests.get(data['next'])
                  data = response.json()
            else:
                  dict_to_json(
                        pokemon_search_by_names_databank, 
                        pokemon_search_by_names_file
                  )

                  download_complete_msg("search by name feature")

      elif Path.exists(pokemon_search_by_types_file) == False or types_download_progress == 0:

            if types_download_progress == 0:

                  data_missing_msg("search by type feature")

            for pokemon in data['results']:
                  
                  types_download_progress += 1

                  message = downloading_message(types_download_progress, pokemon_total, last_length)

                  last_length = len(message)


                  for type in types_fetcher(pokemon['url']):
                              pokemon_search_by_types_databank[type].append(pokemon['name'])
                              
            if data['next'] != None:
                  response = requests.get(data['next'])
                  data = response.json()
            else:

                  dict_to_json(
                        pokemon_search_by_types_databank, 
                        pokemon_search_by_types_file
                  )

                  download_complete_msg("search by type feature")
      else:
            if starting_message_alredy_printed == False:
                  starting_message()
                  starting_message_alredy_printed = True

            pokemon_search_by_names_databank = json.load(open(pokemon_search_by_names_file, "r"))
            pokemon_search_by_types_databank = json.load(open(pokemon_search_by_types_file, "r"))

            pokemon_input = input('Enter a Pokémon name or type. If you want to quit the program, type "exit" >>> ').lower()

            print(pokemon_answer_message(
                  pokemon_input,
                  pokemon_search_by_names_databank,
                  pokemon_search_by_types_databank,
                  pokemon_search_by_names_file,
                  pokemon_search_by_types_file
            ))

            if Path.exists(pokemon_search_by_names_file) == False:
                  names_download_progress = 0

            if Path.exists(pokemon_search_by_types_file) == False:
                  types_download_progress = 0

            print()

            if pokemon_input == "exit":
                  running = False