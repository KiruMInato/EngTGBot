import psycopg2
from db import db
from bots import config
from bots import main
from function import groups
from buttons import markups_of_registration as nav
from buttons import markups_of_mainMenu as nav2
from telebot import types
from  function import registration
from function import mainMenu
from  bots import main
database= db.Database()
bot=config.bot
status_create_test_in_tg=False
create_test_in_excel=False

def callback(call):
    global role
    global grade
    if call.data == "registration":
        main.status_of_registration=True
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
        record=database.get_grade_letter_of_group(call.from_user.username)
        choose_grade_and_letter_btn = types.InlineKeyboardMarkup()
        main.status_create_test_in_tg=True
        for i in record:
            choose_grade_and_letter_btn.add(types.InlineKeyboardButton(f'Класс: {i[1]} Буква: {i[2]}', callback_data=str(i[0])))
        bot.send_message(call.message.chat.id, 'Выберите группу:', reply_markup=choose_grade_and_letter_btn)
    elif call.data == 'create_test_in_excel':
        main.status_create_test_in_excel=True
        record=database.get_grade_letter_of_group(call.from_user.username)
        choose_grade_and_letter_btn = types.InlineKeyboardMarkup()
        for i in record:
            choose_grade_and_letter_btn.add(
                types.InlineKeyboardButton(f'Класс: {i[1]} Буква: {i[2]}', callback_data=str(i[0])))
        bot.send_message(call.message.chat.id, 'Выберите группу:', reply_markup=choose_grade_and_letter_btn)



    elif call.data == 'get_test':
        main.status_get_test = True
        record = database.get_teacher_id_from_student(tg=call.from_user.username)
        choose_tests_btn=types.InlineKeyboardMarkup()
        for i in record:
            choose_tests_btn.add(types.InlineKeyboardButton(f'{i[1]}', callback_data=str(i[1])))
            bot.send_message(call.message.chat.id, 'Доступные тесты:', reply_markup=choose_tests_btn)
    elif call.data=='positive_answer_to_start_test':
         main.status_get_test=False
         main.status_of_taking_the_test=True
         record = database.select_question_and_answer(main.test_id)
         bot.send_message(call.message.chat.id, f'{record[0][0]}?')



    elif call.data=='see_all_groups':
        record = database.get_grade_and_letter_from_teacher(tg=call.from_user.username)
        print(record)

    elif call.data == 'get_report_of_test':
        main.status_ger_report=True
        record = database.get_grade_letter_of_group(call.from_user.username)
        choose_grade_and_letter_btn = types.InlineKeyboardMarkup()
        for i in record:
            choose_grade_and_letter_btn.add(
                types.InlineKeyboardButton(f'Класс: {i[1]} Буква: {i[2]}', callback_data=str(i[0])))
        bot.send_message(call.message.chat.id, 'Выберите группу:', reply_markup=choose_grade_and_letter_btn)


    elif call.data=='go_back_to_menu_student':
        mainMenu.send_mainMenu_to_student(call.message)
    elif call.data=='go_back_to_menu_teacher':
        mainMenu.send_mainMenu_to_teacher(call.message)



    else:
        if main.status_of_registration==True:
            number_of_teachers = database.get_all_teachers_from_users()
            for i in number_of_teachers:
                if call.data==str(i[0]):
                    name=i[0]
                    tg = call.from_user.username
                    role=registration.user.role
                    name_student=registration.user.name
                    group_id=database.select_teacherid_to_student_into_groups(name, groups.group.grade, groups.group.letter, tg, name_student, role, message=call.message)
                    if group_id:
                        bot.send_message(call.message.chat.id, 'Регистрация прошла успешно!', reply_markup=nav2.run_mainMenu_student)
                        main.status_of_registration = False



        if main.status_create_test_in_excel==True or main.status_create_test_in_tg==True or main.status_ger_report==True:
            record = database.get_grade_letter_of_group(call.from_user.username)
            for i in record:
                if call.data==str(i[0]) and main.status_create_test_in_tg==True:
                    bot.send_message(call.message.chat.id, f'Вот ваш шаблон!\n'
                                                           'Следуйте по нему и ваши вопросы будут занесены в базу данных!\n\n'
                                                           'Test Name:\n'
                                                           'Test Theme:\n'
                                                           'Question:\n'
                                                           'Answer:\n'
                                                           '(И так дальше сколько вам нужно вопросов)')
                    main.group_id=i[0]
                elif call.data==str(i[0]) and main.status_create_test_in_excel==True:
                    bot.send_document(call.message.chat.id, open('../Other/testexample.xlsx', 'rb'), caption='Вот ваш шаблон.\n'
                                                                                                     'Под ячейкой А1 пишите Question (писать можно до бесконечности)\n'
                                                                                                     'Под ячейкой B1 пишите Answer (писать можно до бесконечности)\n'
                                                                                                     'В ячейках C2 и D2 напишите название теста и его тему!\n'
                                                                                                     'ВАЖНО: писать вопрос и справа ответ на этот вопрос!')
                    main.group_id = i[0]
                elif call.data==str(i[0]) and main.status_ger_report==True:
                    main.group_id = i[0]
                    test=database.select_test_from_group_id(main.group_id)
                    choose_tests_btn = types.InlineKeyboardMarkup()
                    if test:
                        for i in test:
                            choose_tests_btn.add(types.InlineKeyboardButton(f'{i[1]}', callback_data=str(i[1])))
                        bot.send_message(call.message.chat.id, 'Активные тесты:', reply_markup=choose_tests_btn)
                    else:
                        bot.send_message(call.message.chat.id, 'Нет активных тестов для данной группы.')




        if main.status_get_test==True:
            record = database.get_teacher_id_from_student(tg=call.from_user.username)
            for i in record:
                if call.data==str(i[1]):
                    main.test_id=i[0]
                    answer_to_start_test_btn=types.InlineKeyboardMarkup()
                    answer_to_start_test_btn.add(types.InlineKeyboardButton('Да', callback_data='positive_answer_to_start_test'))
                    bot.send_message(call.message.chat.id, 'Начать прохождение теста?\n'
                                                   'P.S.: После начала теста все сообщения в чате будут удалены!', reply_markup=answer_to_start_test_btn)

        if main.status_ger_report==True:
            test = database.select_test_from_group_id(main.group_id)
            for i in test:
                if call.data==str(i[1]):
                    main.test_id=i[0]
                    report=database.select_student_id_date_time_pass_from_reports(main.test_id) # [(88, date_time(19 59 19...), '1'),(.....)]
                    if report:
                        st_id=[]
                        passes=[]
                        date=[]
                        q=set()
                        for i in report:
                            student_id=i[0]
                            pas=i[2]
                            date_time = str(i[1])
                            question_id=i[3]
                            date.append(date_time)
                            st_id.append(student_id)
                            passes.append(pas)
                            q.add(question_id)
                        for n in range(0, len(st_id)+1):
                            if n<len(st_id)-1:
                                if st_id[n]==st_id[n+1]:
                                    st_id.pop(n)
                                    passes[n+1]=int(passes[n+1])+int(passes[n])
                                    passes.pop(n)
                                    date.pop(n)
                                    name = database.select_name_from_users(st_id[n])
                                    name=name[0]
                                    bot.send_message(call.message.chat.id, f'{name} | {date[n]} | {passes[n]} из {len(q)}')
                    else:
                        bot.send_message(call.message.chat.id, 'Тест никем не пройден.')