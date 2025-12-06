import db
from bots import config
bot = config.bot
database = db.Database()


class Word_finding:
    word=None
    translate=None


    def set_word(self, word):
        self.word=word

    def set_translate(self, translate):
        self.translate=translate


fd=Word_finding()

def find_word_by_translate(message):
    if message.text and not message.text.startswith('/'):
        find_word_by_translate_2(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите слово:")
        bot.register_next_step_handler(message, find_word_by_translate)

def find_word_by_translate_2(message):
    global word
    translate = message.text.strip()
    fd.set_translate(translate)
    result = None
    result = database.find_word_by_translate(message, fd.translate)
    bot.send_message(message.chat.id, result)
