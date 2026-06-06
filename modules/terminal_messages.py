from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "cache"

pokemon_search_by_names_file = DATA_DIR / "pokemon_names_databank.json"
pokemon_search_by_types_file = DATA_DIR / "pokemon_types_databank.json"


# Prints the downloading message, with a progress bar and padding to overwrite the previous message.
def downloading_message(pokemon_number, pokemon_total, last_length):

      message = (f"[{(pokemon_number / pokemon_total) * 100:.2f}%] Downloading Pokémon data from PokeAPI...")

      padding = " " * max(0, last_length - len(message))

      print(f"\r{message}{padding}", end="", flush=True)

      return message

def starting_message():

      print('\nCached data found. Loading...')
      print('\nLoading complete!')
      print('\nStarting the program...')
      print('\nWELCOME TO POKEAPI-STUDY-PROJECT!')
      print()

def pokemon_answer_message(
            pokemon_input,
            pokemon_names_databank, 
            pokemon_types_databank,pokemon_search_by_names_file,
            pokemon_search_by_types_file):
      
      if Path.exists(pokemon_search_by_names_file) == True and Path.exists(pokemon_search_by_types_file) == True:

            if pokemon_input in pokemon_names_databank:
                  return f"{pokemon_input}'s type(s) is/are: {pokemon_names_databank[pokemon_input]}"
            
            elif pokemon_input in pokemon_types_databank:
                  return f"The following Pokémon are of type {pokemon_input}: {pokemon_types_databank[pokemon_input]}"
            
            elif pokemon_input == "exit":
                  return "Exiting the program..."
            
            else:
                  return f'[ERROR 404] "{pokemon_input}" data not found. '
            
      else:
            return "[FATAL ERROR] cached data integrity violated!"

def download_complete_msg(feature):
      print(f"\n[{feature}]'s data download complete!")
      print("\nChecking for cached data...")

def data_missing_msg(feature):      
      print(f"[{feature}]'s data missing, starting download.")