from modules import gui_utils
from modules import download_utils

#* Main loop:

gui_utils.search_screen.frame_status.pack(pady=10)

gui_utils.search_screen.frame_1.pack(pady=10)

gui_utils.search_screen.frame_2.pack(pady=10)

gui_utils.download_screen.frame_status.pack(pady=20)

gui_utils.download_screen.frame_1.pack(expand=True, fill="both")



def main_loop():
      # DOWNLOAD
      if download_utils.names.need_download() or download_utils.types.need_download():
            gui_utils.frame_switch(gui_utils.download_screen.root)
            gui_utils.download_screen.update_label()


            if download_utils.names.need_download():
                  download_utils.names.download_one()
                  gui_utils.download_screen.update_label()

                  if download_utils.names.last_of_current_page():

                        if download_utils.names.has_next_page():
                              download_utils.names.turn_next_page()
                              gui_utils.download_screen.update_label()
                        else:
                              download_utils.names.save_downloaded_data()
                              gui_utils.download_screen.update_label()


            elif download_utils.types.need_download():
                  download_utils.types.download_one()
                  gui_utils.download_screen.update_label()

                  if download_utils.types.last_of_current_page():

                        if download_utils.types.has_next_page():
                              download_utils.types.turn_next_page()
                              gui_utils.download_screen.update_label()
                        else:
                              download_utils.types.save_downloaded_data()
                              gui_utils.download_screen.update_label()
                  

      else:
            gui_utils.download_screen.update_label()
            gui_utils.frame_switch(gui_utils.search_screen.root)

            download_utils.names.data_load()
            download_utils.types.data_load()
            

      gui_utils.root.after(1, main_loop)


gui_utils.root.after(1, main_loop)


gui_utils.search_screen.download_status_label.pack(pady=20)
gui_utils.search_screen.entry.pack(pady=5, padx=5, side='left')
gui_utils.search_screen.button.pack(pady=5, side='left') 
gui_utils.search_screen.text_tk.pack(pady=40)
gui_utils.download_screen.download_status_label.pack(pady=20)
gui_utils.download_screen.progress_label.pack(pady=50)
      
gui_utils.root.mainloop()