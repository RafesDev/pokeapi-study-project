from pathlib import Path
import requests
import json
from pathlib import Path
from collections import defaultdict

class PokemonDownload():
      def __init__(self, name):
            self.file_path = download_vars.DATA_DIR / f"pokemon_{name}_databank.json"
            
            if name == "names":
                  self.databank = {}
            elif name == "types":
                  self.databank = defaultdict(list)
            elif name == "ids":
                  self.databank = {}
                  self.databank2 = {}

            self.name = name

            response = requests.get(
            'https://pokeapi.co/api/v2/pokemon'
            )

            self.data = response.json()


            if Path.exists(self.file_path) is False:
                  self.download_progress = 0
            else:
                  self.download_progress = download_vars.pokemon_total

            self.pokemon_index_in_page = 0

            self.already_downloaded_one = False

      def need_download(self):
            
            download_vars.download_status = "Download Status: Checking for cached data..."

            if Path.exists(self.file_path) is False:
                  download_vars.download_status = f"Download Status: <{self.name.upper()}> feature's data missing"
                  return True
            else:
                  return False
            
      def download_one(self):

            download_vars.download_status = f"Download Status: Downloading <{self.name.upper()}> data..."
            
            download_vars.download_progress_msg = f"[{(self.download_progress/download_vars.pokemon_total)*100:.2f}%] Downloading data..."

            ###* DEV TOOL
            #print(download_vars.download_progress_msg)

            if self.pokemon_index_in_page == 20:
                  self.pokemon_index_in_page = 0

            if self.name == "types":

                  pokemon = self.data['results'][self.pokemon_index_in_page]

                  for type in types_fetcher(pokemon['url']):
                        self.databank[type].append(pokemon['name'])

            elif self.name == "names":

                  pokemon = self.data['results'][self.pokemon_index_in_page]

                  self.databank[pokemon['name']] = types_fetcher(pokemon['url'])

            self.pokemon_index_in_page += 1
            self.download_progress += 1

            download_vars.download_status = f"Download Status: Downloading <{self.name.upper()}> data..."
            
            download_vars.download_progress_msg = f"[{(self.download_progress/download_vars.pokemon_total)*100:.2f}%] Downloading data..."

      def last_of_current_page(self):
            if self.pokemon_index_in_page >= len(self.data["results"]):
                  return True
            return False

      def save_downloaded_data(self):
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w") as file:
                  json.dump(self.databank, file, indent=4)

      def has_next_page(self):
            if self.data['next'] is not None:
                  return True
            return False
      
      def turn_next_page(self):
            self.data = requests.get(self.data['next']).json()

      def data_load(self):
            self.databank = json.load(open(self.file_path, "r"))
            download_vars.download_status = f"Download Status: Nothing to download"

      
def types_fetcher(pokemon_url):

      response = requests.get(pokemon_url)
      
      if response.status_code != 200:

            for _ in range(3):

                  response = requests.get(pokemon_url)

                  if response.status_code == 200:
                        break

            if response.status_code != 200:
                  return ['No data, API request failed']
            

      pokemon_data = response.json()

      types = []
      for type in pokemon_data['types']:
            types.append(type['type']['name'])

      return types

def create_id():
      i = 0
      for pokemon in names.databank:
            i += 1
            ids.databank[pokemon] = i
            ids.databank2[i] = pokemon


class DownloadState():
      def __init__(self):

            self.download_status = "Download Status: Initializating Download Protocol..."
            self.download_progress_msg = "[N/A]"

            self.BASE_DIR = Path(__file__).resolve().parent.parent
            self.DATA_DIR = self.BASE_DIR / "data" / "cache"

            response = requests.get(
            'https://pokeapi.co/api/v2/pokemon'
            )

            self.data = response.json()

            self.pokemon_total = self.data["count"]

download_vars = DownloadState()



names = PokemonDownload("names")
types = PokemonDownload("types")
ids = PokemonDownload("ids")