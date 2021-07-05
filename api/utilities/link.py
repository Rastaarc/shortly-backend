import string
import random
from .constants import (
    URL_PREFIX
)
import re


def create_short_link(keyword, prefix=URL_PREFIX):
    return prefix + re.sub(r"\W+", "", keyword)


def create_short_link_free(prefix=URL_PREFIX):
    letters = string.ascii_letters
    numbers = string.digits

    letters_ord = [4, 5, 6]
    digits_ord = [1, 2, 3]

    short = random.choices(letters, k=random.choice(letters_ord))
    short += random.choices(numbers, k=random.choice(digits_ord))
    random.shuffle(short)
    short.sort(reverse=True)
    k = short[:2]
    short = short[2:]
    random.shuffle(short)
    short = k + short
    short_link = "".join(short)

    return prefix + short_link


def valid_link(link):
    match = re.match(
        r'/^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?$/', link)

    return True if match else False
