import time
import re
import os
from googletrans import Translator
import polib
import dotenv

dotenv.load_dotenv()  # Загружаем переменные окружения из .env файла

language = os.getenv("DEST_LANGUAGE", "ru")  # Получаем язык из переменной окружения или используем русский по умолчанию


def fix_punctuation_spacing(text):
    """Исправляет пробелы после знаков препинания"""
    text = re.sub(r'([.!?,;:])(?=[A-Za-zА-Яа-яЁё])', r'\1 ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def translate_po_file(po_path, src_lang='en', dest_lang=language, delay=0.5):
    """
    Автоматический перевод .po файла
    
    Args:
        po_path: путь к .po файлу
        src_lang: исходный язык
        dest_lang: целевой язык
        delay: задержка между запросами (чтобы не получить бан)
    """
    translator = Translator()
    po_file = polib.pofile(po_path)

    # Настройка метаданных
    po_file.metadata['Language'] = dest_lang
    po_file.fuzzy = False  # type: ignore

    # Удаляем fuzzy флаги
    for entry in po_file:
        entry.flags = [flag for flag in entry.flags if flag != 'fuzzy']

    untranslated = po_file.untranslated_entries()
    total = len(untranslated)

    print(f"🔄 Найдено {total} непереведённых строк")
    print(f"📝 Начинаю перевод с {src_lang} на {dest_lang}...\n")

    success_count = 0
    error_count = 0

    for idx, entry in enumerate(untranslated, 1):
        try:
            # Пропускаем пустые строки
            if not entry.msgid.strip():
                continue

            # Переводим
            translated = translator.translate(
                entry.msgid, src=src_lang, dest=dest_lang)

            # Исправляем пунктуацию
            entry.msgstr = fix_punctuation_spacing(translated.text) # type: ignore

            print(
                f"[{idx}/{total}] ✔ {entry.msgid[:50]}... → {entry.msgstr[:50]}...")
            success_count += 1

            # Задержка для избежания блокировки
            time.sleep(delay)

        except Exception as e:
            print(
                f"[{idx}/{total}] ✖ Ошибка при переводе '{entry.msgid[:50]}...': {e}")
            error_count += 1
            time.sleep(delay * 2)  # Увеличенная задержка после ошибки

    # Сохраняем
    po_file.save()

    print("\n✅ Перевод завершён!")
    print(f"   Успешно: {success_count}")
    print(f"   Ошибок: {error_count}")
    print(f"   Сохранено в: {po_path}")
    print("\n💡 Не забудьте выполнить: python manage.py compilemessages")


if __name__ == "__main__":
    translate_po_file(f"locale/{language}/LC_MESSAGES/django.po")
