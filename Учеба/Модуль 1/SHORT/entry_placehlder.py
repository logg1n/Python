import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
   def __init__(self, master=None, placeholder=None, color='grey', **kwargs):
      super().__init__(master, **kwargs)

      self.placeholder = placeholder
      self.placeholder_color = color
      self.default_fg_color = self['fg']

      self.bind("<FocusIn>", self._clear_placeholder)
      self.bind("<FocusOut>", self._set_placeholder)

      self._set_placeholder()

   def _set_placeholder(self, event=None):
      if not self.get():
         self.insert(0, self.placeholder)
         self.config(fg=self.placeholder_color)

   def _clear_placeholder(self, event=None):
      if self.get() == self.placeholder:
         self.delete(0, tk.END)
         self.config(fg=self.default_fg_color)

   def get_clean(self):
      content = self.get()
      if content == self.placeholder:
         return ''
      return content


# Пример использования
if __name__ == '__main__':
   root = tk.Tk()

   # Создаем поле с плейсхолдером
   entry = EntryWithPlaceholder(
      root,
      placeholder="Введите ваше имя...",
      width=30,
      font=('Arial', 12)
   )
   entry.pack(pady=20, padx=20)


   # Кнопка для демонстрации получения значения
   def show_value():
      print("Введенное значение:", entry.get_clean())


   tk.Button(root, text="Показать значение", command=show_value).pack()

   root.mainloop()