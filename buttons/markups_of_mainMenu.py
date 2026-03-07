from telebot import types

run_mainMenu_teacher = types.ReplyKeyboardMarkup(resize_keyboard=True)
run_mainMenu_teacher.add(types.KeyboardButton('Главное меню👀'))
remove_run_mainMenu_teacher = types.ReplyKeyboardRemove()

run_mainMenu_student = types.ReplyKeyboardMarkup(resize_keyboard=True)
run_mainMenu_student.add(types.KeyboardButton('Главное меню👀'))
remove_run_mainMenu_student = types.ReplyKeyboardRemove()

mainMenu_student = types.InlineKeyboardMarkup()
mainMenu_student.add(types.InlineKeyboardButton('Словарь 📒', callback_data='dictionary'),
                     types.InlineKeyboardButton('Получить задание 💬', callback_data='get_test'))

dictionary = types.InlineKeyboardMarkup()
dictionary.add(types.InlineKeyboardButton(' Найти слово 🔢', callback_data='find word'),
               types.InlineKeyboardButton(' Получить 20 случайных слов 🎲', callback_data='get random words of dictionary'))

dictionary_find_word = types.InlineKeyboardMarkup()
dictionary_find_word.add(types.InlineKeyboardButton(' Попробовать снова 🔢', callback_data='find word'))

mainMenu_teacher = types.InlineKeyboardMarkup()
mainMenu_teacher.add(types.InlineKeyboardButton('--Создать тест--', callback_data='create_test_for_student'),
                     types.InlineKeyboardButton('--Посмотреть группы--', callback_data='see_all_groups'))

create_test_type = types.InlineKeyboardMarkup()
create_test_type.add(types.InlineKeyboardButton('--Создать в Telegramm--', callback_data='create_test_in_tg'),
                     types.InlineKeyboardButton('--Создать в Excel--', callback_data='create_test_in_excel'))

