from modules import data_utils
from modules import gui_utils
import tkinter as tk

def list_upper(list_):
      list_uppered = []
      for item in list_:
            list_uppered.append(item.upper())
      
      return list_uppered


def list_result_better_format(list_):
      new_list = []
      for item in list_:
            new_item = f"[{item}]"
            new_list.append(new_item)
      
      return new_list

class Cards():
      def __init__(self):
            self.cards_list = []
            self.cards_number = 0

cards = Cards()


def display_pokemon_card(
            pokemon_input_,
            pokemon_page_number,
            pokemon_search_total
          ):

            pokemon_input = pokemon_input_.lower()

      
            if pokemon_input in data_utils.names.databank:
                  pokemon = pokemon_input
                  pokemon = gui_utils.PokemonCard(pokemon, gui_utils.search_screen.frame_2)
                  
                  pokemon.class_pack()

                  cards.cards_list.append(pokemon)
                  cards.cards_number += 1
            

            elif pokemon_input in data_utils.types.databank:

                  pokemon_page_index = 0 + (pokemon_page_number-1)*7

                  for _ in range(7):
                              
                        if pokemon_page_index < pokemon_search_total:

                              pokemon = data_utils.types.databank[pokemon_input][pokemon_page_index]

                              pokemon = gui_utils.PokemonCard(pokemon, gui_utils.search_screen.frame_2)

                              pokemon.class_pack()

                              cards.cards_list.append(pokemon)
                              cards.cards_number += 1

                              pokemon_page_index += 1
            

            elif pokemon_input.isdigit():

                  pokemon = data_utils.ids.databank2[int(pokemon_input)]
                  pokemon = gui_utils.PokemonCard(pokemon, gui_utils.search_screen.frame_2)
                  
                  pokemon.class_pack()

                  cards.cards_list.append(pokemon)
                  cards.cards_number += 1

            else:
                  label = ErrorLabel()

                  cards.cards_list.append(label)


def clean_last_search():
      for pokemon in cards.cards_list:
            pokemon.class_pack_forget()
      cards.cards_list.clear()
      cards.cards_number = 0

class ErrorLabel():
      def __init__(self):
            self.label = tk.Label(gui_utils.search_screen.frame_2,text= f'Input not in databank\n[ERROR 404]', font=('Arial', 30, 'bold'))

            self.label.pack(pady=100)
      
      def class_pack_forget(self):
            self.label.destroy()



def display_all_pokemon(pokemon_page_number, pokemon_search_total):

      data_utils.create_id()

      pokemon_page_index = 0 + (pokemon_page_number-1)*7

      for _ in range(7):
                  
            if pokemon_page_index < pokemon_search_total:

                  pokemon = data_utils.ids.databank2[(pokemon_page_index+1)]

                  pokemon = gui_utils.PokemonCard(pokemon, gui_utils.search_screen.frame_2)

                  pokemon.class_pack()

                  cards.cards_list.append(pokemon)
                  cards.cards_number += 1

                  pokemon_page_index += 1