import telebot
from bots import config
from buttons import markups_of_mainMenu as nav2


bot=config.bot


def send_mainMenu_to_student(message):
    bot.send_photo(message.chat.id, open('../photo/mainMenu_student.jpg', 'rb'),
                               caption=f'Добро пожаловать, {message.from_user.first_name}!', reply_markup=nav2.remove_run_mainMenu_student and nav2.mainMenu_student)


def send_mainMenu_to_teacher(message):
    bot.send_photo(message.chat.id, open('../photo/mainMenu_teacher.jpg', 'rb'),
                   caption=f'Добро пожаловать, {message.from_user.first_name}!', reply_markup=nav2.remove_run_mainMenu_teacher and nav2.mainMenu_teacher)



def send_mainMenu_to_admin(message):
    bot.send_photo(message.chat.id, open('../photo/mainMenu_admin.jpg', 'rb'),
                   caption=f'Добро пожаловать, {message.from_user.first_name}!')

