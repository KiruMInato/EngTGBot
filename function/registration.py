from bots import config
from db.db import database
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
from bots import main
from function import groups

bot = config.bot
class User:
    name=None
    role=None
    tg_name=None

    def set_name(self, name):
        self.name=name

    def set_role(self, role):
        self.role=role

    def set_tg_name(self, tg_name):
        self.tg_name=tg_name
user=User()
def start_registration(message):
    bot.send_photo(message.chat.id, open('../photo/Do you speak english.jpg', 'rb'),
                               caption=f'Добро пожаловать, {message.from_user.first_name}!\n'
                                       f'P.S.: вы не сможете пользоваться ботом, если у вас скрыт ЮЗ TG!', reply_markup=nav.start_registration)

def user_name(message, role):
            global name
            name = message.text.strip()
            user.set_tg_name(message.from_user.username)
            user.set_name(name)
            user.set_role(role)
            if user.role == 'Student':
                bot.send_message(message.chat.id, 'Выберите номер вашего класса:', reply_markup=nav.set_students_grade)
            elif user.role == 'Teacher':

                bot.send_message(message.chat.id, 'Введите ваши классы и их литеры(буквы)\nПример:\n 10 Б, 11 Г, 4 А, 7 В\nСледуйте четко по шаблону!\nПосле класса пробел и потом буква!')

def grade_and_letters_of_teacher_groups(message):
    if message.text and not message.text.startswith('/'):
        teacher_id=database.insert_tg_name_and_name_and_role(user.tg_name, user.name, user.role)
        groups.set_grades_and_letters(message, teacher_id)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите по шаблону: 10 Б, 11 Г, 4 А, 7 В")
        bot.register_next_step_handler(message, grade_and_letters_of_teacher_groups)


