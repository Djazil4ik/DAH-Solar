import re
from googletrans import Translator
from bs4 import BeautifulSoup
import time

translator = Translator()


def safe_translate(text, src, dest, retries=3, delay=2):
    for attempt in range(retries):
        try:
            translator = Translator()
            return translator.translate(text, src=src, dest=dest).text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return text


def translate_html(html_content, src, dest, retries=3, delay=2):
    soup = BeautifulSoup(html_content, 'html.parser')

    elements = [
        el for el in soup.find_all(string=True)
        if el.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]'] #type: ignore
        and el.text.strip()
    ]

    if not elements:
        return str(soup)

    texts = [el.text.strip() for el in elements]

    translated_texts = safe_translate_bulk(
        texts, src=src, dest=dest, retries=retries, delay=delay)

    for element, translated in zip(elements, translated_texts): #type: ignore
        translated = re.sub(
            r'([.!?,;:])(?=[A-Za-zА-Яа-яЁёA-Za-z\u0400-\u04FF\u0100-\u024F])', r'\1 ', translated)
        translated = re.sub(r'\s+', ' ', translated).strip()
        element.replace_with(translated)

    return str(soup)


def safe_translate_bulk(texts, src, dest, retries=3, delay=2):
    for attempt in range(retries):
        try:
            translator = Translator()
            results = translator.translate(texts, src=src, dest=dest)
            return [r.text for r in results] #type: ignore
        except Exception:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return texts
