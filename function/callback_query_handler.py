import psycopg2
from db import db
from bots import config
from function import groups
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
from telebot import types

database= db.Database()
bot=config.bot


def callback(call):
    global role
    global grade
    if call.data == "registration":
        bot.send_message(call.message.chat.id, f'Кем вы являетесь?', reply_markup=nav.registration_set_role)
    elif call.data == '5':
        grade = 5
        groups.user_grade(call, grade)
    elif call.data == '6':
        grade = 6
        groups.user_grade(call, grade)
    elif call.data == '7':
        grade = 7
        groups.user_grade(call, grade)
    elif call.data == '8':
        grade = 8
        groups.user_grade(call, grade)
    elif call.data == '9':
        grade = 9
        groups.user_grade(call, grade)
    elif call.data == '10':
        grade = 10
        groups.user_grade(call, grade)
    elif call.data == '11':
        grade = 11
        groups.user_grade(call, grade)
    elif call.data == 'users':
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
    elif call.data == 'dictionary':
        with open('../photo/mainMenu_dictionary.jpg', 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo=photo, caption=' ', reply_markup=nav2.dictionary)
    elif call.data == 'get random words of dictionary':
        database.get_20_random_words(call)
    elif call.data == 'find word':
        bot.send_message(call.message.chat.id, "🔍 Введите слово для поиска:")
    elif call.data == 'create_test_for_student':
        bot.send_message(call.message.chat.id, 'Выберите тип создания теста', reply_markup=nav2.create_test_type)
    elif call.data == 'create_test_in_tg':
        bot.send_message(call.message.chat.id, f'Вот ваш шаблон!\n'
                                               'Следуйте по нему и ваши вопросы будут занесены в базу данных!\n\n'
                                               'Test Name:\n'
                                               'Test Theme:\n'
                                               'Question:\n'
                                               'Answer:\n'
                                               '(И так дальше сколько вам нужно вопросов)')
    elif call.data == 'get_test':
        tg=call.message.from_user.username
        record = database.get_teacher_id_from_student(tg)
        if record==None:
            number_of_teachers=database.get_all_teachers_from_users()
            teachers_button=types.InlineKeyboardMarkup()
            for i in number_of_teachers:
                teachers_button.add(types.InlineKeyboardButton(i[0], callback_data=str(i[0])))
            bot.send_message(call.message.chat.id, 'Выберите вашего учителя из списка!', reply_markup=teachers_button)
        else:
            pass
    elif call.data=='see_all_groups':
        tg=call.message.from_user.username
        record = database.get_grade_and_letter_from_teacher(tg)
        print(record)


    else:
        number_of_teachers = database.get_all_teachers_from_users()
        for i in number_of_teachers:
            if call.data==str(i):
                name=i[0]
                database.insert_teacherid_to_student_into_groups(name)