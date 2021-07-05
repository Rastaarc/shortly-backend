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
    regex = re.compile(
        r"(\w+://)?"                # protocol                      (optional)
        r"(\w+\.)?"                 # host                          (optional)
        r"((\w+)\.(\w+))"           # domain
        # top-level domain              (optional, can have > 1)
        r"(\.\w+)*"
        r"([\w\-\._\~/]*)*(?<!\.)"  # path, params, anchors, etc.   (optional)
    )
    match = regex.match(link)

    print(match)
    return True if match else False
