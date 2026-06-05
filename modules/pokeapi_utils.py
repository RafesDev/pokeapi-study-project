import requests

def types_fetcher(pokemon_url):

      response = requests.get(pokemon_url)
      pokemon_data = response.json()

      types = []
      for type in pokemon_data['types']:
            types.append(type['type']['name'])

      return types