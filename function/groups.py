from bots import config
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
from db.db import database
from bots import main
from telebot import types
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
    set_teacher(message)

def set_teacher(message):
    number_of_teachers = database.get_all_teachers_from_users()
    teachers_button = types.InlineKeyboardMarkup()
    for i in number_of_teachers:
        teachers_button.add(types.InlineKeyboardButton(i[0], callback_data=str(i[0])))
    bot.send_message(message.chat.id, 'Выберите вашего учителя из списка!', reply_markup=teachers_button)

def set_grades_and_letters(message, teacher_id):
    grades_and_letters = message.text.strip().split(',')
    mass = []
    for i in grades_and_letters:
        a=i.split(' ')
        if a[0]=='':
            a.pop(0)
        mass.append(a)
    database.get_teacher_id_and_insert_grade_letter_of_groups(teacher_id, mass)
    bot.send_message(message.chat.id, 'Регистрация прошла успешно!', reply_markup=nav2.run_mainMenu_teacher)
    main.status_of_registration = False