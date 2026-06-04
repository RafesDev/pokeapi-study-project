import requests
import json

def downloading_message(pokemon_number, pokemon_total, pokemon, last_length):

      message = f"[{pokemon_number}/{pokemon_total}] Getting data for {pokemon['name']}..."

      padding = " " * max(0, last_length - len(message))

      print(f"\r{message}{padding}", end="", flush=True)

      return message


pokemon_types_databank = {}

response = requests.get(
      'https://pokeapi.co/api/v2/pokemon'
      )
data = response.json()

pokemon_number = 0
pokemon_total = data['count']

last_length = 0

running = True

while running:

      for pokemon in data['results']:
            
            pokemon_number += 1

            message = downloading_message(pokemon_number, pokemon_total, pokemon, last_length)

            last_length = len(message)

            response = requests.get(pokemon['url'])
            pokemon_data = response.json()


            types = []
            for type in pokemon_data['types']:
                  types.append(type['type']['name'])

            pokemon_types_databank[pokemon['name']] = types

      if data['next'] != None:
            response = requests.get(data['next'])
            data = response.json()
      else:
            running = False
                  

print()
print("\nDone!")