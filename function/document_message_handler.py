from bots import main
import openpyxl
from bots.main import *
import zipfile
import os
from db import db
database = db.Database()

def document(message):
    if main.status_create_test_in_excel == True:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)
        original_filename = message.document.file_name or "document"
        zip_path = os.path.join(temp_dir, f"{original_filename}.zip")
        xlsx_path = os.path.join(temp_dir, original_filename)
        try:
            with open(zip_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            if not zipfile.is_zipfile(zip_path):
                bot.reply_to(message, "Ошибка: файл не является корректным ZIP‑архивом.")
                return
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            if original_filename.lower().endswith('.xlsx'):
                os.rename(zip_path, xlsx_path)
            else:
                xlsx_path_with_ext = xlsx_path if xlsx_path.lower().endswith('.xlsx') else f"{xlsx_path}.xlsx"
                os.rename(zip_path, xlsx_path_with_ext)
                xlsx_path = xlsx_path_with_ext
            workbook = openpyxl.load_workbook(xlsx_path)
            sheet = workbook.active
            test_name = sheet[2][2].value
            theme = sheet[2][3].value
            test_id = database.insert_tests(test_name, theme, main.group_id)
            for i in range(2, sheet.max_row + 1):
                question = sheet[i][0].value
                answer = sheet[i][1].value
                if question or answer != None:
                    database.insert_question_and_answer_into_testquestions(question, test_id, answer)
            bot.send_message(message.chat.id, 'Создание теста завершено!', reply_markup=nav2.back_to_teacher_menu)
        except Exception as e:
            bot.reply_to(message, e)
        finally:
            import shutil

            if os.path.exists(str(temp_dir)):
                shutil.rmtree(str(temp_dir))