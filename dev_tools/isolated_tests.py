
from collections import defaultdict
import tkinter as tk
import requests

def types_fetcher(pokemon_url):

  response = requests.get(pokemon_url)
  pokemon_data = response.json()

  types = []
  for type in pokemon_data['types']:
        types.append(type['type']['name'])

  return types

def names_download_step():
  global names_download_progress
  global pokemon_total
  global data
  global text_tk
  global download_progress_msg

  if names_download_progress != pokemon_total:

    for pokemon in data['results']:

      pokemon_search_by_names_databank[pokemon['name']] = types_fetcher(pokemon['url'])

      names_download_progress += 1

      label.configure(text=f'[{(names_download_progress / pokemon_total)*100:.2f}%] Downloading...')

    next_step_controller()

    print(f'\r{pokemon_search_by_names_databank}', end="", flush=True)

    types = types_fetcher(pokemon["url"])

    if not types:
      print("Problema encontrado:")
      print("Nome:", pokemon["name"])
      print("URL:", pokemon["url"])

    root.after(1, names_download_step)


def next_step_controller():
   global data
   if data['next'] is not None:
    response = requests.get(data['next'])
    data = response.json()

pokemon_search_by_names_databank = {}
pokemon_search_by_types_databank = defaultdict(list)

response = requests.get(
'https://pokeapi.co/api/v2/pokemon'
)

data = response.json()


pokemon_total = data['count']

names_download_progress = 0
types_download_progress = 0

download_progress_msg = f'[{(names_download_progress / pokemon_total)*100:.2f}%] Downloading...'

root = tk.Tk()

label = tk.Label(root, text=download_progress_msg)
label.pack(pady=50)

root.after(1, names_download_step)

root.mainloop()

