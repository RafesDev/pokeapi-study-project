from modules import gui_utils
import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

def get_image_size(image):
      print(f"{image} size: {image.size}")
      return image.size


def get_frame_size(frame):
      print(f"{frame} size: {frame.winfo_width()} x {frame.winfo_height()}")
      return frame.winfo_width(), frame.winfo_height()

def resize_image(image, frame):
      frame_width, frame_height = get_frame_size(frame)
      image_width, image_height = get_image_size(image)

      width_ratio = frame_width / image_width
      height_ratio = frame_height / image_height

      print(f"Width ratio: {width_ratio}, Height ratio: {height_ratio}")

      resize_ratio = min(width_ratio, height_ratio)

      print(f"Resize ratio: {resize_ratio}")

      new_width = int(image_width * resize_ratio)
      new_height = int(image_height * resize_ratio)

      print(f"New image size: {new_width} x {new_height}")

      resized_image = image.resize((new_width, new_height))
      
      return resized_image

def on_resize(event, image, label):
      resized_image = resize_image(image, event.widget)
      photo = ImageTk.PhotoImage(resized_image)
      label.config(image=photo)
      label.image = photo  # Keep a reference to avoid garbage collection

root = tk.Tk()

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

image_frame = tk.Frame(root)
image_frame.grid(row=0, column=0, sticky="nsew")
image_frame.rowconfigure(0, weight=1)
image_frame.columnconfigure(0, weight=1)

pokemon_data = gui_utils.actual_poke_id.data

response = requests.get(pokemon_data.front)
print(pokemon_data.front)

pillow_image_front = Image.open(BytesIO(response.content))

resized_image_front = resize_image(pillow_image_front, image_frame)

pokemon_photo_front = ImageTk.PhotoImage(resized_image_front)

label = tk.Label(image_frame, image=pokemon_photo_front)
label.grid(row=0, column=0, sticky="nsew")

root.bind('<Configure>', lambda event: on_resize(event, pillow_image_front, label))

root.mainloop()