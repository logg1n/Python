#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
from telebot import types
from telebot.types import Message


from trade import get_info_ticker

API_TOKEN = "7650936396:AAEJWIcu9bq8LcIyPGbDoZp1oMmKgH9d36Q"

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def start_command(message: Message):
    bot.reply_to(
        message,
        "Привет, напиши /price <тикер> что бы узнать последнюю цену! /price btcusdt",
    )


@bot.message_handler(commands=["price"])
def send_price(message: Message):
    try:
        ticker = message.text.split()[1].upper()
        ticker_info = get_info_ticker(ticker)
        if ticker_info:
            price = float(ticker_info.get("lastPrice", "Информация о цене недоступна"))
            bot.reply_to(message, f"Текущая цена {ticker}: {price}")
        else:
            bot.reply_to(message, "Не удалось получить информацию о цене.")
    except IndexError:
        bot.reply_to(message, "Пожалуйста, введите команду в формате /price <тикер>.")


@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "Пока только такие команды:\n"
        "/start - Начальное приветствие\n"
        "/price <тикер> - Узнать текущую цену указанного тикера\n"
        "/help - Показать список доступных команд"
    )
    bot.reply_to(message, help_text)


@bot.message_handler(func=lambda message: message.text.startswith("/"))
def handle_invalid_command(message):
    bot.reply_to(
        message,
        "К сожалению такой команды не существует, используйте /help для просмотра доступных команд.",
    )


@bot.message_handler(func=lambda message: not message.text.startswith("/"))
def handle_text_message(message):
    bot.reply_to(message, "Как интересно, можешь дальше не продолжать))")


bot.polling()
