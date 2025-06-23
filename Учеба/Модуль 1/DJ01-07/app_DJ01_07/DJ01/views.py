from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests


# Create your views here.

def data(request):
    # Получаем данные о погоде через API (используем OpenWeatherMap)
    def get_weather(city):
        API_KEY = "441edc6b9e726e3b9b27f4b5fd0f752d"  # Зарегистрируйтесь на https://openweathermap.org для бесплатного ключа
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url).json()
        return {
            "city": city,
            "temp": response["main"]["temp"],
            "description": response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"]
        }

    weather_data = {
        "Минск": get_weather("Minsk"),
        "Москва": get_weather("Moscow"),
    }

    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Погода в Минске и Москве</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        .weather-container {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        .weather-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 200px;
        }}
        .weather-icon {{
            width: 100px;
            height: 100px;
        }}
        .temp {{
            font-size: 24px;
            font-weight: bold;
            color: #0066cc;
        }}
    </style>
</head>
<body>
    <h1>Погода сейчас</h1>
    <div class="weather-container">
        <div class="weather-card">
            <h2>{weather_data["Минск"]["city"]}</h2>
            <img src="http://openweathermap.org/img/wn/{weather_data["Минск"]["icon"]}@2x.png" class="weather-icon">
            <div class="temp">{weather_data["Минск"]["temp"]}°C</div>
            <p>{weather_data["Минск"]["description"].capitalize()}</p>
        </div>
        <div class="weather-card">
            <h2>{weather_data["Москва"]["city"]}</h2>
            <img src="http://openweathermap.org/img/wn/{weather_data["Москва"]["icon"]}@2x.png" class="weather-icon">
            <div class="temp">{weather_data["Москва"]["temp"]}°C</div>
            <p>{weather_data["Москва"]["description"].capitalize()}</p>
        </div>
    </div>
</body>
</html>
    """
    return HttpResponse(html_content)

def test(request):
    current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #333;
            }}
            #current-date {{
                font-weight: bold;
                color: #0066cc;
            }}
        </style>
    </head>
    <body>
        <h1>Test Page</h1>
        <p>Текущая дата: <span id="current-date">{current_date}</span></p>
        <p>Это тестовая страница с датой и текстом.</p>

        <script>
            // Обновляем дату через JavaScript (если нужно динамическое изменение)
            const dateElement = document.getElementById('current-date');
            dateElement.textContent = new Date().toLocaleString('ru-RU');
        </script>
    </body>
    </html>
        """
    return HttpResponse(html)

