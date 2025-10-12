from function import registration
import telebot
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from telebot import types



bot = telebot.TeleBot('8389909764:AAFYb8P0mgWwusXF7GZ3tav0uzDGlhimfws')

name = None
role = None

try:
    connection = psycopg2.connect(user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)

@bot.message_handler(commands=['start'])
def reg1(message):
    registration.start_registration(message)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
        global role
        if call.data == "registration":
                markup1 = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Student', callback_data='student')
                btn2 = types.InlineKeyboardButton('Teacher', callback_data='teacher')
                markup1.add(btn1, btn2)
                bot.send_message(call.message.chat.id, f'Кем вы являетесь?', reply_markup=markup1)
        if call.data == "student":
            role = 'Student'
            bot.answer_callback_query(call.id, "Вы выбрали Ученик!")
            bot.send_message(call.message.chat.id, "Отлично, теперь введите имя и фамилию:")
            bot.register_next_step_handler(call.message, reg2)
        if call.data == "teacher":
            role = 'Teacher'
            bot.answer_callback_query(call.id, "Вы выбрали Учитель!")
            bot.send_message(call.message.chat.id, "Отлично, теперь введите ФИО:")
            bot.register_next_step_handler(call.message, reg2)
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

def reg2(message):
    global role
    if message.text and not message.text.startswith('/'):
        registration.user_name(message, role)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите ваше имя:")
        bot.register_next_step_handler(message, reg2)

if __name__ == "__main__":
    bot.polling(none_stop=True)