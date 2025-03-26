import random
import sqlite3
import tkinter as tk

from datadase import DataBase
from entry_placehlder import EntryWithPlaceholder
from player import Player

WIDTH = 400
HEIGHT = 400


def get_player(name):
   try:
      db.cursor.execute(f"""
            SELECT * FROM {table}
            WHERE name = ?
            """, (name,))
      return db.cursor.fetchone()
   except sqlite3.Error as e:
      print(f"Ошибка при получении игрока: {e}")
      return None


def insert_player(name):
   try:
      db.cursor.execute("""
            INSERT INTO players (name, total_wins, total_lose)
            VALUES (?, 0, 0)
            """, (name,))
      db.connection.commit()
      print(f"Игрок '{name}' успешно добавлен в таблицу!")
   except sqlite3.Error as e:
      print(f"Ошибка при добавлении игрока: {e}")


def on_start(name1, name2):
   if not name1 or not name2:
      print("Введите имена обоих игроков!")
      return
   if name1 == name2:
      print("Введите разные имена игроков!")
      return


   # Обработка игрока 1
   data1 = get_player(name1)
   if data1:
      player1.initialize(data1)
   else:
      insert_player(name1)
      data1 = get_player(name1)
      if data1:
         player1.initialize(data1)
      else:
         print("Ошибка при создании игрока 1")
         return

   # Обработка игрока 2
   data2 = get_player(name2)
   if data2:
      player2.initialize(data2)
   else:
      insert_player(name2)
      data2 = get_player(name2)
      if data2:
         player2.initialize(data2)
      else:
         print("Ошибка при создании игрока 2")
         return

   switch_screen(game_screen)


def switch_screen(func, **kwargs):
   for widget in window.winfo_children():
      widget.destroy()
   func(**kwargs)


def start_screen(pn1, pn2):
   player1_name = pn1 if pn1 else ""
   player2_name = pn2 if pn2 else ""



   # Контейнер для элементов формы
   form_frame = tk.Frame(window)
   form_frame.pack(pady=20, expand=True)

   player1_entry = EntryWithPlaceholder(
      form_frame,
      placeholder="Введите имя игрока 1",
      font=("Arial", 14),
      width=25
   )
   player1_entry.grid(row=1, column=1, padx=10, pady=20)

   player1_label = tk.Label(form_frame, text=player1_name, font=("Arial", 14))
   player1_label.grid(row=0, column=1, pady=5)


   player2_entry = EntryWithPlaceholder(
      form_frame,
      placeholder="Введите имя игрока 2",
      font=("Arial", 14),
      width=25
   )
   player2_entry.grid(row=2, column=1, padx=10, pady=5)

   player2_label = tk.Label(form_frame, text=player2_name, font=("Arial", 14))
   player2_label.grid(row=3, column=1, pady=5)

   # Общая функция обработки ввода
   def handle_enter(entry_widget, label_widget, is_player1=True):
      name = entry_widget.get_clean()
      if name:
         nonlocal player1_name, player2_name
         if is_player1:
            player1_name = name
         else:
            player2_name = name
         label_widget.config(text=name)
         entry_widget.delete(0, tk.END)
         entry_widget._set_placeholder()  # Восстанавливаем плейсхолдер

   # Привязка событий
   player1_entry.bind("<Return>",
                      lambda e: handle_enter(player1_entry, player1_label, True))

   player2_entry.bind("<Return>",
                      lambda e: handle_enter(player2_entry, player2_label, False))

   # Кнопка START GAME
   tk.Button(
      window,
      text="START GAME",
      font=("Arial", 16),
      command=lambda: on_start(player1_name, player2_name)
   ).pack(pady=20, side="bottom")

def back_screen(winner):
   # Очистка экрана
   for widget in window.winfo_children():
      widget.destroy()

   # Заголовок с результатом
   result_label = tk.Label(
      window,
      text=winner if winner == "Ничья!" else f"Победил {winner}!",
      font=("Arial", 20, "bold")
   )
   result_label.pack(pady=50)

   # Кнопка "Назад" с адаптивным позиционированием
   back_btn = tk.Button(
      window,
      text="Назад в меню",
      font=("Arial", 16),
      width=15,
      height=2,
      command=lambda: switch_screen(lambda: start_screen(player1.name, player2.name))
   )
   back_btn.pack(pady=20)

def update_stats(winner_name, loser_name):
   try:
      # Обновляем статистику победителя
      db.cursor.execute("""
            UPDATE players 
            SET total_wins = total_wins + 1 
            WHERE name = ?
        """, (winner_name,))

      # Обновляем статистику проигравшего
      db.cursor.execute("""
            UPDATE players 
            SET total_lose = total_lose + 1 
            WHERE name = ?
        """, (loser_name,))

      db.connection.commit()
      print("Статистика обновлена успешно!")
   except sqlite3.Error as e:
      print(f"Ошибка при обновлении статистики: {e}")


def game_screen():
   buttons = []
   current_player = random.choice(["X", "O"])

   def check_winner():
      for i in range(3):
         if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return 1
         if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return 1
      if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
         return 1
      if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
         return 1
      if all(buttons[x][y]["text"] != "" for x in range(3) for y in range(3)):
         return 3
      return 0

   def on_click(x, y):
      nonlocal current_player
      if buttons[x][y]['text'] != "":
         return
      buttons[x][y]['text'] = current_player
      result = check_winner()

      if result == 1:
         winner = player1 if current_player == 'X' else player2
         loser = player2 if current_player == 'X' else player1
         update_stats(winner.name, loser.name)
         switch_screen(lambda: back_screen(winner.name))  # Исправлено

      elif result == 3:
         switch_screen(lambda: back_screen("Ничья!"))
      else:
         current_player = "O" if current_player == "X" else "X"
         update_player_labels()

   def update_player_labels():
      player_label1.config(
         text=f"{player1} (X)",  # Добавлено .name
         font=("Arial", 14, "bold") if current_player == "X" else ("Arial", 14)
      )
      player_label2.config(
         text=f"{player2} (O)",  # Добавлено .name
         font=("Arial", 14, "bold") if current_player == "O" else ("Arial", 14)
      )

   # Создание элементов интерфейса (только один раз!)
   player_label1 = tk.Label(window, font=("Arial", 14))
   player_label2 = tk.Label(window, font=("Arial", 14))
   player_label1.place(x=10, y=10, anchor="nw")
   player_label2.place(x=WIDTH - 10, y=HEIGHT - 10, anchor="se")

   grid_frame = tk.Frame(window)
   grid_frame.place(relx=0.5, rely=0.5, anchor="center")

   for i in range(3):
      row = []
      for j in range(3):
         btn = tk.Button(
            grid_frame,
            text="",
            font=("Arial", 20),
            width=5,
            height=2,
            command=lambda r=i, c=j: on_click(r, c))
         btn.grid(row=i, column=j, padx=5, pady=5)
         row.append(btn)
      buttons.append(row)

   update_player_labels()  # Инициализация меток

if __name__ == '__main__':
   window = tk.Tk()
   window.title("Крестики-нолики")
   window.geometry(f"{WIDTH}x{HEIGHT}")

   player1 = Player()
   player1.sym = 'X'
   player2 = Player()
   player2.sym = 'O'

   db = DataBase("users.db")
   table = "players"
   db.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_wins INTEGER DEFAULT 0,
            total_lose INTEGER DEFAULT 0
        )
    """)
   db.connection.commit()

   start_screen("","")
   window.mainloop()
   db.close()
