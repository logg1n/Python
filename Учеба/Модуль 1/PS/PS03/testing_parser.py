import os
from dotenv import load_dotenv, set_key
from bs4 import BeautifulSoup
import requests

def read_file() -> str:
    """Читает HTML-данные из локального файла."""
    try:
        with open("page.html", "r", encoding="utf-8") as file:
            return file.read()
    except:
        update_env_flag(False)
        return ""

def save_file(content: str):
    """Сохраняет HTML-данные в локальный файл."""
    with open("page.html", "w", encoding="utf-8") as file:
        file.write(content)

def fetch_html() -> BeautifulSoup | None:
    """Получает HTML-данные с сайта."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = "https://www.21vek.by/mobile/"
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
        return None

def update_env_flag(value: bool):
    """Обновляет значение FLAG в файле .env."""
    env_path = ".env"
    # Преобразуем булево значение в строку "true"/"false"
    str_value = "true" if value else "false"
    set_key(env_path, "FLAG", str_value)

if __name__ == '__main__':
    load_dotenv()
    flag = os.getenv("FLAG", "false").lower() == "true"
    html: BeautifulSoup | None = None

    if flag:
        # Если FLAG=True, читаем из файла
        html_content = read_file()
        html = BeautifulSoup(html_content, "lxml")
    else:
        # Если FLAG=False, загружаем с сайта
        html = fetch_html()
        if html:
            save_file(str(html))
            update_env_flag(True)  # Устанавливаем FLAG=True

    if html:
        info = html.select('[data-testid="card-info"]')
        price = html.select('[data-testid="card-current-price"]')

        for i, p in zip(info, price):
            print(f"{i.text.strip("Смартфон | восстановленный")} : {p.text}")