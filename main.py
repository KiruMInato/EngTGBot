

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
        bot.send_photo(message.chat.id, open('Do you speak english.jpg', 'rb'),
                       caption='Пройдите регистрацию')
        bot.register_next_step_handler(message, user_name)

    else:
        bot.send_photo(message.chat.id, open('Do you speak english.jpg', 'rb'),
                       caption=f'Добро пожаловать, {message.from_user.first_name}!')


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

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
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

if __name__ == "__main__":
    bot.polling(none_stop=True)
    # markup = types.InlineKeyboardMarkup()
    # btn = types.InlineKeyboardButton("Ученик", callback_data="student")
    # btn2 = types.InlineKeyboardButton("Учитель", callback_data="teacher")
    # markup.add(btn)
    # markup.add(btn2) , reply_markup=markup
    # @bot.callback_query_handler(func=lambda call: True)
    # def callback(call):
    #     if call.data == "student":
    #         bot.answer_callback_query(call.id, "Вы выбрали Ученик!")
    #         bot.send_message(call.message.chat.id, "Отлично, теперь вы ученик!")
    #     if call.data == "teacher":
    #         bot.answer_callback_query(call.id, "Вы выбрали Учитель!")
    #         bot.send_message(call.message.chat.id, "Отлично, теперь вы учитель!")
