import tkinter as tk

def clean_event(event):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)

def label_info_updater():
    tk_text.config(state="normal")
    tk_text.delete(1.0, tk.END)
    tk_text.insert(1.0, entry.get())
    tk_text.config(state="disabled")

root = tk.Tk()

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(
    frame,
    width=50
)

tk_text = tk.Text(root)
tk_text.config(state="disabled")


placeholder = "Enter a pokemon name or type"

entry.insert(0, placeholder)

entry.bind("<FocusIn>", clean_event)

button = tk.Button(
    frame,
    text="Search",
    command=lambda: label_info_updater()
)

entry.pack(pady=5, padx=5, side='left')
button.pack(pady=5, side='left') 
tk_text.pack(pady=40)

root.mainloop()

