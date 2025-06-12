# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 18:34:15 2025

@author: Polina Smagina
"""

from flask import Flask, request
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
)
import asyncio

app = Flask(__name__)
TOKEN = '7552462255:AAEkMMPlsedRLloda5E30cbmQs9jE_BFLho'

import os
TOKEN = os.getenv("TOKEN")
# Создаем приложение
application = Application.builder().token(TOKEN).build()

# Примерная структура данных
categories = {
    "Покуш": [
        {
            "name": "Завтрак",
            "description": "Идеи для вкусного начала дня ☀️",
            "images": [
                {"url": "https://drive.google.com/file/d/1FJADhUvoAQRRojpzsSueiLUZ_MaFpCfQ/view?usp=sharing", "caption": "Оладушки🥞"},
                {"url": "", "caption": "Яичница🍳"},
                {"url": "", "caption": "Каша🥣"},
                {"url": "", "caption": "Горячие бутербродики🥪"},
                {"url": "", "caption": "Сырники🥯"}
            ]
        },
        {
            "name": "Обед-ужин",
            "description": "Хочется сытно поесть 🍽️️",
            "images": [
                {"url": "", "caption": "Том ям🍛"},
                {"url": "", "caption": "Самса🫓"},
                {"url": "", "caption": "Бургир🍔"},
                {"url": "", "caption": "Паста🍝"},
                {"url": "", "caption": "Шаверма🌯"},
                {"url": "", "caption": "Суши🍣"},
                {"url": "", "caption": "Запеченное рагу🥘"}
             ]
        },
        {
            "name": "Вкусняшки",
            "description": "Хочется сладости приготовить 🧁",
            "images": [
                {"url": "", "caption": "Синабоны🍮"},
                {"url": "", "caption": "Тортик🍰"},
                {"url": "", "caption": "Печеньки🍪"}
            ]
        },
    ],
    "Хорошая погода, выходим на улицу!": [
            {
                "name": "Сапборды",
                "description": "Тепло, бегом кататься️",
                "images": [
                    {"url": "https://optim.tildacdn.com/tild3462-6565-4230-b235-303364363665/-/format/webp/photo.jpg.webp", "caption": "Река Оредеж"},
                    {"url": "", "caption": "Самим взять сап и найти место"}
            ]
        },
        {
                "name": "Кинотеатр",
                "description": "Базовая свиданка️",
                "images": [
                    {"url": "", "caption": "Кинооо"},
                    {"url": "", "caption": "Фильм на открытом воздухе"}
            ]
        },
        {
                "name": "Культурно обогащаемся",
                "description": "Так уж и быть без кроссвордов️",
                "images": [
                    {"url": "", "caption": "Театр"},
                    {"url": "", "caption": "Музей"}
            ]
        },
        {
                "name": "Поездка на электричке",
                "description": "Начнем с таких путешествий️",
                "images": [
                    {"url": "", "caption": "Выборг"},
                    {"url": "", "caption": "Петергоф"},
                    {"url": "", "caption": "Кронштадт"},
                    {"url": "", "caption": "Разные городки в ЛО"}
            ]
        },
        {
                "name": "Активности 😊",
                "description": "Обязательные активности в теплую погоду️",
                "images": [
                    {"url": "", "caption": "Ладожское озеро"},
                    {"url": "", "caption": "Веревочный парк (Кошкино)"},
                    {"url": "", "caption": "Веревочный парк (СПБ)"},
                    {"url": "", "caption": "Мазапарк"},
                    {"url": "https://cdn.culture.ru/images/6d028ee8-9812-5996-9a22-8c605e38fa38", "caption": "Покататься на велосипедах"},
                    {"url": "", "caption": "Погулять в парке"}
            ]
        },
        {
                "name": "Термальный комплекс",
                "description": "Полный релакс️",
                "images": [
                    {"url": "https://newreportage.ru/wp-content/uploads/2023/03/IMG_20230325_224229.jpg", "caption": "https://greenflowlakhtapark.ru/price"}
            ]
        },
    ],
    "Посиделки дома": [
            {
                "name": "Порисовать на мольбертах",
                "description": "Будем разукрашивать картину или сами нарисуем, все равно мили мили️",
                "images": [
                    {"url": "", "caption": "Ляляля"}
            ]
        },
        {
                "name": "Полепить из глины",
                "description": "Будет тебе пепельница:D",
                "images": [
                    {"url": "", "caption": "Рукодельничать будем"}
            ]
        },
        {
                "name": "Поиграть в настолки",
                "description": "Найдем игры для двоих️",
                "images": [
                    {"url": "", "caption": "Уютни вечер"}
            ]
        },
        {
                "name": "Полепить из воздушного пластилина",
                "description": "Пластилиновое свидание из рилсов️",
                "images": [
                    {"url": "", "caption": "Милые фигурки"}
            ]
        },
    ],
        "Киновечер": [
            {
                "name": "Комедия",
                "description": "Легкие фильмы️",
                "images": [
                    {"url": "", "caption": "Однажды в Голливуде"},
                    {"url": "", "caption": "Лило и Стич"}
            ]
        },
        {
                "name": "Триллеры/ужасы",
                "description": "Жутко жутко",
                "images": [
                    {"url": "", "caption": "СолнцеСтояние"},
                    {"url": "", "caption": "Левиафан"},
                    {"url": "", "caption": "Носферату"}
            ]
        },
        {
                "name": "Драма",
                "description": "Будем плакать вместе?️",
                "images": [
                    {"url": "", "caption": "Похороните меня за плинтусом"},
                    {"url": "", "caption": "Сказочник"},
                    {"url": "", "caption": "Трудности перевода"},
                    {"url": "", "caption": "Вечное сияние чистого разума"},
                    {"url": "", "caption": "Искупление"},
                    {"url": "", "caption": "Мальчик в полосатой пижаме"},
                    {"url": "", "caption": "Список Шиндлера"},
                    {"url": "", "caption": "Эдвард руки-ножницы"}
            ]
        },
        {
                "name": "Мультики",
                "description": "Милый вечерочек️",
                "images": [
                    {"url": "", "caption": "Остров собак"},
                    {"url": "", "caption": "Кошмар перед Рождеством"},
                    {"url": "", "caption": "Труп невесты"},
                    {"url": "", "caption": "Дикий робот"},
                    {"url": "", "caption": "Меч в камне"}
            ]
        },
        {
                "name": "Сериалы",
                "description": "Засядем дома под одеялком️",
                "images": [
                    {"url": "", "caption": "Игра престолов"},
                    {"url": "", "caption": "Атланта"}
            ]
        }

    ]
}

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Приветик! Наконец-то ты в Петербурге))) Здесь я накидала вариантики для нашего досуга.\n\n"
        "Выбери категорию, а потом интересующий вариант!\n\n"
        "📌 Доступные команды:\n"
        "/menu — Главное меню\n"
        "/restart — Перезапуск"
    )
    await update.message.reply_text(text)
    await show_categories(update)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_categories(update)

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def show_categories(update_or_query):
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat|{cat}")] for cat in categories]
    markup = InlineKeyboardMarkup(keyboard)
    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text("Чего бы из этого тебе хотелось:", reply_markup=markup)
    else:
        await update_or_query.edit_message_text("Чего бы из этого тебе хотелось:", reply_markup=markup)

async def show_variants(category, query):
    items = categories.get(category, [])
    keyboard = [[InlineKeyboardButton(item["name"], callback_data=f"item|{category}|{i}")]
                for i, item in enumerate(items)]
    keyboard.append([InlineKeyboardButton("⬅ Назад", callback_data="back_to_menu")])
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Варианты для категории *{category}*:", reply_markup=markup, parse_mode='Markdown')

async def show_item_detail(category, index, query):
    item = categories[category][int(index)]
    media = []
    for image in item['images']:
        media.append(InputMediaPhoto(media=image['url'], caption=image['caption'], parse_mode='Markdown'))

    await query.message.delete()
    await query.message.chat.send_media_group(media=media)

    keyboard = [[InlineKeyboardButton("⬅ Назад", callback_data=f"cat|{category}")]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.message.chat.send_message("Выберите следующий шаг:", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_menu":
        await show_categories(query)
    elif data.startswith("cat|"):
        category = data.split("|")[1]
        await show_variants(category, query)
    elif data.startswith("item|"):
        _, category, index = data.split("|")
        await show_item_detail(category, index, query)

# Получение file_id
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await update.message.reply_text(f"file_id: {file_id}")
    elif update.message.document:
        file_id = update.message.document.file_id
        await update.message.reply_text(f"file_id: {file_id}")
    else:
        await update.message.reply_text("Это не картинка. Пришли фото или документ.")

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("menu", menu))
application.add_handler(CommandHandler("restart", restart))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_file_id))

# Flask webhook
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return 'ok'

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    app.run(port=5000)