import psycopg2
import db
from bots import config
from function import groups
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
database=db.Database()
bot=config.bot


def callback(call):
    global role
    global grade
    if call.data == "registration":
        bot.send_message(call.message.chat.id, f'Кем вы являетесь?', reply_markup=nav.registration_set_role)
    if call.data == '5':
        grade = 5
        groups.user_grade(call, grade)
    if call.data == '6':
        grade = 6
        groups.user_grade(call, grade)
    if call.data == '7':
        grade = 7
        groups.user_grade(call, grade)
    if call.data == '8':
        grade = 8
        groups.user_grade(call, grade)
    if call.data == '9':
        grade = 9
        groups.user_grade(call, grade)
    if call.data == '10':
        grade = 10
        groups.user_grade(call, grade)
    if call.data == '11':
        grade = 11
        groups.user_grade(call, grade)
    if call.data == 'users':
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
    if call.data == 'dictionary':
        with open('../photo/mainMenu_dictionary.jpg', 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo=photo, caption=' ', reply_markup=nav2.dictionary)
    if call.data == 'get random words of dictionary':
        database.get_20_random_words(call)
    if call.data == 'find by translation':
        find_word_by_translate_status = True
        bot.send_message(call.message.chat.id, "🔍 Введите слово для поиска:")





