from logging import root
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

import requests

from modules import(
      gui_utils,
      search_utils,
      data_utils
)

details_content = None

def without_line_break(string_with_line_break): ## Yes, I didn't knew that "replace()" exists. TnT
      letter_list = []
      for letter in string_with_line_break:
            if letter.isspace():
                  letter_list.append(' ')
            else:
                  letter_list.append(str(letter))

      return ''.join(letter_list)

def get_image_size(image):
      print(f"{image} size: {image.size}")
      return image.size


def get_frame_size(width_weight, height_weight, root_width, root_height):
      print(f"Frame size: {root_width * width_weight} x {root_height * height_weight}")
      return root_width * width_weight, root_height * height_weight

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

def close_details():
      gui_utils.details_screen.root.grid_forget()

      gui_utils.details_screen_object.root.grid_forget()

      gui_utils.search_screen.root.pack()

class DetailsScreen():
      def vars_def(self, parent):

            parent.grid_rowconfigure(0, weight=1)
            parent.grid_columnconfigure(0, weight=1)

            self.root = parent
            self.root.config(bg='red')

            

            self.root_width = gui_utils.root.winfo_width()
            self.root_height = gui_utils.root.winfo_height()

            print('width: ',self.root_width)
            print('height: ',self.root_height)

            self.border_frame_n = tk.Frame(self.root, height=(self.root_height*0.01), bg='red')
            self.border_frame_s = tk.Frame(self.root, height=(self.root_height*0.01), bg='red')
            self.border_frame_e = tk.Frame(self.root, width=(self.root_width*0.01), bg='red')
            self.border_frame_w = tk.Frame(self.root, width=(self.root_width*0.01), bg='red')

            print(gui_utils.actual_poke_id.data.name)
            self.data = gui_utils.actual_poke_id.data


            self.header_frame = tk.Frame(self.root, bg='light blue')
            self.title_frame = tk.Frame(self.header_frame, bg='light blue')

            self.name_label = tk.Label(self.title_frame, text=self.data.name.upper(), font=('Arial', 60, 'bold'), bg='light blue')
            self.exit_button = tk.Button(self.header_frame, text='X', font=('Arial', 40, 'bold'), command= close_details, bg='light blue')


            self.content_frame = tk.Frame(self.root)

            self.left_frame = tk.Frame(self.content_frame, bg='red')
            self.mid_spacer_frame = tk.Frame(self.content_frame, width=(self.root_width*0.01), bg='red')
            self.right_frame = tk.Frame(self.content_frame, bg='red', width=(self.root_width*0.55))

            ## HEADER
            self.header_left = tk.Frame(self.left_frame, bg='red')
            self.id_label = tk.Label(self.header_left, text=f'#{gui_utils.with_zeros(self.data.id)}', font=('Arial', 40, 'bold'), bg='light blue')
            self.types_frame = tk.Frame(self.header_left, bg='light blue')
            self.type1_label = tk.Label(self.types_frame, text=self.data.type1.capitalize(), font=('Arial', 40, 'bold'), bg=type_color(self.data.type1))
            self.types_frame_spacer = tk.Frame(self.types_frame, bg='light blue', width=(self.root_width*0.01))
            self.type2_label = tk.Label(self.types_frame, text=self.data.type2.capitalize(), font=('Arial', 40, 'bold'), bg=type_color(self.data.type2)) if len(self.data.types) > 1 else None

            ## LEFT
            self.top_spacer_frame = tk.Frame(self.left_frame, height=(self.root_height*0.01))
            self.pokemon_image_frame = tk.Frame(self.left_frame, height=(self.root_height*0.5))
            self.pokemon_image_frame.grid_propagate(False)

            self.image_front = requests.get(self.data.front)
            self.image_back = requests.get(self.data.back)
            self.actual_image = self.image_front

            self.original_image = Image.open(BytesIO(self.actual_image.content))
            self.image = ImageTk.PhotoImage(self.resize_image(self.original_image))

            self.image_label = tk.Label(self.pokemon_image_frame, image=self.image, bg='light blue')

            self.image_turn_button = tk.Button(self.pokemon_image_frame, text='↔', font=('Arial', 30, 'bold'), bg='light blue', command=self.turn_image)

            ## RIGHT

            # TOP

            ## DESCRIPTION (HEADER)
            self.description_frame = tk.Frame(self.right_frame, width=(self.root_width*0.55))
            self.description_header = tk.Frame(self.description_frame)
            self.description_title = tk.Label(self.description_header, text='DESCRIPTION', font=('Arial', 35, 'bold'), bg='red')

            ## DESCRIPTION (CONTENT/TEXT)
            self.description_content_frame = tk.Frame(self.description_frame, width=(self.root_width*0.55))
            self.description_content_frame.grid_propagate(False)
            self.description_content = tk.Text(self.description_content_frame, font=('Arial', 30, 'bold'), wrap='word', bg='light blue', relief='flat', highlightthickness=0)
            self.description_content.insert('1.0',without_line_break(self.data.description))
            self.description_content.configure(state='disabled')

            # BOTTOM

            self.right_bottom_frame = tk.Frame(self.right_frame, width=(self.root_width*0.55))
            self.right_bottom_frame.grid_propagate(False)

            ## EVO FAMILY
            self.evo_family_frame = tk.Frame(self.right_bottom_frame, bg='light blue', width=(self.root_width*0.27))
            self.evo_family_label = tk.Label(self.evo_family_frame, text='EVO FAMILY', font=('Arial', 35, 'bold'), bg='red')
            self.evo_family_frame.grid_propagate(False)

            self.evo_coming_soon_label = tk.Label(self.evo_family_frame, text='COMING SOON', font=('Arial', 30, 'bold'), bg='light blue')

            self.right_bottom_spacer_frame = tk.Frame(self.right_bottom_frame, width=(self.root_width*0.01), bg='red')

            ## STATS
            self.stats_frame = tk.Frame(self.right_bottom_frame, bg='light blue')
            self.stats_label = tk.Label(self.stats_frame, text='STATS', font=('Arial', 35, 'bold'), bg='red')

            self.stats_coming_soon_label = tk.Label(self.stats_frame, text='COMING SOON', font=('Arial', 30, 'bold'), bg='light blue')






      def resize_image(self,image):
            frame_width, frame_height = get_frame_size(0.42, 0.5, self.root_height, self.root_width)
            image_width, image_height = get_image_size(image)

            width_ratio = frame_width / image_width
            height_ratio = frame_height / image_height

            print(f"Width ratio: {width_ratio}, Height ratio: {height_ratio}")

            resize_ratio = min(width_ratio, height_ratio)

            print(f"Resize ratio: {resize_ratio}")

            new_width = int(image_width * resize_ratio * 1.2)
            new_height = int(image_height * resize_ratio * 1.2)

            print(f"New image size: {new_width} x {new_height}")

            resized_image = image.resize((new_width, new_height))
            
            return resized_image

      def load_image(self):
            self.image = ImageTk.PhotoImage(self.resize_image(self.original_image))
                        
            self.image_label.configure(image=self.image)

      def turn_image(self):
            if self.actual_image == self.image_front:
                  self.actual_image = self.image_back
            elif self.actual_image == self.image_back:
                  self.actual_image = self.image_front

            self.original_image = Image.open(BytesIO(self.actual_image.content))

            self.load_image()

      def on_resize(self, event):
            print('old width: ',self.root_width)
            print('old height: ',self.root_height)

            self.root_width = event.width
            self.root_height = event.height

            self.right_frame.configure(width=(self.root_width*0.55))
            self.description_frame.configure(width=(self.root_width*0.55))
            self.description_content_frame.configure(width=(self.root_width*0.55))
            self.right_bottom_frame.configure(width=(self.root_width*0.55))
            self.evo_family_frame.configure(width=(self.root_width*0.27))
            self.right_bottom_spacer_frame.configure(width=(self.root_width*0.01))
            self.pokemon_image_frame.configure(height=(self.root_height*0.5))
            self.load_image()

            print('new width: ',self.root_width)
            print('new height: ',self.root_height)








      ### UI CONFIG



      ## UI STRUCTURE

      def root_grid(self):
            self.root.grid(
            row=0,
            column=0,
            sticky='nsew'
            )

            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_rowconfigure(2, weight=1)

            self.root.grid_rowconfigure(0, weight=0)
            self.root.grid_columnconfigure(0, weight=0)

            self.root.grid_rowconfigure(3, weight=0)

      def content_grid(self):
            self.content_frame.grid(
                  row=2,
                  column=1,
                  sticky='nsew'
            )

            self.content_frame.grid_rowconfigure(0, weight=1)

            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_columnconfigure(1, weight=0)
            self.content_frame.grid_columnconfigure(2, weight=0)

      def left_frame_grid(self):
            self.left_frame.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )

            self.left_frame.grid_rowconfigure(0, weight=0)
            self.left_frame.grid_rowconfigure(1, weight=0)
            self.left_frame.grid_rowconfigure(2, weight=0)
            self.left_frame.grid_rowconfigure(3, weight=1)
            self.left_frame.grid_columnconfigure(0, weight=1)

            self.header_left.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )

      def right_frame_grid(self):
            self.right_frame.grid(
                  row=0,
                  column=2,
                  sticky='nsew'
            )

            self.right_frame.columnconfigure(0, weight=1)
            self.right_frame.rowconfigure(0, weight=3)
            self.right_frame.rowconfigure(1, weight=5)

      def spacers_grid(self):
            self.top_spacer_frame.grid(
                  row=1,
                  column=1,
                  sticky='nsew'
            )

            self.mid_spacer_frame.grid(
                  row=0,
                  column=1,
                  sticky='nsew'
            )

            self.right_bottom_spacer_frame.grid(
                  row=0,
                  column=1,
                  sticky='nsew'
            )

            self.border_frame_n.grid(
                row=0,
                column=0,
                sticky='n'
            )            

            self.border_frame_e.grid(
                  row=0,
                  column=2,
                  sticky='e'
            )

            self.border_frame_w.grid(
                  row=0,
                  column=0,
                  sticky='w'
            )


      ## UI ELEMENTS

      def header_grid(self):
            self.header_frame.grid(
                row=1,
                column=1,
                sticky='nsew'
            )

            self.header_frame.grid_columnconfigure(1, weight=1)
            self.header_frame.grid_columnconfigure(2, weight=0)

            self.title_frame.grid(
                  row=1,
                  column=1,
                  sticky='nsew'
            )

            self.name_label.pack(pady=2, anchor='w', expand=True)

            self.header_left.grid_rowconfigure(0, weight=1)
            self.header_left.grid_columnconfigure(0, weight=1)
            self.header_left.grid_columnconfigure(1, weight=1)

            self.id_label.grid(
                  row=0,
                  column=0,
                  sticky='w'
            )

            self.types_frame.grid(
                  row=0,
                  column=1,
                  stick='e'
            )

            self.types_frame.grid_rowconfigure(0, weight=1)
            self.types_frame.grid_columnconfigure(0, weight=1)
            self.types_frame.grid_columnconfigure(1, weight=1)
            self.types_frame.grid_columnconfigure(2, weight=1)

            self.type1_label.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )
            if len(self.data.types) > 1:
                  self.types_frame_spacer.grid(
                        row=0,
                        column=1,
                        sticky='nsew'
                  )
                  self.type2_label.grid(
                        row=0,
                        column=2,
                        sticky='nsew'
                  )

            self.exit_button.grid(
                  row=1,
                  column=2,
                  sticky='ne'
            )

      def description_frame_grid(self):
            self.description_frame.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )

            self.description_frame.columnconfigure(0, weight=1)
            self.description_frame.rowconfigure(0, weight=1)
            self.description_frame.rowconfigure(1, weight=10)

            self.description_header.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )
            self.description_header.columnconfigure(0, weight=1)
            self.description_header.rowconfigure(0, weight=1)
            self.description_title.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )

            self.description_content_frame.grid(
                  row=1,
                  column=0,
                  sticky='nsew'
            )
            self.description_content_frame.rowconfigure(0, weight=1)
            self.description_content_frame.columnconfigure(0, weight=1)

            self.description_content.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )
            

      def right_bottom_frame_grid(self):
            self.right_bottom_frame.grid(
                  row=1,
                  column=0,
                  sticky='nsew'
            )
            self.right_bottom_frame.rowconfigure(0, weight=1)
            self.right_bottom_frame.columnconfigure(0, weight=0)
            self.right_bottom_frame.columnconfigure(1, weight=0)
            self.right_bottom_frame.columnconfigure(2, weight=1)

      def pokemon_image_frame_grid(self):
            self.pokemon_image_frame.grid(
                  row=2,
                  column=0,
                  sticky='nsew'
            )
            self.pokemon_image_frame.rowconfigure(0, weight=1)
            self.pokemon_image_frame.columnconfigure(0, weight=1)

            self.image_label.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )

            self.image_turn_button.place(relx=1.0, rely=1.0, anchor="se")

      def evo_family_grid(self):      
            self.evo_family_frame.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )
            self.evo_family_frame.rowconfigure(0, weight=0)
            self.evo_family_frame.columnconfigure(0, weight=1)
            self.evo_family_frame.rowconfigure(1, weight=1)

            self.evo_family_label.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )

            self.evo_coming_soon_label.grid(
                  row=1,
                  column=0,
                  sticky='nsew'
            )
            
      def stats_frame_grid(self):
            self.stats_frame.grid(
                  row=0,
                  column=2,
                  sticky='nsew'
            )
            self.stats_frame.rowconfigure(0, weight=0)
            self.stats_frame.columnconfigure(0, weight=1)
            self.stats_frame.rowconfigure(1, weight=1)
            self.stats_label.grid(
                  row=0,
                  column=0,
                  sticky='nsew'
            )
            self.stats_coming_soon_label.grid(
                  row=1,
                  column=0,
                  sticky='nsew'
            )

      def class_grid(self):

            self.root_grid()
            self.content_grid()
            self.left_frame_grid()
            self.right_frame_grid()
            self.spacers_grid()
            self.right_bottom_frame_grid()
            self.pokemon_image_frame_grid()
            self.description_frame_grid()
            self.header_grid()
            self.evo_family_grid()
            self.stats_frame_grid()