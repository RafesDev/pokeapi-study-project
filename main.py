#* Imports:

#import extern libraries:
import requests
import json
from pathlib import Path
from collections import defaultdict
import tkinter as tk

#import modules:
from modules.terminal_messages import (
      downloading_message,
      pokemon_answer_message,
      download_complete_msg,
      data_missing_msg
)
from modules.pokeapi_utils import (
      types_fetcher
)
from modules.json_utils import (
      dict_to_json
)
from modules.backend_logic import (
      should_download_data
)
from modules.tkinter_utils import (
      clean_event,
      label_info_updater,
      data_verifier
)

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

pokemon_total = data['count']

names_download_progress = pokemon_total
types_download_progress = pokemon_total

# boolean:
running = True
starting_message_already_printed = False
data_already_loaded = False
window_already_activated = False

#* Main loop:
print("\nChecking for cached data")

if Path.exists(pokemon_search_by_names_file) is False:
      names_download_progress = 0

if Path.exists(pokemon_search_by_types_file) is False:
      types_download_progress = 0

while running:
            
      if should_download_data(names_download_progress, types_download_progress, pokemon_total) is True:

            response = requests.get(
            'https://pokeapi.co/api/v2/pokemon'
            )

            data = response.json()

      if Path.exists(pokemon_search_by_names_file) is False or names_download_progress == 0:

            if names_download_progress == 0:
                  print(data_missing_msg("search by name feature"))

            for pokemon in data['results']:
                  
                  names_download_progress += 1

                  message = downloading_message(names_download_progress, pokemon_total)

                  padding = " " * max(0, last_length - len(message))

                  print(f"\r{message}{padding}", end="", flush=True)

                  last_length = len(message)

                  pokemon_search_by_names_databank[pokemon['name']] = types_fetcher(pokemon['url'])

                   

            if data['next'] is not None:
                  response = requests.get(data['next'])
                  data = response.json()
            else:
                  dict_to_json(
                        pokemon_search_by_names_databank, 
                        pokemon_search_by_names_file
                  )

                  print(download_complete_msg("search by name feature"))

      elif Path.exists(pokemon_search_by_types_file) is False or types_download_progress == 0:

            if types_download_progress == 0:

                  print(data_missing_msg("search by type feature"))

            for pokemon in data['results']:
                  
                  types_download_progress += 1

                  message = downloading_message(types_download_progress, pokemon_total)

                  padding = " " * max(0, last_length - len(message))

                  print(f"\r{message}{padding}", end="", flush=True)

                  last_length = len(message)


                  for type in types_fetcher(pokemon['url']):
                              pokemon_search_by_types_databank[type].append(pokemon['name'])
                              
            if data['next'] is not None:
                  response = requests.get(data['next'])
                  data = response.json()
            else:

                  dict_to_json(
                        pokemon_search_by_types_databank, 
                        pokemon_search_by_types_file
                  )

                  print(download_complete_msg("search by type feature"))
      else:
            if data_already_loaded is False:

                  print('\nCached data found. Loading...')
                  
                  pokemon_search_by_names_databank = json.load(open(pokemon_search_by_names_file, "r"))
                  pokemon_search_by_types_databank = json.load(open(pokemon_search_by_types_file, "r"))
                  
                  data_already_loaded = True

                  print('\nLoading complete!')

            if starting_message_already_printed is False:
                  print('\nStarting the program...')
                  print('\nWELCOME TO POKEAPI-STUDY-PROJECT!')
                  print()
                  starting_message_already_printed = True

            root = tk.Tk()

            frame = tk.Frame(root)
            frame.pack(pady=10)

            entry = tk.Entry(
                  frame,
                  width=50
            )

            label = tk.Label(
                  root,
                  text=""
            )


            placeholder = "Enter a pokemon name or type"

            entry.insert(0, placeholder)

            entry.bind("<FocusIn>",lambda event: clean_event(event, entry, placeholder))

            button = tk.Button(
                  frame,
                  text="Search",
                  command=lambda: (
                        label_info_updater(
                              entry, 
                              label, 
                              pokemon_search_by_names_databank,
                              pokemon_search_by_types_databank,
                              pokemon_search_by_names_file,
                              pokemon_search_by_types_file
), 
                        data_verifier(
                              pokemon_search_by_names_file,
                              pokemon_search_by_types_file

)))

            entry.pack(pady=5, padx=5, side='left')
            button.pack(pady=5, side='left') 
            label.pack(pady=40)

   
            if window_already_activated == False:
                  window_already_activated = True
                  root.mainloop()
            else:
                  running = False
          