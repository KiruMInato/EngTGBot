from bots import main
import telebot
import psycopg2
from telebot import types
from bots import config
from psycopg2 import Error
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
from db import database
from bots import main

bot=config.bot
id = None
class Group:
    userId = None
    letter = None
    grade = None
    def set_grade(self, grade):
        self.grade=grade

    def set_letter(self, letter):
        self.letter=letter
group=Group()
def user_grade(call, grade):
    global letter
    group.set_grade(grade)
    bot.send_message(call.message.chat.id, "Буква вашего класса!", reply_markup=nav.registration_set_letter)

def user_letter(message):
    bot=config.bot
    global letter
    letter = message.text.strip()
    group.set_letter(letter)
    database.insert_userId_letter_grade_into_groups(group.grade, group.letter)
    bot.send_message(message.chat.id, 'Регистрация прошла успешно!', reply_markup=nav2.run_mainMenu_student)
    main.status_of_registration = False