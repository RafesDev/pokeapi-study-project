import requests

response = requests.get(
      'https://pokeapi.co/api/v2/pokemon'
      )
data = response.json()

print(data["results"][20])