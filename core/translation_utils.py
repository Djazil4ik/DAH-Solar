import re
from googletrans import Translator
from bs4 import BeautifulSoup
import time

translator = Translator()


def safe_translate(text, src, dest, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return translator.translate(text, src=src, dest=dest).text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
                e = e
            else:
                # Возвращаем исходный текст при постоянной ошибке
                return text


def translate_html(html_content, src, dest, retries=3, delay=2):
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup.find_all(string=True):
        if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']: #type: ignore
            text = element.strip() # type: ignore
            if text:
                translated = safe_translate(
                    text, src=src, dest=dest, retries=retries, delay=delay)

                # Пробел после знаков препинания если слитно
                translated = re.sub(r'([.!?,;:])(?=[A-Za-zА-Яа-яЁёA-Za-z\u0400-\u04FF\u0100-\u024F])', r'\1 ', translated) # type: ignore
                translated = re.sub(r'\s+', ' ', translated).strip()

                element.replace_with(translated) # type: ignore

    return str(soup)
