from bots import config
from db import database
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
from function import mainMenu
from bots import main
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
    main.status_of_registration = True
    user.set_tg_name(message.from_user.username)
    bot.send_photo(message.chat.id, open('../photo/Do you speak english.jpg', 'rb'),
                               caption=f'Добро пожаловать, {message.from_user.first_name}!', reply_markup=nav.start_registration)

def user_name(message, role):
            global name
            name = message.text.strip()
            user.set_name(name)
            user.set_role(role)
            database.set_name_tgname_role_into_table(user.name, user.role, user.tg_name)
            if user.role == 'Student':
                bot.send_message(message.chat.id, 'Выберите номер вашего класса:', reply_markup=nav.set_students_grade)
            elif user.role == 'Teacher':
                bot.send_message(message.chat.id, 'Регистрация прошла успешно!', reply_markup=nav2.run_mainMenu_teacher)
                main.status_of_registration = False
