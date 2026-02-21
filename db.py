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

    def set_name_tgname_role_into_table(self, name, role, tg_name):
        with psycopg2.connect(dbname="EngTGBot",
                                user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('INSERT INTO users (name, tg_name, role) VALUES (%s, %s, %s)',
                               (name, tg_name, role))
                return True

    def select_id_from_users(self, id):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT id FROM users', (id,))
                record = cursor.fetchone()
                return record

    def insert_userId_letter_grade_into_groups(self, userId, grade, letter):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('INSERT INTO groups (userid, grade, letter) VALUES (%s, %s, %s)',
                           (userId, grade, letter))
                return True

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

    def get_teacher_id_from_student(self, tg):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT teacherid FROM groups JOIN users on groups.userid=users.id WHERE users.tg_name=%s', (tg, ))
                record=cursor.fetchone()
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

    def insert_teacherid_to_student_into_groups(self, name):
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT teacherid FROM groups JOIN users on groups.userid=users.id WHERE users.name=%s', (name, ))
                teacher_id=cursor.fetchone()
                cursor.execute('INSERT INTO groups(teacherid) VALUES (%s)', (teacher_id, ))

database = Database()