

from function import registration
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import bot
from function import groups
from buttons import markups_of_registration as nav




name = None
role = None
grade = None

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

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    global role
    if message.text == 'А':
        bot.send_message(message.chat.id, "Вы выбрали А класс! Завершаю регистрацию...", reply_markup=nav.remove_registration_set_letter)
        groups.user_letter(message)
    if message.text == 'Б':
        bot.send_message(message.chat.id, "Вы выбрали Б класс! Завершаю регистрацию...", reply_markup=nav.remove_registration_set_letter)
        groups.user_letter(message)
    if message.text == 'Student':
        role = 'Student'
        bot.send_message(message.chat.id, "Отлично, теперь введите ФИО:", reply_markup=nav.remove_registration_set_role)
        bot.register_next_step_handler(message, reg2)
    if message.text == 'Teacher':
        role = 'Teacher'
        bot.send_message(message.chat.id, "Отлично, теперь введите ФИО:", reply_markup=nav.remove_registration_set_role)
        bot.register_next_step_handler(message, reg2)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
        global role
        global grade
        if call.data == "registration":
            bot.send_message(call.message.chat.id, f'Кем вы являетесь?', reply_markup=nav.registration_set_role)
        if call.data == '5':
            grade = 5
            bot.send_message(call.message.chat.id, 'Вы выбрали 5 класс!')
            groups.user_grade(call, grade)
        if call.data == '6':
            grade = 6
            bot.send_message(call.message.chat.id, 'Вы выбрали 6 класс!')
            groups.user_grade(call, grade)
        if call.data == '7':
            grade = 7
            bot.send_message(call.message.chat.id, 'Вы выбрали 7 класс!')
            groups.user_grade(call, grade)
        if call.data == '8':
            grade = 8
            bot.send_message(call.message.chat.id, 'Вы выбрали 8 класс!')
            groups.user_grade(call, grade)
        if call.data == '9':
            grade = 9
            bot.send_message(call.message.chat.id, 'Вы выбрали 9 класс!')
            groups.user_grade(call, grade)
        if call.data == '10':
            grade = 10
            bot.send_message(call.message.chat.id, 'Вы выбрали 10 класс!')
            groups.user_grade(call, grade)
        if call.data == '11':
            grade = 11
            bot.send_message(call.message.chat.id, 'Вы выбрали 11 класс!')
            groups.user_grade(call, grade)
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