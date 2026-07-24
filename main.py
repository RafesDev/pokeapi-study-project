from modules import gui_utils
from modules import data_utils

#* Main loop:

gui_utils.root.title('Pokédex App')

gui_utils.search_screen.frame_1.pack(pady=10)

gui_utils.search_screen.frame_2.pack(pady=10)

gui_utils.search_screen.frame_3.pack()

gui_utils.download_screen.frame_status.pack(pady=20)

gui_utils.download_screen.frame_1.pack(expand=True, fill="both")

home_activated = False

def main_loop():
      # DOWNLOAD
      if data_utils.names.need_download() or data_utils.types.need_download():
            if gui_utils.frame_switch_vars.actual_frame == gui_utils.search_screen.root:
                  gui_utils.root.destroy()

            else:
                  gui_utils.frame_switch(gui_utils.download_screen.root)
                  gui_utils.download_screen.update_label()


                  if data_utils.names.need_download():
                        data_utils.names.download_one()
                        gui_utils.download_screen.update_label()

                        if data_utils.names.last_of_current_page():

                              if data_utils.names.has_next_page():
                                    data_utils.names.turn_next_page()
                                    gui_utils.download_screen.update_label()
                              else:
                                    data_utils.names.save_downloaded_data()
                                    gui_utils.download_screen.update_label()


                  elif data_utils.types.need_download():
                        data_utils.types.download_one()
                        gui_utils.download_screen.update_label()

                        if data_utils.types.last_of_current_page():

                              if data_utils.types.has_next_page():
                                    data_utils.types.turn_next_page()
                                    gui_utils.download_screen.update_label()
                              else:
                                    data_utils.types.save_downloaded_data()
                                    gui_utils.download_screen.update_label()
                  

      else:

            gui_utils.frame_switch(gui_utils.search_screen.root)
            gui_utils.search_screen.update_label()

            data_utils.names.data_load()
            data_utils.types.data_load()
            gui_utils.search_screen.update_label()

            global home_activated

            if home_activated == False:
                  gui_utils.search_screen.home()

                  home_activated = True

           
      gui_utils.root.after(1, main_loop)

gui_utils.root.after(1, main_loop)

gui_utils.search_screen.home_button.pack(pady=5, side='left')
gui_utils.search_screen.entry.pack(pady=5, padx=5, side='left')
gui_utils.search_screen.button.pack(pady=5, side='left')
gui_utils.download_screen.download_status_label.pack(pady=20)
gui_utils.download_screen.progress_label.pack(pady=150)
      
gui_utils.root.mainloop()