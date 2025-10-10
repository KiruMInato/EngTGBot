import main
import telebot
import psycopg2
from telebot import types


def start_registration(message):
        bot = main.bot
        tg = message.from_user.username
        connection = psycopg2.connect(user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726",
                                  database="EngTGBot")
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS USERS (id serial primary key, name text, tg_name text UNIQUE, role text)')
        connection.commit()
        cursor.close()
        connection.close()
        connection = psycopg2.connect(user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726",
                                  database="EngTGBot")
        cursor = connection.cursor()
        cursor.execute('SELECT tg_name FROM users WHERE LOWER(tg_name) = LOWER(%s)', (tg,))
        record = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        if record is None:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton('Регистрация', callback_data="registration")
            markup.add(btn)
            bot.send_photo(message.chat.id, open('Do you speak english.jpg', 'rb'),
                       caption=f'Добро пожаловать, {message.from_user.first_name}!', reply_markup=markup)
        else:
            bot.send_photo(message.chat.id, open('Do you speak english.jpg', 'rb'),
                       caption=f'Добро пожаловать, {message.from_user.first_name}!')