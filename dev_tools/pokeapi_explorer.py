import requests
import pprint

response = requests.get(
      'https://pokeapi.co/api/v2/pokemon/4/'
      )
data = response.json()

### UI COMPONENTS:

## POKEMON NAME 
name = data['name'] # STRING


## POKEMON TYPES
types = data['types'] # DICTIONARIES LIST

# TYPE 1
type1 = types[0]['type']['name'] # STRING

# TYPE 2
type2 = types[1]['type']['name'] if len(types) > 1 else None # STRING


## POKEMON ID
id = data['id'] # STRING


## POKEMON MOVES
moves = data['moves'] # DICTIONARIES LIST
#pprint.pprint(moves) # FOR TESTING PURPOSES

repeat_times = len(moves)
repeat_times = 5 # FOR TESTING PURPOSES

for i in range(repeat_times):
      move_data = requests.get(moves[i]['move']['url']).json()
      #pprint.pprint(move_data) # FOR TESTING PURPOSES

      ## MOVE NAME
      move_name = moves[i]['move']['name'] # STRING

      ## MOVE LVL LEARNED
      lvl_learned = moves[i]['version_group_details'][0]['level_learned_at'] # INT
      
      ## MOVE TYPE
      move_type = move_data['type']['name'] # STRING
      
      ## MOVE ACCURACY
      move_accuracy = move_data['accuracy'] # INT

      ## MOVE POWER
      move_power = move_data['power'] # INT
      
      ## MOVE PP
      move_pp = move_data['pp'] # INT

      #print(f'Move Name: {move_name}, Level Learned: {lvl_learned}, Type: {move_type}, Accuracy: {move_accuracy}, Power: {move_power}, PP: {move_pp}') # FOR TESTING PURPOSES


## POKEMON STATS
stats = data['stats']
#pprint.pprint(stats) # FOR TESTING PURPOSES

stats_dict = {} # STATS DICTIONARY (KEY: STAT NAME, VALUE: STAT VALUE)

for stat in range(len(stats)):
      stat_value = stats[stat]['base_stat'] # INT
      stat_name = stats[stat]['stat']['name'] # STRING
      stats_dict[stat_name] = stat_value

# HP
# ATTACK
# DEFENSE
# SPECIAL ATTACK
# SPECIAL DEFENSE
# SPEED


## POKEMON IMAGE (FRONT PLUS BACK)
front = data['sprites']['front_default'] # PNG LINK
back = data['sprites']['back_default'] # PNG LINK

## POKEMON EVOLUTIONS

family = [] # POKEMON EVOLUTIONS LIST

species = requests.get(data['species']['url']).json()
evolution_chain = requests.get(species['evolution_chain']['url']).json()

def get_family(node):
      family.append(node['species']['name'])

      for child in node['evolves_to']:
            get_family(child)

get_family(evolution_chain['chain'])

## POKEMON DESCRIPTION
def get_description(data):
      request = (data['species']['url'])
      print(request)
      species = requests.get(request).json()
      
      for i in range(len(species['flavor_text_entries'])):
            if species['flavor_text_entries'][i]['language']['name'] == 'en':
                  return species['flavor_text_entries'][i]['flavor_text']  
                  
description = get_description(data) # DESCRIPTION STRING

def without_line_break(string_with_line_break):
      letter_list = []
      for letter in string_with_line_break:
            if letter.isspace():
                  letter_list.append(' ')
            else:
                  letter_list.append(str(letter))

      return ''.join(letter_list)

print(without_line_break(description))

import tkinter as tk

root = tk.Tk()

text_widget = tk.Text(root)

text_widget.insert('1.0', without_line_break(description))

text_widget.pack()

root.mainloop()