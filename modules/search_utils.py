from modules import download_utils

def pokemon_answer_message(
            pokemon_input,
          ):
      
      if download_utils.names.need_download() or download_utils.types.need_download():
            return "[FATAL ERROR] cached data integrity violated!"
      
      else:
            if pokemon_input in download_utils.names.databank:
                  return f"{pokemon_input}'s type(s) is/are: {download_utils.names.databank[pokemon_input]}"
            
            elif pokemon_input in download_utils.types.databank:
                  return f"The following Pokémon are of type {pokemon_input}: {download_utils.types.databank[pokemon_input]}"
            
            else:
                  return f'[ERROR 404] "{pokemon_input}" data not found. '