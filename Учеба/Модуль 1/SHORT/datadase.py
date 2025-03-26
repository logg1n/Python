import sqlite3


class DataBase:
   def __init__(self, db_name):
      """Инициализация обёртки, подключение к базе данных."""
      self.connection = sqlite3.connect(db_name)
      self.cursor = self.connection.cursor()

   @property
   def connection(self):
      """Getter для connection."""
      return self._connection

   @connection.setter
   def connection(self, new_connection):
      """Setter для connection."""
      if isinstance(new_connection, sqlite3.Connection):
         self._connection = new_connection
      else:
         raise ValueError("Переданный объект не является экземпляром sqlite3.Connection")

   @property
   def cursor(self):
      """Getter для cursor."""
      return self._cursor

   @cursor.setter
   def cursor(self, new_cursor):
      """Setter для cursor."""
      if isinstance(new_cursor, sqlite3.Cursor):
         self._cursor = new_cursor
      else:
         raise ValueError("Переданный объект не является экземпляром sqlite3.Cursor")

   def close(self):
      self.cursor.close()
      self.connection.close()