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

class DetailsVars():
      def __init__(self, pokemon_id):

            print(pokemon_id)

            response = requests.get(
                  f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
                  )
            
            self.data = response.json()

            ### UI COMPONENTS:

            ## POKEMON NAME 
            self.name = self.data['name'] # STRING


            ## POKEMON TYPES
            self.types = self.data['types'] # DICTIONARIES LIST

            # TYPE 1
            self.type1 = self.types[0]['type']['name'] # STRING

            # TYPE 2
            self.type2 = self.types[1]['type']['name'] if len(self.types) > 1 else None # STRING


            ## POKEMON ID
            self.id = self.data['id'] # STRING

            ## MOVES
            self.moves_number_max = len(self.data['moves'])

            self.move_number = 0

            self.actual_move = PokemonMove(self.data, self.move_number)

            ## POKEMON STATS
            self.stats = self.data['stats']
            #pprint.pprint(stats) # FOR TESTING PURPOSES

            self.stats_dict = {} # STATS DICTIONARY (KEY: STAT NAME, VALUE: STAT VALUE)

            for stat in range(len(self.stats)):
                  stat_value = self.stats[stat]['base_stat'] # INT
                  stat_name = self.stats[stat]['stat']['name'] # STRING
                  self.stats_dict[stat_name] = stat_value

            # HP
            # ATTACK
            # DEFENSE
            # SPECIAL ATTACK
            # SPECIAL DEFENSE
            # SPEED


            ## POKEMON IMAGE (FRONT PLUS BACK)
            self.front = self.data['sprites']['front_default'] # PNG LINK
            self.back = self.data['sprites']['back_default'] # PNG LINK

            ## POKEMON EVOLUTIONS

            self.family = [] # POKEMON EVOLUTIONS LIST

            species = requests.get(self.data['species']['url']).json()
            evolution_chain = requests.get(species['evolution_chain']['url']).json()


            get_family(evolution_chain['chain'], self.family)

            ## POKEMON DESCRIPTION
            
            self.description = get_description(self.data) # DESCRIPTION STRING

      def next_move(self):
            if self.move_number < self.moves_number_max-1:
                  self.move_number += 1
                  self.actual_move = PokemonMove(self.data, self.move_number)
            else:
                  pass

      def previous_move(self):
            if self.move_number > 0:
                  self.move_number -= 1
                  self.actual_move = PokemonMove(self.data, self.move_number)
            else:
                  pass

class PokemonMove():
      def __init__(self, data, move_index):
            ## POKEMON MOVES
            self.moves = data['moves'] # DICTIONARIES LIST
            
            move_data = requests.get(self.moves[move_index]['move']['url']).json()

            ## MOVE NAME
            self.move_name = self.moves[move_index]['move']['name'] # STRING

            ## MOVE LVL LEARNED
            self.lvl_learned = self.moves[move_index]['version_group_details'][0]['level_learned_at'] # INT

            ## MOVE TYPE
            self.move_type = move_data['type']['name'] # STRING

            ## MOVE ACCURACY
            self.move_accuracy = move_data['accuracy'] # INT

            ## MOVE POWER
            self.move_power = move_data['power'] # INT

            ## MOVE PP
            self.move_pp = move_data['pp'] # INT

def get_family(node, family):
      family.append(node['species']['name'])

      for child in node['evolves_to']:
            get_family(child, family)

def get_description(data):
                  species = requests.get(data['species']['url']).json()
                  
                  for i in range(len(species['flavor_text_entries'])):
                        if species['flavor_text_entries'][i]['language']['name'] == 'en':
                              return species['flavor_text_entries'][i]['flavor_text']  
                        


names = PokemonDownload("names")
types = PokemonDownload("types")
ids = PokemonDownload("ids")