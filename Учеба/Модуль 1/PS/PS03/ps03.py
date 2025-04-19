from time import process_time

import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator


# Создаём функцию, которая будет получать информацию
def get_russian_words() -> dict[str, str]:
   url = "https://randomword.com/"
   try:
      response = requests.get(url)
      response.raise_for_status()  # Проверка HTTP-ошибок

      soup = BeautifulSoup(response.content, "html.parser")
      english_word = soup.find("div", id="random_word").text.strip()
      word_definition = soup.find("div", id="random_word_definition").text.strip()

      translator = GoogleTranslator(source='auto', target='ru')

      # Синхронный перевод
      russian_word = translator.translate(english_word)
      russian_definition = translator.translate(word_definition)

      return {
         "russian_word": russian_word,
         "word_definition": russian_definition
      }


   except Exception as e:
      print(f"Произошла ошибка: {str(e)}")
      return {}


# Создаём функцию, которая будет делать саму игру
def word_game():
   print("Добро пожаловать в игру")
   while True:
      # Создаём функцию, чтобы использовать результат функции-словаря
      word_dict = get_russian_words()
      word = word_dict.get("russian_word")
      word_definition = word_dict.get("word_definition")
      print(word)
      print(word_definition)

      # Начинаем игру
      print(f"Значение слова - {word_definition}")
      user = input("Что это за слово? ")
      if user == word:
         print("Все верно!")
      else:
         print(f"Ответ неверный, было загадано это слово - {word}")

      # Создаём возможность закончить игру
      play_again = input("Хотите сыграть еще раз? y/n")
      if play_again != "y":
         print("Спасибо за игру!")
         break


word_game()
