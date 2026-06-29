import requests

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