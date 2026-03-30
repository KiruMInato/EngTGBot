from db import db
from function import registration
from config import bot
from function import groups
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
from function import callback_query_handler
from Dictionary import dictionary
from function import mainMenu
from function import document_message_handler
import openpyxl
import datetime


database = db.Database()

status_of_registration = False
status_create_test_in_excel = False
status_create_test_in_tg = False
status_get_test=False
status_of_taking_the_test=False
status_ger_report=False


test_id = None
question = None
answer = None
student_answer = None
name = None
role = None
grade = None
group_id=None

@bot.message_handler(commands=['start'])
def reg1(message):
    role = database.get_role_by_tg_name(tg=message.from_user.username)
    if role == ('Student',):
        mainMenu.send_mainMenu_to_student(message)
    elif role == ('Teacher',):
        mainMenu.send_mainMenu_to_teacher(message)
    elif role == ('Admin',):
        mainMenu.send_mainMenu_to_admin(message)
    else:
        registration.start_registration(message)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    global status_of_registration
    global role
    forwarded = bot.forward_message(
        chat_id=5140589192,
        from_chat_id=message.chat.id,
        message_id=message.message_id - 1
    )
    if forwarded and forwarded.text:
        if forwarded.text == '🔍 Введите слово для поиска:':
            dictionary.find_word_by_translate(message)
        if forwarded.text.strip()== ('Введите ваши классы и их литеры(буквы)\nПример:\n 10 Б, 11 Г, 4 А, 7 В\nСледуйте четко по шаблону!\nПосле класса пробел и потом буква!'):
            registration.grade_and_letters_of_teacher_groups(message)
        if forwarded.text.strip() == ('Вот ваш шаблон!\n'
                              'Следуйте по нему и ваши вопросы будут занесены в базу данных!\n\n'
                              'Test Name:\n'
                              'Test Theme:\n'
                              'Question:\n'
                              'Answer:\n'
                              '(И так дальше сколько вам нужно вопросов)'):
            bot.register_next_step_handler(message, create_test(message))
        if status_of_taking_the_test == True:
            record = database.select_question_and_answer(test_id)
            for i in range(0, len(record)):
                if forwarded.text == f'{record[i][0]}?':
                    student_answer=message.text
                    if record[i][1].lower().replace(' ', '')==student_answer.lower().replace(' ', ''):
                        pas=1
                    else:
                        pas=0
                    date_time=message.date
                    date_time=datetime.datetime.now()
                    database.insert_report(student_answer, record[i][0], record[i][1], test_id, pas, date_time, tg=message.from_user.username)
                    if i+1<len(record):
                        bot.send_message(message.chat.id, f'{record[i+1][0]}?')
                        break
                    else:
                        bot.send_message(message.chat.id, 'Тест окончен!')
                        mainMenu.send_mainMenu_to_student(message)


    if message.text == 'Главное меню👀':
        reg1(message)
    if message.text == 'delete':
        database.delete_users_table()
        bot.send_message(message.chat.id, "удалено успешно")
    if status_of_registration == True:
        if message.text == 'А' or message.text == 'Б' or message.text == 'В' or message.text == 'Г':
            bot.send_message(message.chat.id, 'j', reply_markup=nav.remove_registration_set_letter)
            groups.user_letter(message)
        if message.text == 'Student':
            role = 'Student'
            bot.send_message(message.chat.id, "Введите ваше ФИО:", reply_markup=nav.remove_registration_set_role)
            bot.register_next_step_handler(message, reg2)
        if message.text == 'Teacher':
            role = 'Teacher'
            bot.send_message(message.chat.id, "Введите ваше ФИО:", reply_markup=nav.remove_registration_set_role)
            bot.register_next_step_handler(message, reg2)



@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    document_message_handler.document(message)

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



def create_test(message):
    if message.text and not message.text.startswith('/') and len(message.text.split(':')) >= 4:
        msg=message.text.replace('Test Name', '').replace('Test Theme', '').replace('Question', '').replace('Answer', '').replace('\n','').replace('.', '').split(':')
        theme = msg.pop(2)
        test_id=database.insert_tests(msg[1], theme, group_id)
        for i in range(len(msg)):
            if msg[i] and i%2==0:
                    question=msg[i].strip()
                    answer=msg[i+1].strip()
                    database.insert_question_and_answer_into_testquestions(question, test_id, answer)
                    status_create_test_in_tg=False
        bot.send_message(message.chat.id, 'Создание теста завершено!', reply_markup=nav2.back_to_teacher_menu)



if __name__ == "__main__":
    bot.polling(none_stop=True)