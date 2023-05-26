import math
import telebot
from dotenv import load_dotenv
import os
from DataBase import name_search, ingredients_search, category_search, repeat_name_serch, add_user, add_to_favorite, output_list, output_one1, delete_from_favorite, random_recipe
from telebot import types
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start']) #стартовая команда
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('команды')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Привет, я кулинарный бот, который поможет вам найти рецепт для приготовления различных блюд", reply_markup=markup)
    user_id = message.chat.id
    new_user(user_id)
def new_user(user_id):
    add_user(user_id)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'команды':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')
        btn4 = types.KeyboardButton('избранное')
        btn5 = types.KeyboardButton('случайный рецепт')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.from_user.id, "Я могу осуществлять поиск кулинарных рецептов по названию, составу, категории.", reply_markup=markup)
    elif message.text == 'поиск по названию':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, 'Введите название рецепта, который ищите')
        bot.register_next_step_handler(msg, process_name_search)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')
        btn4 = types.KeyboardButton('избранное')
        markup.add(btn1, btn2, btn3, btn4)
    elif message.text == 'поиск по категориям':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, 'Введите название категорий через запятую и пробел, по которым ищите рецепты. '
                                                'Пример ввода: Мясо, На ужин')
        bot.register_next_step_handler(msg, process_category_search)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')
        btn4 = types.KeyboardButton('избранное')
        markup.add(btn1, btn2, btn3, btn4)
    elif message.text == 'поиск по ингредиентам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, 'Введите название ингредиентов через запятую и пробел, по которым ищите рецепты. '
                                                'Пример ввода: Помидор, Картофель')
        bot.register_next_step_handler(msg, process_ingredients_search)
        btn1 = types.KeyboardButton('поиск по названию')
        btn2 = types.KeyboardButton('поиск по категориям')
        btn3 = types.KeyboardButton('поиск по ингредиентам')
        btn4 = types.KeyboardButton('избранное')
        markup.add(btn1, btn2, btn3, btn4)
    elif message.text == 'избранное':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        user_id = message.chat.id
        output_favorite(user_id)
        btn1 = types.InlineKeyboardButton('удалить')
        btn2 = types.InlineKeyboardButton('вывести')
        btn3 = types.InlineKeyboardButton('команды')
        keyboard.add(btn1, btn2, btn3)
        markup1.add(btn1, btn2, btn3)
    elif message.text == 'случайный рецепт':
        data = random_recipe()
        bot.send_message(message.chat.id, data)
        ms = bot.send_message(message.chat.id, 'Добавить в избранное? (Да или Нет)')
        bot.register_next_step_handler(ms, add_to_favorites, data[1])

def process_name_search(message):
    try:
        print('msg', message.text)
        information = name_search(message.text)
        i = len(information)
        a = 1
        bot.send_message(message.chat.id, information[0])
        if i <= 1:
            ms = bot.send_message(message.chat.id, 'Введите номер рецепта из списка')
            bot.register_next_step_handler(ms, test3, information, a)
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

# def test(message, information):
#     try:
#         mess = int(message.text)
#         information = information.split('.')
#         data = repeat_name_serch(information[mess])
#         bot.send_message(message.chat.id, data)
#     except Exception as e:
#         print(e)

def test3(message, information, a):
    try:
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
        ms = bot.send_message(message.chat.id, 'Добавить в избранное? (Да или Нет)')
        bot.register_next_step_handler(ms, add_to_favorites, data[1])
    except Exception as e:
        print(e)

def test2(message, information, a):
    try:
        text = message.text
        b = len(information)
        if text == 'Да' or text == 'дв' or text == 'да' or text == 'lf' and a<b:
            bot.send_message(message.chat.id, information[a])
            a = a+1
            if a <b:
                ms = bot.send_message(message.chat.id, 'Показать еще? (Да или Нет)')
                bot.register_next_step_handler(ms, test2, information, a)
            else:
                ms = bot.send_message(message.chat.id, 'Введите номер рецепта')
                bot.register_next_step_handler(ms, test3, information, a-1)
        elif text == 'Нет' or text == 'нет' or text == 'ytn' or a==b:
            ms = bot.send_message(message.chat.id, 'Введите номер рецепта')
            bot.register_next_step_handler(ms, test3, information, a)
        else:
            ms = bot.send_message(message.chat.id, 'Введите (Да или Нет)')
            bot.register_next_step_handler(ms, test2, information, a)
    except Exception as e:
        print(e)
def add_to_favorites(message, data):
    try:
        text = message.text.lower()
        user_id = message.chat.id
        if text == 'дв' or text == 'да' or text == 'lf':
            flag = add_to_favorite(user_id, data)
            if flag == False:
                bot.send_message(message.chat.id, 'Рецепт успешно добавлен')
            else:
                bot.send_message(message.chat.id, 'Рецепт уже был добавлен или произошла ошибка')
        elif text == 'нет' or text == 'ytn':
            pass
        else:
            ms = bot.send_message(message.chat.id, 'Не понял... Напишите да или нет')
            bot.register_next_step_handler(ms, add_to_favorite, data)
    except Exception as e:
        print(e)

def output_favorite(user_id):
    try:
        data = output_list(user_id)
        bot.send_message(user_id, data[0])
        ms = bot.send_message(user_id, 'Желаете удалить (1)' + '\n' + 'Вывести один из рецептов  (2)' + '\n'  + 'Иначе напишите "нет"')
        bot.register_next_step_handler(ms, check, data[1])
    except Exception as e:
        print(e)

def check(message, data):
    try:
        user_id = message.chat.id
        text = message.text.lower()
        if text == '2':
            ms = bot.send_message(user_id, "Напишите номер рецепта, который хотите вывести")
            bot.register_next_step_handler(ms, output_one, data)
        elif text == '1':
            ms = bot.send_message(user_id, "Напишите номер рецепта, который хотите удалить")
            bot.register_next_step_handler(ms, delete_one, data)
        elif text == 'нет' or text == 'ytn':
            pass
        else:
            pass
    except Exception as e:
        print(e)
def output_one(message, data):
    try:
        text = message.text
        text = int(text)
        if text >=1 and text <= len(data):
            result = output_one1(data[text-1])
            bot.send_message(message.chat.id, result)
        else:
            ms = bot.send_message(message.chat.id, "Ошибка, введите правильно номер рецепта из списка")
            bot.register_next_step_handler(ms, output_one, data)
    except Exception as e:
        print(e)

def delete_one(message, data):
    try:
        text = message.text
        user_id = message.chat.id
        text = int(text)
        if text >= 1 and text <= len(data):
            result = delete_from_favorite(user_id, data[text - 1])
            bot.send_message(message.chat.id, result)
            a = output_list(user_id)
            bot.send_message(user_id, a[0])
        else:
            ms = bot.send_message(message.chat.id, "Ошибка, введите правильно номер рецепта из списка")
            bot.register_next_step_handler(ms, output_one, data)
    except Exception as e:
        print(e)
bot.polling(none_stop=True, interval=0)
bot.delete_webhook()
