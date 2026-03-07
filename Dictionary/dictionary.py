from db import db
from bots import config
from buttons import markups_of_mainMenu as nav2
bot = config.bot
database = db.Database()


class Word_finding:
    word=None

    def set_word(self, word):
        self.word=word

fd=Word_finding()

def find_word_by_translate(message):
    if message.text and not message.text.startswith('/'):
        find_word_by_translate_2(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите слово:")
        bot.register_next_step_handler(message, find_word_by_translate)

def find_word_by_translate_2(message):
    global word
    word = message.text.strip()
    fd.set_word(word)
    result = None
    result = database.find_word_by_translate(fd.word)
    if result:
        response = "✨ <b>Словарь</b> ✨\n\n"
        for word, translate, transcription in result:
            response += f"<b>{word}</b>\n"
            if transcription:
                trans = transcription
                for char in ['[', ']', '\\']:
                    trans = trans.replace(char, '')
                response += f"<code>/{trans}/</code>\n"
            translations = [t.strip() for t in translate.split(',')]
            response += "<i>Перевод:</i>\n"
            for trans in translations:
                response += f"• {trans}\n"
            response += "\n"
        bot.send_message(message.chat.id, response, parse_mode="HTML", reply_markup=nav2.dictionary_find_word)
    else:
        bot.send_message(message.chat.id,
            "😔 <b>Увы, слово не найдено</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Наш словарь пока не знает этого слова.\n\n"
            "<b>Что можно сделать:</b>\n"
            "• Проверить правильность написания\n"
            "• Попробовать синонимы\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💫 Попробуйте ещё раз!",
            parse_mode="HTML", reply_markup=nav2.dictionary_find_word)