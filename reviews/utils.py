import string
import random
from better_profanity import profanity
from pathlib import Path


def generate_slug():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


BASE_DIR = Path(__file__).resolve().parent.parent
bad_words_file = BASE_DIR / 'russian_badwords.txt'

# Загружаем слова из нашего файла
profanity.load_censor_words_from_file(str(bad_words_file))


def censor_profanity(text: str) -> str:
    return profanity.censor(text)
