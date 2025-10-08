

import telebot
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from telebot import types
from telebot.types import InlineKeyboardMarkup

bot = telebot.TeleBot('8389909764:AAFYb8P0mgWwusXF7GZ3tav0uzDGlhimfws')

name = None

try:
    connection = psycopg2.connect(user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)


@bot.message_handler(commands=['start'])
def info(message):

    tg=message.from_user.username
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
    cursor.execute('SELECT tg_name FROM users WHERE LOWER(tg_name) = LOWER(\'%s\')'% str(tg))
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

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "registration":
        bot.send_message(call.message.chat.id, f'Введите своё имя:')
        bot.register_next_step_handler(call.message, user_name)
    if call.data == 'users':
        connection = psycopg2.connect(user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726",
                                  database="EngTGBot")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        info = ''
        for el in users:
            info += f'Имя: {el[1]}| TG: {el[2]}| Role: {el[3]}\n'
        cursor.close()
        connection.close()
        bot.send_message(call.message.chat.id, info)


def user_name(message):
    global name
    name = message.text.strip()
    connection = psycopg2.connect(
       user="postgres",
       password="sk1726ks",
       host="localhost",
       port="1726",
       database="EngTGBot")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (name, tg_name, role) VALUES (%s, %s, %s)', (name, message.from_user.username, 'User'))
    connection.commit()
    cursor.close()
    connection.close()
    markup = types.InlineKeyboardMarkup()
    btn=types.InlineKeyboardButton('Список пользователей', callback_data='users')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Регистрация прошла успешно!', reply_markup=markup)



if __name__ == "__main__":
    bot.polling(none_stop=True)

