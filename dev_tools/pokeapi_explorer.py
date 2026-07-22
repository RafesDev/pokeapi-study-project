import requests

response = requests.get(
      'https://pokeapi.co/api/v2/pokemon/20/'
      )
data = response.json()

print(data["id"])