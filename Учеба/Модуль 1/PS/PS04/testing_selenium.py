import textwrap
from typing import Dict, Any

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement


def init_browser(option: Dict[str, Any] | None = None)->WebDriver:
   options = Options()
   if option is not None:
      for k, v in option.items():
         options.add_experimental_option(k, v)

   return WebDriver(options)

def init_menu(browser):
   menu = ("1. Нужно что-то найти?\n"
           +"2. Выйти из программы\n"
           +"Введите пункт меню.\n")

   while val := input(menu):
      match val:
         case '1':
            while True:
               try:
                  search = browser.find_element(By.XPATH, "//input[@name='search']")
                  search.clear()
                  search.send_keys(input("Что вы хотите найти?\n"))
                  search.submit()

                  match input("Это то что вы искали?(e-выход) (y/n/e)\n").lower():
                     case 'y':
                        init_sub_menu(browser)
                        break
                     case 'e':
                        browser.quit()
                        exit()
                     case _:
                        browser.back()
               except StaleElementReferenceException:
                  print("Элемент устарел. Повторяем поиск...")
                  continue
               except Exception as e:
                  print(f"Ошибка: {e}")
                  print("Браузер закрыт или произошла ошибка. Перезапускаю...")
                  browser.quit()

                  browser = init_browser(options)
                  browser.get("https://ru.wikipedia.org/wiki/")
                  break
         case '2':
            browser.quit()
            exit()
         case _:
            continue


import textwrap
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


def init_sub_menu(browser):
   sub_menu = ("1. Следующий параграф\n"
               + "2. Предыдущий параграф\n"
               + "3. Найти связанные страницы\n"
               + "4. Назад (к предыдущей странице)\n"
               + "5. Выход в главное меню\n"
               + "Введите пункт меню.\n")

   # Храним историю посещенных страниц
   history = [browser.current_url]

   paragraphs = browser.find_elements(By.XPATH, "//p")
   if not paragraphs:
      print("Не найдено ни одного параграфа!")
      return

   current_index = 0
   links_in_paragraph = []

   def print_paragraph(index):
      """Печатает параграф с форматированием и собирает ссылки"""
      nonlocal links_in_paragraph
      paragraph = paragraphs[index]
      paragraph_text = paragraph.text
      cleaned_text = ' '.join(paragraph_text.split())
      wrapped_text = textwrap.fill(cleaned_text, width=80)

      links_in_paragraph = paragraph.find_elements(By.XPATH, ".//a")

      print(f"\nПараграф {index + 1}/{len(paragraphs)}:")
      print(f"Найдено ссылок: {len(links_in_paragraph)}\n")
      print(wrapped_text)
      print("\n" + "=" * 80 + "\n")

   def show_links_menu():
      """Меню для выбора ссылок из параграфа"""
      if not links_in_paragraph:
         print("В этом параграфе нет ссылок!")
         return False

      print("\nСписок связанных страниц:")
      for i, link in enumerate(links_in_paragraph, 1):
         link_text = link.text.strip() or "[без текста]"
         href = link.get_attribute('href') or "#"
         print(f"{i}. {link_text} ({href[:50]}...)")

      print(f"{len(links_in_paragraph) + 1}. Отмена")

      try:
         choice = int(input("\nВыберите ссылку для перехода: "))
         if 1 <= choice <= len(links_in_paragraph):
            links_in_paragraph[choice - 1].click()
            # Добавляем новую страницу в историю
            history.append(browser.current_url)
            return True
         elif choice == len(links_in_paragraph) + 1:
            return False
         else:
            print("Неверный выбор!")
      except ValueError:
         print("Пожалуйста, введите число!")
      return False

   print_paragraph(current_index)

   while True:
      try:
         val = int(input(sub_menu))
         match val:
            case 1:  # Следующий параграф
               if current_index + 1 < len(paragraphs):
                  current_index += 1
                  print_paragraph(current_index)
               else:
                  print("Это последний параграф!")
            case 2:  # Предыдущий параграф
               if current_index - 1 >= 0:
                  current_index -= 1
                  print_paragraph(current_index)
               else:
                  print("Это первый параграф!")
            case 3:  # Поиск связанных страниц
               if show_links_menu():
                  # Обновляем данные после перехода
                  paragraphs = browser.find_elements(By.XPATH, "//p")
                  current_index = 0
                  if paragraphs:
                     print_paragraph(current_index)
            case 4:  # Назад (к предыдущей странице)
               if len(history) > 1:
                  history.pop()  # Удаляем текущий URL
                  browser.get(history[-1])  # Переходим на предыдущий
                  paragraphs = browser.find_elements(By.XPATH, "//p")
                  current_index = 0
                  if paragraphs:
                     print_paragraph(current_index)
               else:
                  print("Это первая страница, назад нельзя!")
            case 5:  # Выход в главное меню
               return
            case _:
               print("Неверный пункт меню!")
      except ValueError:
         print("Пожалуйста, введите число!")
      except StaleElementReferenceException:
         print("Содержимое страницы изменилось, обновляем данные...")
         paragraphs = browser.find_elements(By.XPATH, "//p")
         if not paragraphs:
            print("Параграфы больше не найдены!")
            return
         current_index = min(current_index, len(paragraphs) - 1)
         print_paragraph(current_index)

if __name__ == '__main__':
   options = {
      "detach": True,
      "excludeSwitches": ["enable-automation"],
   }
   browser = init_browser(options)
   browser.get("https://ru.wikipedia.org/wiki/")

   init_menu(browser)

