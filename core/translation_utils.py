import re
import time
import logging

from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)


def safe_translate(text, src, dest, retries=3, delay=2):
    last_exc = None
    for attempt in range(retries):
        try:
            translator = GoogleTranslator(source=src, target=dest)
            return translator.translate(text)
        except Exception as e:
            last_exc = e
            logger.warning(
                "translate attempt %s/%s failed (%s -> %s): %r",
                attempt + 1, retries, src, dest, e
            )
            if attempt < retries - 1:
                time.sleep(delay)

    logger.error(
        "translate failed after %s retries (%s -> %s): %r",
        retries, src, dest, last_exc
    )
    return text


def safe_translate_bulk(texts, src, dest, retries=3, delay=2):
    last_exc = None
    for attempt in range(retries):
        try:
            translator = GoogleTranslator(source=src, target=dest)
            results = translator.translate_batch(texts)
            return results
        except Exception as e:
            last_exc = e
            logger.warning(
                "translate attempt %s/%s failed (%s -> %s): %r",
                attempt + 1, retries, src, dest, e
            )
            if attempt < retries - 1:
                time.sleep(delay)

    logger.error(
        "translate failed after %s retries (%s -> %s): %r",
        retries, src, dest, last_exc
    )
    return texts


def translate_html(html_content, src, dest, retries=3, delay=2):
    soup = BeautifulSoup(html_content, 'html.parser')

    elements = [
        el for el in soup.find_all(string=True)
        # type: ignore
        if el.parent.name not in ['style', 'script', 'head', 'title', 'meta'] #type: ignore 
        and el.text.strip()
    ]

    if not elements:
        return str(soup)

    texts = [el.text.strip() for el in elements]

    translated_texts = safe_translate_bulk(
        texts, src=src, dest=dest, retries=retries, delay=delay)

    for element, translated in zip(elements, translated_texts):  # type: ignore
        translated = re.sub(
            r'([.!?,;:])(?=[A-Za-zА-Яа-яЁёA-Za-z\u0400-\u04FF\u0100-\u024F])', r'\1 ', translated)
        translated = re.sub(r'\s+', ' ', translated).strip()
        element.replace_with(translated) # type: ignore

    return str(soup)
