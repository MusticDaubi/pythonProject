import math
import telebot
from dotenv import load_dotenv
import os
from DataBase import name_search, ingredients_search, category_search, repeat_name_serch
from telebot import types
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start']) #стартовая команда
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('команды')
    btn2 = types.KeyboardButton('Не работает')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Привет", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'команды':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, "Я могу осуществлять поиск кулинарных рецептов по названию, составу, категории.", reply_markup=markup)
    elif message.text == 'поиск по названию':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, 'Введите название рецепта, который ищите')
        bot.register_next_step_handler(msg, process_name_search)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')
        markup.add(btn1, btn2, btn3)
    elif message.text == 'поиск по категориям':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, 'Введите название категорий через запятую и пробел, по которым ищите рецепты. '
                                                'Пример ввода: Мясо, На ужин')
        bot.register_next_step_handler(msg, process_category_search)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')

        markup.add(btn1, btn2, btn3)
    elif message.text == 'поиск по ингредиентам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, 'Введите название ингредиентов через запятую и пробел, по которым ищите рецепты. '
                                                'Пример ввода: Помидор, Картофель')
        bot.register_next_step_handler(msg, process_ingredients_search)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')
        markup.add(btn1, btn2, btn3)

def process_name_search(message):
    try:
        print('msg', message.text)
        information = name_search(message.text)
        i = len(information)
        a = 1
        bot.send_message(message.chat.id, information[0])
        if i <= 1:
            ms = bot.send_message(message.chat.id, 'Введите номер рецепта из списка')
            bot.register_next_step_handler(ms, test, information)
        else:
            ms = bot.send_message(message.chat.id,  'Показать еще? (Да или Нет)')
            bot.register_next_step_handler(ms, test2, information, a)
    except Exception as e:
        print('Error name serch ', e)
        bot.reply_to(message, "Ошибка")

def process_category_search(message):
    try:
        print('msg', message.text)
        print('DataBase', name_search)
        information = category_search(message.text)
        i = len(information)
        a = 1
        bot.send_message(message.chat.id, information[0])
        if i <= 1:
            ms = bot.send_message(message.chat.id, 'Введите номер рецепта из списка')
            bot.register_next_step_handler(ms, test3, information, a)
        else:
            ms = bot.send_message(message.chat.id, 'Показать еще? (Да или Нет)')
            bot.register_next_step_handler(ms, test2, information, a)
    except Exception as e:
        print('Error name serch ', e)
        bot.reply_to(message, "Ошибка")

def process_ingredients_search(message):
    try:
        print('msg', message.text)
        print('DataBase', name_search)
        information = ingredients_search(message.text)
        i = len(information)
        a = 1
        bot.send_message(message.chat.id, information[0])
        if i <= 1:
            ms = bot.send_message(message.chat.id, 'Введите номер рецепта из списка')
            bot.register_next_step_handler(ms, test3, information, a)
        else:
            ms = bot.send_message(message.chat.id, 'Показать еще? (Да или Нет)')
            bot.register_next_step_handler(ms, test2, information, a)
    except Exception as e:
        print('Error name serch ', e)
        bot.reply_to(message, "Ошибка")

def test(message, information):
    mess = int(message.text)
    information = information.split('.')
    data = repeat_name_serch(information[mess])
    bot.send_message(message.chat.id, data)

def test3(message, information, a):
    mess = int(message.text)
    b = math.ceil(mess/15)
    if mess <=15:
        mess = mess
    elif mess > 15 and mess % 15 != 0:
        mess = mess % 15
    elif mess > 15 and mess % 15 == 0:
        mess= 15
    information = information[b-1].split('.')
    data = repeat_name_serch(information[mess])
    bot.send_message(message.chat.id, data)

def test2(message, information, a):
    text = message.text
    b = len(information)
    if text == 'Да' or text == 'да' and a<b:
        bot.send_message(message.chat.id, information[a])
        a = a+1
        if a <b:
            ms = bot.send_message(message.chat.id, 'Показать еще? (Да или Нет)')
            bot.register_next_step_handler(ms, test2, information, a)
        else:
            ms = bot.send_message(message.chat.id, 'Введите номер рецепта')
            bot.register_next_step_handler(ms, test3, information, a-1)
    elif text == 'Нет' or text == 'нет' or a==b:
        ms = bot.send_message(message.chat.id, 'Введите номер рецепта')
        bot.register_next_step_handler(ms, test3, information, a)
    else:
        ms = bot.send_message(message.chat.id, 'Введите (Да или Нет)')
        bot.register_next_step_handler(ms, test2, information, a)

bot.polling(none_stop=True, interval=0)
# bot.delete_webhook()
