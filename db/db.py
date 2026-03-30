from os.path import curdir

import psycopg2
from bots import config
bot = config.bot


#distinct-убрать дубли

class Database:
    connection = None
    cursor = None
    def __init__(self):
        pass

    def get_role_by_tg_name(self, tg):
        with psycopg2.connect(dbname="EngTGBot",
                user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT role FROM users WHERE tg_name=%s', (tg,))
                role = cursor.fetchone()
                return role

    def add_words_bulk(self, words_list):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.executemany(
                    'INSERT INTO dictionary (word, translate, transcription) VALUES (%s, %s, %s)',
                    words_list
                )
        print(f"Добавлено {len(words_list)} слов в словарь")

    def get_20_random_words(self, call):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute("SELECT word, translate, transcription FROM dictionary ORDER BY RANDOM() LIMIT 20")
                words = cursor.fetchall()

                response = "🎲 20 случайных слов:\n\n"
                for i, (word, translate, transcription) in enumerate(words, 1):
                    response += f"{i}. {word} - {translate} - {transcription}\n"
                bot.send_message(call.message.chat.id, response)

    def find_word_by_translate(self, word):
        with psycopg2.connect(dbname="EngTGBot",
                          user="postgres",
                          password="sk1726ks",
                          host="localhost",
                          port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('''SELECT word, translate, transcription
                        FROM dictionary
                        WHERE translate LIKE %s
                        OR translate LIKE %s
                        OR translate LIKE %s''',
                        (f'%{word}%', f'%{word},%', f'%, {word},%'))
                result = cursor.fetchall()
                if not result:
                    cursor.execute('''SELECT word, translate, transcription 
                                            FROM dictionary 
                                            WHERE word = %s 
                                            ''',
                                   (word, ))
                    result = cursor.fetchall()
                return result

    def delete_users_table(self):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                tg="KMirado"
                cursor.execute('DELETE FROM users WHERE tg_name=%s', (tg, ))
                # cursor.execute('DELETE FROM groups')

    def get_teacher_id_from_student(self, tg):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT group_id FROM users WHERE tg_name=%s', (tg, ))
                group_id=cursor.fetchone()
                cursor.execute('SELECT test_id, test_name, theme FROM tests JOIN groups on groups.group_id=tests.group_id WHERE groups.group_id=%s', (group_id, ))
                record=cursor.fetchall()
                return record

    def get_grade_and_letter_from_teacher(self, tg):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT grade, letter FROM groups JOIN users on groups.teacher_id=users.id WHERE users.tg_name=%s', (tg, ))
                record=cursor.fetchall()
                return record

    def  get_all_teachers_from_users(self):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                role="Teacher"
                cursor.execute('SELECT name FROM users WHERE role=%s', (role, ))
                record=cursor.fetchall()
                return record

    def select_teacherid_to_student_into_groups(self, name, grade, letter, tg, name_student, role, message):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:

                cursor.execute('SELECT teacher_id FROM groups JOIN users on groups.teacher_id=users.id WHERE users.name=%s', (name, ))
                teacher_id=cursor.fetchone()
                cursor.execute('SELECT group_id FROM groups WHERE teacher_id=%s and grade=%s and letter=%s', (teacher_id, grade, letter, ))
                group_id=cursor.fetchone()
                if group_id:
                    cursor.execute('INSERT INTO users (name, tg_name, role) VALUES (%s, %s, %s)',
                                   (name_student, tg, role))
                    cursor.execute('UPDATE users SET group_id=%s WHERE tg_name=%s', (group_id, tg, ))
                else:
                    bot.send_message(message.chat.id, 'Группы с такими классами и литерами не найдены!\n'
                                                      'Возможно вы выбрали не правильные или учитель не создал подходящую группу.\n'
                                                      'Попробуйте начать регистрацию с момента выбора класса. (имя и роль уже внесены в бауз данных)\n'
                                                      'Если не получается и выдает ошибку, то решите проблему с учителем.\n'
                                                      'В противном случае напишите в тех. поддержку, написав комманду /support')
                return group_id

    def insert_tg_name_and_name_and_role(self, tg_name, name, role):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('INSERT INTO users(name, tg_name, role) VALUES (%s, %s, %s)', (name, tg_name, role, ))
                cursor.execute('SELECT id FROM users WHERE tg_name=%s', (tg_name, ))
                teacher_id = cursor.fetchone()
                return teacher_id

    def get_teacher_id_and_insert_grade_letter_of_groups(self, teacher_id, mass):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                for i in mass:
                    cursor.execute('INSERT INTO groups(teacher_id, grade, letter) VALUES (%s, %s, %s)', (teacher_id, i[0], i[1], ))

    def insert_tests(self, test_name, theme, group_id):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('INSERT INTO tests(test_name, theme, group_id) VALUES (%s, %s, %s)', (test_name, theme, group_id, ))
                cursor.execute('SELECT test_id FROM tests WHERE test_name=%s and theme=%s and group_id=%s', (test_name, theme, str(group_id), ))
                test_id=cursor.fetchone()
                return test_id

    def get_grade_letter_of_group(self, tg):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT groups.group_id, grade, letter FROM groups JOIN users on groups.teacher_id=users.id WHERE tg_name=%s', (tg, ))
                record=cursor.fetchall()
                return record

    def insert_question_and_answer_into_testquestions(self,question, test_id, answer):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('INSERT INTO testquestions(test_id, question, answer) VALUES (%s, %s, %s)', (test_id, str(question), str(answer), ))

    def select_question_and_answer(self, test_id):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT question, answer FROM testquestions WHERE test_id=%s', (test_id, ))
                record = cursor.fetchall()
                return record

    def insert_report(self, student_answer, question, answer, test_id, pas, date_time, tg):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT id FROM users WHERE tg_name=%s', (tg, ))
                student_id=cursor.fetchone()
                cursor.execute('SELECT question_id FROM testquestions WHERE question=%s and answer=%s and test_id=%s', (question, answer, test_id, ))
                question_id=cursor.fetchone()
                cursor.execute('INSERT INTO reports (test_id, student_id, date_time, question_id, answer, pass) VALUES (%s, %s, %s, %s, %s, %s)', (test_id, student_id, date_time, question_id, student_answer, pas))
    def select_test_from_group_id(self, group_id):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT test_id, test_name, theme FROM tests JOIN groups on groups.group_id=tests.group_id WHERE groups.group_id=%s', (group_id, ))
                test_id=cursor.fetchall()
                return test_id

    def select_student_id_date_time_pass_from_reports(self, test_id):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT student_id, date_time, pass, question_id FROM reports WHERE test_id=%s', (test_id, ))
                record=cursor.fetchall()
                return record

    def select_name_from_users(self, id):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT name FROM users WHERE id=%s', (id, ))
                name=cursor.fetchone()
                return name



database = Database()