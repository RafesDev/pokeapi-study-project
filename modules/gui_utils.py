#POKEAPI-STUDY-PROJECT/modules/gui_utils.py
import tkinter as tk
from PIL import Image, ImageTk

from modules import (
  data_utils,
  search_utils,
  details_screen_utils
)

download_screen = None
search_screen = None
details_screen = None
entry = None
placeholder = None
frame_switch_vars = None
root = None

class ProgramFrame():
      def __init__(self, name, parent):

            self.name = name

            self.root = tk.Frame(parent)

            self.frame_status = tk.Frame(self.root)
      
            self.frame_1 = tk.Frame(self.root)

            self.frame_2 = tk.Frame(self.root)

            self.frame_3 = tk.Frame(self.root)

            self.download_status_label = tk.Label(
                  self.frame_status,
                  text=data_utils.download_vars.download_status)

            self.progress_label = tk.Label(
                  self.frame_1,
                  text=data_utils.download_vars.download_progress_msg)

            self.entry = tk.Entry(
                  self.frame_1,
                  width=50
            )

            self.button_got_clicked = False

            self.page_number = 1

            self.previus_button = tk.Button(self.frame_3, text='<', font=('Arial', 20, 'bold'), command= lambda:self.page_controller('previus'), cursor='hand2')

            self.page_number_label = tk.Label(self.frame_3, text=f'Page: {self.page_number}', font=('Arial', 20, 'bold'), bd=2, relief="raised")

            self.next_button = tk.Button(self.frame_3, text='>', font=('Arial', 20, 'bold'), command= lambda:self.page_controller('next'), cursor='hand2')

            self.placeholder = "Enter a pokemon NAME, TYPE or INDEX"

            self.entry.insert(0, self.placeholder)

            self.entry.bind("<FocusIn>",lambda event: clean_event(event, self.entry, self.placeholder))

            self.button = tk.Button(
                  self.frame_1,
                  text="SEARCH",
                  command= self.search_command,
                  cursor='hand2'
)
            
            self.entry.bind("<Return>", self.search_command)

            self.pokemon_search_total = 0

            self.max_page = 1

            self.home_button = tk.Button(self.frame_1, text='HOME', command= self.home, cursor='hand2')

      def search_command(self, event=None):
            self.search_with_page_reset()
            self.button_click_detector()

      def button_click_detector(self):
            self.button_got_clicked = True

      def search_with_page_reset(self, event=None):
            self.page_number = 1
            self.page_number_label.config(text=f'Page: {self.page_number}/{self.max_page}')
            self.search()


      def search(self, event=None):
            if data_utils.ids.databank == {}:
                  data_utils.create_id()


            self.pokemon_search_total = 0
            self.max_page = 1
            if self.entry.get().lower() in data_utils.types.databank:

                  for _ in data_utils.types.databank[self.entry.get().lower()]:

                        self.pokemon_search_total += 1

                  if int(self.pokemon_search_total/7) != self.pokemon_search_total/7:
                        self.max_page = int(self.pokemon_search_total/7) + 1
                  else:
                        self.max_page = int(self.pokemon_search_total/7)

            self.page_number_label.config(text=f'Page: {self.page_number}/{self.max_page}')

            search_utils.clean_last_search()

            search_utils.display_pokemon_card(self.entry.get().lower(), self.page_number, self.pokemon_search_total)

            self.page_controller_widgets_pack()

      def home(self, event=None):
            
            if data_utils.ids.databank == {}:
                  data_utils.create_id()


            self.pokemon_search_total = 0
            self.button_got_clicked = False
            self.max_page = 1
      

            for _ in range(data_utils.download_vars.pokemon_total):

                  self.pokemon_search_total += 1

            if int(self.pokemon_search_total/7) != self.pokemon_search_total/7:
                  self.max_page = int(self.pokemon_search_total/7) + 1
            else:
                  self.max_page = int(self.pokemon_search_total/7)

            self.page_number_label.config(text=f'Page: {self.page_number}/{self.max_page}')

            search_utils.clean_last_search()

            search_utils.display_all_pokemon(self.page_number, self.pokemon_search_total)

            self.page_controller_widgets_pack()


      def page_controller(self, direction):
            if direction == 'next':

                  self.page_number += 1


            elif direction == 'previus':

                  self.page_number -= 1

            self.page_number_label.config(text=f'Page: {self.page_number}/{self.max_page}')

            if self.button_got_clicked:
                  self.search()

            else:
                  self.home()

            self.page_controller_widgets_pack()



      def page_controller_widgets_pack(self):
            if self.max_page > 1:

                  if self.page_number == 1:

                        self.previus_button.pack_forget()
                        self.page_number_label.pack_forget()
                        self.next_button.pack_forget()

                        self.page_number_label.pack(padx=4, side='left')

                        self.next_button.pack(padx=2, side='left')


                  elif self.page_number == self.max_page:

                        self.previus_button.pack_forget()
                        self.page_number_label.pack_forget()
                        self.next_button.pack_forget()


                        self.previus_button.pack(padx=2, side='left')

                        self.page_number_label.pack(padx=4, side='left')


                  else:
                        self.previus_button.pack_forget()
                        self.page_number_label.pack_forget()
                        self.next_button.pack_forget()

                        self.previus_button.pack(padx=2, side='left')

                        self.page_number_label.pack(padx=4, side='left')

                        self.next_button.pack(padx=2, side='left')
            
            else:
                  self.previus_button.pack_forget()
                  self.page_number_label.pack_forget()
                  self.next_button.pack_forget()



      def update_label(self):
            self.download_status_label.config(text=data_utils.download_vars.download_status)

            self.progress_label.config(text=data_utils.download_vars.download_progress_msg)

