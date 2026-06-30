#* Imports:

#import extern libraries:
import requests
import json
from pathlib import Path
from collections import defaultdict
import tkinter as tk

#import modules:
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
def download_types(data):
      global types_download_progress

      for pokemon in data['results']:

            for type in types_fetcher(pokemon['url']):
                  pokemon_search_by_types_databank[type].append(pokemon['name'])
                  
            types_download_progress += 1

def download_names(data):
      global names_download_progress

      for pokemon in data['results']:

            pokemon_search_by_names_databank[pokemon['name']] = types_fetcher(pokemon['url'])

            names_download_progress += 1
      

def next_step_controller(data, feature):
      if data['next'] is not None:
            response = requests.get(data['next'])
            data = response.json()

            return data
            
      else:
            if feature == "types":
                  dict_to_json(
                        pokemon_search_by_types_databank, 
                        pokemon_search_by_types_file
                  )

                  msg = f"<SEARCH BY TYPES> data's feature download complete!"

                  print(f'\n{msg}')
                  
            elif feature == "names":
                  dict_to_json(
                        pokemon_search_by_names_databank, 
                        pokemon_search_by_names_file
                  )

                  msg = "<SEARCH BY NAMES> data's feature download complete!"

                  print(f'\n{msg}')

            return

def download_step():
      
      if Path.exists(pokemon_search_by_names_file) is False:
            global names_data

            download_names(names_data)

            download_progress_msg = f"[{(names_download_progress/pokemon_total)*100:.2f}%] Downloading <SEARCH BY NAMES> feature's data..."

            print(download_progress_msg)

            names_data = next_step_controller(names_data, "names")

      elif Path.exists(pokemon_search_by_types_file) is False:
            global types_data

            download_types(types_data)

            download_progress_msg = f"[{(types_download_progress/pokemon_total)*100:.2f}%] Downloading <SEARCH BY TYPES> feature's data..."

            print(download_progress_msg)
            
            types_data = next_step_controller(types_data, "types")

      else:
            global data_already_downloaded
            data_already_downloaded = True
            return data_already_downloaded

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
data_already_downloaded = False
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

            response = requests.get(
            'https://pokeapi.co/api/v2/pokemon'
            )

            names_data = response.json()

            response = requests.get(
            'https://pokeapi.co/api/v2/pokemon'
            )

            types_data = response.json()

      download_step()

      if data_already_downloaded:

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

            text_tk = tk.Text(root)


            placeholder = "Enter a pokemon name or type"

            entry.insert(0, placeholder)

            entry.bind("<FocusIn>",lambda event: clean_event(event, entry, placeholder))

            button = tk.Button(
                  frame,
                  text="Search",
                  command=lambda: (
                        label_info_updater(
                              entry, 
                              text_tk, 
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
            text_tk.pack(pady=40)

   
            if window_already_activated == False:
                  window_already_activated = True
                  root.mainloop()
            else:
                  running = False
          