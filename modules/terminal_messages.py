from pathlib import Path
import json

# Prints the downloading message, with a progress bar and padding to overwrite the previous message.
def downloading_message(pokemon_number, pokemon_total, last_length):

      message = f"[{pokemon_number}/{pokemon_total}] Downloading Pokémon data from PokeAPI..."

      padding = " " * max(0, last_length - len(message))

      print(f"\r{message}{padding}", end="", flush=True)

      return message

def starting_message():

      print('\nCached data found. Loading...')
      print('\nLoading complete!')
      print('\nStarting the program...')
      print()

def pokemon_answer_message(pokemon_input, pokemon_types_databank):
      if pokemon_input in pokemon_types_databank:
            return f"{pokemon_input}'s type(s) is/are: {pokemon_types_databank[pokemon_input]}"
      
      elif pokemon_input == "exit":
            return "Exiting the program..."
      
      else:
            return f'"{pokemon_input}" is not in the databank. '
      
def show_cache_status(databank_file):
      print("Checking for cached data...")

      if Path.exists(databank_file) == False:
            print("\nNo cached data found. Starting download...")
            print()
      else:
            starting_message()