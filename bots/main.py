import db
from function import registration
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import bot
from function import groups
from buttons import markups_of_registration as nav
from function import callback_query_handler
from function import mainMenu
from Dictionary import dictionary

database=db.Database()
status_of_registration = False
find_word_by_translate_status = False
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
    global status_of_registration, find_word_by_translate_status
    global role
    print(message.id)
    print(message.text, status_of_registration, find_word_by_translate_status)
    if message.text == 'Main Menu':
        registration.start_registration(message)
    if message.text == 'delete':
        database.delete_users_table()
        bot.send_message(message.chat.id, "удалено успешно")
    if find_word_by_translate_status == True:
        bot.register_next_step_handler(message.chat.id, dictionary.find_word_by_translate)
    if status_of_registration == True:
        if message.text == 'А':
            bot.send_message(message.chat.id, "Завершаю регистрацию...", reply_markup=nav.remove_registration_set_letter)
            groups.user_letter(message)
        if message.text == 'Б':
            bot.send_message(message.chat.id, "Завершаю регистрацию...", reply_markup=nav.remove_registration_set_letter)
            groups.user_letter(message)
        if message.text == 'В':
            bot.send_message(message.chat.id, "Завершаю регистрацию...", reply_markup=nav.remove_registration_set_letter)
            groups.user_letter(message)
        if message.text == 'Г':
            bot.send_message(message.chat.id, "Завершаю регистрацию...", reply_markup=nav.remove_registration_set_letter)
            groups.user_letter(message)
        if message.text == 'Student':
            role = 'Student'
            bot.send_message(message.chat.id, "Введите ваше ФИО:", reply_markup=nav.remove_registration_set_role)
            bot.register_next_step_handler(message, reg2)
        if message.text == 'Teacher':
            role = 'Teacher'
            bot.send_message(message.chat.id, "Введите ваше ФИО:", reply_markup=nav.remove_registration_set_role)
            bot.register_next_step_handler(message, reg2)
        message.id -= 1
        print(message.text)
        print(message.id)

        if message.text == '🔍 Введите слово для поиска:':
            bot.register_message_handler(message, dictionary.find_word_by_translate)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    callback_query_handler.callback(call)


def reg2(message):
    global role
    if message.text and not message.text.startswith('/') and len(message.text.split()) == 3:
        registration.user_name(message, role)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите ваше ФИО:")
        bot.register_next_step_handler(message, reg2)

if __name__ == "__main__":
    bot.polling(none_stop=True)