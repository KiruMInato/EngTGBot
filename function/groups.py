
from bots import main
import telebot
import psycopg2
from telebot import types
from bots import config
from psycopg2 import Error
from buttons import markups_of_registration as nav
from db import database



bot=config.bot
id = None
class Group:
    userId = None
    letter = None
    grade = None
    def set_grade(self, grade):
        self.grade=grade

    def set_userId(self, userId):
        self.userId=userId

    def set_letter(self, letter):
        self.letter=letter
group=Group()
def user_grade(call, grade):
    bot=config.bot
    global letter
    record = database.select_id_from_users(id)
    group.set_grade(grade)
    group.set_userId(record)
    bot.send_message(call.message.chat.id, "Буква вашего класса!", reply_markup=nav.registration_set_letter)





def user_letter(message):
    bot=config.bot
    global letter
    letter = message.text.strip()
    group.set_letter(letter)
    database.insert_userId_letter_grade_into_groups(group.userId, group.grade, group.letter)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Список пользователей', callback_data='users')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Регистрация прошла успешно!', reply_markup=markup)