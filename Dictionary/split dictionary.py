import re

# путь к исходному файлу со словами
file_path = "slova6k.txt"

# сюда будет собираться итоговый список
words_list = []

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("//"):  # пропускаем пустые строки и комментарии
            continue

        # ищем шаблон: слово[транскрипция] перевод
        match = re.match(r"^([a-zA-Z\-]+)\[([^\]]+)\]\s*([^/]+)", line)
        if match:
            word = match.group(1).strip()
            transcription = f"[{match.group(2).strip()}]"
            translation = match.group(3).strip()

            # 🧹 очищаем перевод от мусорных символов
            translation = re.sub(r"[%~#*|^/]", "", translation)   # убираем лишние спецсимволы
            translation = translation.replace("-", " ").replace(";", ",").replace("~", "")
            translation = re.sub(r"\s+", " ", translation)        # убираем лишние пробелы
            translation = translation.strip(" ,.")                # чистим края

            # добавляем в список
            words_list.append((word, translation, transcription))

# сортируем по слову
words_list.sort(key=lambda x: x[0].lower())

# сохраняем весь список в файл Python
with open("words_list_full.py", "w", encoding="utf-8") as out:
    out.write("words_list = [\n")
    for word, translation, transcription in words_list:
        out.write(f'    ("{word}", "{translation}", "{transcription}"),\n')
    out.write("]\n")

print(f"✅ Готово! Найдено {len(words_list)} слов. Список сохранён в words_list_full.py")
