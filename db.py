import psycopg2






class Database:
    connection = None
    cursor = None
    def __init__(self):
        pass

    def get_record_by_tg_name(self, tg):
        with psycopg2.connect(dbname="EngTGBot",
                user="postgres",
                                  password="sk1726ks",
                                  host="localhost",
                                  port="1726") as con:
            with con.cursor() as cursor:
                cursor.execute('SELECT users.\"tg_name\" FROM users WHERE LOWER(users.\"tg_name\") = LOWER(%s)', (tg,))
                record = cursor.fetchone()
                return record

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
        """Массовое добавление слов"""
        with psycopg2.connect(dbname="EngTGBot",
                              user="postgres",
                              password="sk1726ks",
                              host="localhost",
                              port="1726") as con:
            with con.cursor() as cursor:
                cursor.executemany(
                    'INSERT INTO dictionary (word, transcription, translate) VALUES (%s, %s, %s)',
                    words_list  # ← УБРАТЬ СКОБКИ! Просто words_list
                )
        print(f"Добавлено {len(words_list)} слов в словарь")

database = Database()