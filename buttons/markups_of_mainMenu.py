from telebot import types

run_mainMenu_teacher = types.ReplyKeyboardMarkup(resize_keyboard=True)
run_mainMenu_teacher.add(types.KeyboardButton('Main Menu'))
remove_run_mainMenu_teacher = types.ReplyKeyboardRemove()

run_mainMenu_student = types.ReplyKeyboardMarkup(resize_keyboard=True)
run_mainMenu_student.add(types.KeyboardButton('Main Menu'))
remove_run_mainMenu_student = types.ReplyKeyboardRemove()

mainMenu_student = types.InlineKeyboardMarkup()
mainMenu_student.add(types.InlineKeyboardButton('Dictionary', callback_data='dictionary'))

dictionary = types.InlineKeyboardMarkup()
dictionary.add(types.InlineKeyboardButton('Find by spelling', callback_data='find by spelling'),
               types.InlineKeyboardButton('🔢 Find by translation 🔢', callback_data='find by translation'),
               types.InlineKeyboardButton('🎲 Get 20 random words 🎲', callback_data='get random words of dictionary'))
