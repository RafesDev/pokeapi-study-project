import tkinter as tk
from pathlib import Path
from modules.terminal_messages import (
    pokemon_answer_message
)

def clean_event(event,entry, placeholder):
  if entry.get() == placeholder:
    entry.delete(0, tk.END)

def label_info_updater(
                entry, 
                label, 
                pokemon_search_by_names_databank,
                pokemon_search_by_types_databank,
                pokemon_search_by_names_file,
                pokemon_search_by_types_file
):
  pokemon_input = entry.get().lower()
  label.config(text=(pokemon_answer_message(
    pokemon_input,
    pokemon_search_by_names_databank,
    pokemon_search_by_types_databank,
    pokemon_search_by_names_file,
    pokemon_search_by_types_file
  )))

def data_verifier(
        pokemon_search_by_names_file,
        pokemon_search_by_types_file
):
  if Path.exists(pokemon_search_by_names_file) is False:
        global names_download_progress
        names_download_progress = 0
        

  if Path.exists(pokemon_search_by_types_file) is False:
        global types_download_progress
        types_download_progress = 0

  if names_download_progress == 0 or types_download_progress == 0:
        global root
        root.destroy()
        global window_already_activated
        window_already_activated = False
                        
