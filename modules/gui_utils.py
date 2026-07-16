import tkinter as tk

from modules import (
  download_utils,
  search_utils
)

root = tk.Tk()

class ProgramFrame():
      def __init__(self, name):

            self.name = name

            self.root = tk.Frame(root)

            self.frame_status = tk.Frame(self.root)
      
            self.frame_1 = tk.Frame(self.root)

            self.frame_2 = tk.Frame(self.root)

            self.download_status_label = tk.Label(
                  self.frame_status,
                  text=download_utils.download_vars.download_status)

            self.progress_label = tk.Label(
                  self.frame_2,
                  text=download_utils.download_vars.download_progress_msg)

            self.entry = tk.Entry(
                  self.frame_1,
                  width=50
            )

            self.text_tk = tk.Text(self.frame_2)


            self.placeholder = "Enter a pokemon name or type"

            self.entry.insert(0, self.placeholder)

            self.entry.bind("<FocusIn>",lambda event: clean_event(event, self.entry, self.placeholder))

            self.button = tk.Button(
                  self.frame_1,
                  text="Search",
                  command=lambda:(
                        self.label_info_updater(
)))

      def label_info_updater(
                  self
            ):
            pokemon_input = self.entry.get().lower()
            self.text_tk.config(state="normal")
            self.text_tk.delete(1.0, tk.END)
            self.text_tk.insert(1.0, (search_utils.pokemon_answer_message(
            pokemon_input,
            )))
            self.text_tk.config(state="disabled")

      def update_label(self):

            self.download_status_label.config(text=download_utils.download_vars.download_status)

            self.progress_label.config(text=download_utils.download_vars.download_progress_msg)





### FRAMES:


      
download_screen = ProgramFrame("download")
search_screen = ProgramFrame("search")
details_screen = ProgramFrame("details")






### MAIN SCREEN:

entry = tk.Entry(
      search_screen.frame_1,
      width=50
)

text_tk = tk.Text(search_screen.frame_2)


placeholder = "Enter a pokemon name or type"

entry.insert(0, placeholder)

#entry.bind("<FocusIn>",lambda event: clean_event(event, entry, placeholder))

#button = tk.Button(
#      search_screen.frame_1,
#      text="Search",
#      command=lambda: 
#            label_info_updater(
#                  entry, 
#                  text_tk, 
#                  names.databank,
#                  types.databank,
#                  names.file_path,
#                  types.file_path
#))


class FrameSwitchState():
      def __init__(self):
            self.actual_frame = None
            self.main_frames_list = [search_screen.root, download_screen.root, details_screen.root]

frame_switch_vars = FrameSwitchState()

def frame_switch(frame):
      if frame_switch_vars.actual_frame != frame:
            for i in frame_switch_vars.main_frames_list:
                  i.pack_forget()
            frame.pack()
            frame_switch_vars.actual_frame = frame

def clean_event(event,entry, placeholder):
            if entry.get() == placeholder:
                  entry.delete(0, tk.END)