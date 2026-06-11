
def should_download_data(names_download_progress, types_download_progress, pokemon_total):

  condition_01 = names_download_progress == 0 and types_download_progress == 0

  condition_02 = names_download_progress == pokemon_total and types_download_progress == 0

  condition_03 = names_download_progress == 0 and types_download_progress == pokemon_total

  download_requirements = condition_01 or condition_02 or condition_03

  return download_requirements
