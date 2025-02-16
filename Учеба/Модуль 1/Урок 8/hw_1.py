import tkinter as tk


def update_label(event):
    label_name.config(text=f"Привет {entry.get()}!")
    entry.delete(0, tk.END)


root = tk.Tk()
root.title("Hello")
root.config(width=228, height=228, padx=24, pady=24)

entry = tk.Entry(root, border=0)
entry.grid(column=1, row=1)
entry.bind("<Return>", update_label)

label_placeholder = tk.Label(root, text="Введите ваше имя:")
label_placeholder.grid(column=1, row=0)

label_name = tk.Label(root, text="")
label_name.grid(column=1, row=3)


root.mainloop()