class FrameSwitchState():
      def __init__(self):
            self.actual_frame = None
            self.main_frames_list = [search_screen.root, download_screen.root, details_screen.root]



def frame_switch(frame):
      if frame_switch_vars.actual_frame != frame:
            for i in frame_switch_vars.main_frames_list:
                  i.pack_forget()
            frame.pack()
            frame_switch_vars.actual_frame = frame

def clean_event(event,entry, placeholder):
            if entry.get() == placeholder:
                  entry.delete(0, tk.END)

def with_zeros(x):
      x_str = str(x)
      y = []
      if x < 10:
            y = ['000',x_str]
      elif x < 100:
            y = ['00', x_str]
      elif x < 1000:
            y = ['0', x_str]
      elif x >= 1000:
            y = ['', x_str]

      return ''.join(y)

class ActualPokeID():
      def __init__(self):
            self.id = None
            self.data = data_utils.DetailsVars(1)


def open_details(id):

      
      details_screen.root.pack(anchor='center', expand=True, fill='both')

      actual_poke_id.id = id
      actual_poke_id.data = data_utils.DetailsVars(actual_poke_id.id)

      details_screen_object.vars_def(details_screen.root)

      search_screen.root.pack_forget()

      root.rowconfigure(0, weight=1)
      root.columnconfigure(0, weight=1)

      
      details_screen_object.class_grid()


      details_screen_object.root.bind('<Configure>', details_screen_object.on_resize)
     

      print(actual_poke_id.data.name)
      print(actual_poke_id.id)

def type_color(type):
      type_colors = {
    "normal":   "#A9A878",
    "bug":      "#A8B821",
    "fighting": "#C03028",
    "ghost":    "#715899",
    "electric": "#F8D030",
    "flying":   "#A890F0",
    "steel":    "#B8B8D0",
    "psychic":  "#F85888",
    "poison":   "#A040A1",
    "fire":     "#F08030",
    "ice":      "#98D8D8",
    "ground":   "#E0C068",
    "water":    "#6890F0",
    "dragon":   "#7038F8",
    "rock":     "#B8A038",
    "grass":    "#78C850",
    "dark":     "#6F5848",
}
      return type_colors[type.lower()]

class PokemonCard():

      

      def __init__(self, name, parent):
            self.types = data_utils.names.databank[name]
            self.name = name
            self.id = data_utils.ids.databank[name]

            self.card = tk.Frame(parent, height=100, width=500 , bd=2, relief="raised")

            self.card.pack_propagate(False)

            self.card4 = tk.Frame(self.card, height=50, width=500)

            self.card4.pack_propagate(False)

            self.card5 = tk.Frame(self.card, height=50, width=500)

            self.card5.pack_propagate(False)

            self.card3 = tk.Frame(self.card4)

            self.card2 = tk.Frame(self.card5)

            self.type1 = self.types[0]

            if len(self.types) > 1:
                  self.type2 = self.types[1]

                  self.sub_title2 =tk.Button(self.card2, text= self.type2.capitalize(), font= ("Arial", 11), command= lambda: self.type_button_command(text= self.type2.capitalize()), cursor='hand2', bg=type_color(self.type2))

            

            self.title = tk.Button(self.card3, text=self.name.upper(), font=("Arial", 16, "bold"), cursor='hand2', bd=0, relief='flat', command= lambda: open_details(self.id))

            self.sub_title1 =tk.Button(self.card2, text= self.type1.capitalize(), font= ("Arial", 11), command= lambda: self.type_button_command(text= self.type1.capitalize()), cursor='hand2', bg=type_color(self.type1))

            self.index = tk.Label(self.card, text= f'#{with_zeros(self.id)}', font=('Arial', 20, 'bold'))

      def type_button_command(self, text, event=None):
            search_screen.entry.delete(0, tk.END)
            search_screen.entry.insert(0, text)
            search_screen.search_command()

      def class_pack(self):

            

            self.title.pack(pady=5, side='left')
            self.sub_title1.pack(padx=1, side="left")

            self.index.pack(padx=5, side='right')

            if len(self.types) > 1:
                  self.sub_title2.pack(side="left")

            self.card.pack(pady=5)
            self.card5.pack(side='bottom')
            self.card4.pack(side='top')
            self.card3.pack(padx=5, side='left')
            self.card2.pack(padx=5, pady=2, side='left')

      def class_pack_forget(self):
            self.card.destroy()





def initialize_program_frames(parent):
      global download_screen, search_screen, details_screen, root

      root = parent
      
      download_screen = ProgramFrame("download", root)
      search_screen = ProgramFrame("search", root)
      details_screen = ProgramFrame("details", root)




      global frame_switch_vars, actual_poke_id, details_screen_object, entry, placeholder

      entry = tk.Entry(
            search_screen.frame_1,
            width=50
      )



      placeholder = "Enter a pokemon name, type or index"

      entry.insert(0, placeholder)

      frame_switch_vars = FrameSwitchState()
      details_screen_object = details_screen_utils.DetailsScreen()

actual_poke_id = ActualPokeID()

