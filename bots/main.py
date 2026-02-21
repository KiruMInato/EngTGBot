import db
from function import registration
from config import bot
from function import groups
from buttons import markups_of_registration as nav
from function import callback_query_handler
from Dictionary import dictionary
from function import mainMenu

database=db.Database()
status_of_registration = False
name = None
role = None
grade = None

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
    global status_of_registration, find_word_by_translate_status
    global role
    forwarded = bot.forward_message(
        chat_id=5140589192,
        from_chat_id=message.chat.id,
        message_id=message.message_id - 1
    )
    if forwarded and forwarded.text:
        if forwarded.text == '🔍 Введите слово для поиска:':
            dictionary.find_word_by_translate(message)
        if forwarded.text.strip() == ('Вот ваш шаблон!\n'
                              'Следуйте по нему и ваши вопосы будут занесены в базу данных!\n\n'
                              ' Test Name:\n'
                              ' Question:\n'
                              ' Answer:\n'
                              '(И так дальше сколько вам нужно вопросов)'):
            bot.register_next_step_handler(message, create_test(message))
    if message.text == 'Главное меню👀':
        reg1(message)
    if message.text == 'delete':
        database.delete_users_table()
        bot.send_message(message.chat.id, "удалено успешно")
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
        msg=message.text.replace('Test Name', '').replace('Question', '').replace('Answer', '').replace('\n','').replace('.', '').split(':')
        test_name=msg[1]
        for i in range(len(msg)):
            if msg[i] and i%2==0:
                    question=msg[i]
                    answer=msg[i+1]
                    print(question,'и его ответ', answer)

if __name__ == "__main__":
    bot.polling(none_stop=True)