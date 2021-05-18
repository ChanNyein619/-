from bs4 import BeautifulSoup
import requests
import re

def get_text():
    result = ""
    links_to_texts = [
        'http://az.lib.ru/t/tolstoj_a_k/text_0190.shtml',
        'http://az.lib.ru/r/rozanow_w_w/text_1911_lyudi_lunnogo_sveta.shtml',
        'http://az.lib.ru/a/arcybashew_m_p/text_0160.shtml'
    ]
    for url in links_to_texts:
        raw_text = requests.get(url).text  # Текс с html тегами
        soup = BeautifulSoup(raw_text, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        cleaned_text = soup.get_text()
        result += cleaned_text
    return result


def get_tokens_by_regexp(text):
    regex = re.compile("[А-Яа-я]+")
    dirt = regex.findall(text.lower())
    clean = list(set(dirt))
    return [word for word in clean if len(word) > 1]


def get_dict():
    return get_tokens_by_regexp(get_text())

