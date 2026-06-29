from pathlib import Path


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
