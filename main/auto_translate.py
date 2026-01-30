from googletrans import Translator
import polib

translator = Translator()
po_file = polib.pofile("locale/uz/LC_MESSAGES/django.po")

# Убираем fuzzy и задаём язык
po_file.metadata['Language'] = 'uz'
po_file.fuzzy = False
for entry in po_file:
    entry.flags = [flag for flag in entry.flags if flag != 'fuzzy']

# Переводим
for entry in po_file.untranslated_entries():
    translated = translator.translate(entry.msgid, src='en', dest='uz')
    entry.msgstr = translated.text
    print(f"✔ {entry.msgid} → {translated.text}")

po_file.save()
print("✅ Автоперевод завершён")
