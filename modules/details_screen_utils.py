import tkinter as tk

from modules import(
      gui_utils,
      search_utils,
      data_utils
)


def close_details():
      gui_utils.details_screen.root.grid_forget()

      gui_utils.details_screen_object.root.grid_forget()

      gui_utils.search_screen.root.pack()
            
      

class DetailsScreen():
      def __init__(self, parent):

            parent.grid_rowconfigure(0, weight=1)
            parent.grid_columnconfigure(0, weight=1)

            self.root = tk.Frame(parent)

            self.coming_soon_label_frame = tk.Frame(self.root)
            
            self.exit_button = tk.Button(self.root, text='X', font=('Arial', 20, 'bold'), command= close_details)

            self.coming_soon_label = tk.Label(self.coming_soon_label_frame, text=f'Details Screen is...\nCOMING SOON!\nStay tuned!', font=('Arial', 50, 'bold'))

      def class_grid(self):

            self.root.grid(
                row=0,
                column=0,
                sticky='nsew'
            )

            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_columnconfigure(1, weight=0)

            self.root.grid_rowconfigure(1, weight=1)

            self.exit_button.grid(
                row=0,
                column=1,
                sticky='ne'
            )

            self.coming_soon_label_frame.grid(
                row=1,
                column=0,
                columnspan=2,
                sticky='nsew'
            )

            self.coming_soon_label.pack(
                expand=True
            )