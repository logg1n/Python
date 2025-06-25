# 🧠 Django + Telegram Bot: Интеграция с API-профилем пользователя

## 📌 Описание

Проект демонстрирует продвинутую интеграцию Django и Telegram-бота. Пользователь может зарегистрировать свою связь с Telegram, а затем получить информацию о себе через API-запрос командой `/myinfo`.

---

## 🚀 Функциональность

- ✅ Регистрация пользователя через Telegram-бота `/register email@example.com`
- ✅ Получение данных профиля через `/myinfo`
- ✅ Обработка ошибок (например, если пользователь не зарегистрирован)
- ✅ CORS-настройки для кросс-доменных запросов
- ✅ Поддержка уникальной связи `telegram_id ↔ email` в базе данных

---

## 🏁 Запуск

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Настройте `.env`:

```env
TELEGRAM_BOT_TOKEN=<ваш_токен>
ALLOW_TELEGRAM_AUTO_CREATE=True
```

3. Выполните миграции и запустите сервер Django:

```bash
python manage.py migrate
python manage.py runserver
```

4. Запустите Telegram-бота:

```bash
python bot.py
```

---

## 🤖 Команды Telegram-бота

| Команда                        | Описание                                                                 |
|--------------------------------|--------------------------------------------------------------------------|
| `/register email@example.com` | Привязывает текущий Telegram-аккаунт к указанному email.                |
| `/myinfo`                      | Получает информацию о пользователе через Django API.                    |

❗️ Перед использованием `/myinfo` необходимо зарегистрироваться через `/register`.

---

## 🔐 CORS

В `settings.py` для разработки включено:

```python
CORS_ALLOW_ALL_ORIGINS = True  # Только для разработки!
```

Можно настроить `CORS_ALLOWED_ORIGINS` для продакшена.

---

## ✅ Пример использования

1. В Telegram:

```
/register test.user@example.com
```

2. После успешной привязки:

```
/myinfo
```

Бот ответит:

```
👤 Имя: testuser
📧 Email: test.user@example.com
📱 Телефон: не указан
```

---

