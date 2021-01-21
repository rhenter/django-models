import re
import unicodedata


def digits_only(raw_number):
    return re.sub(r"[^0-9]", "", raw_number)


def is_equal(words):
    return all(c == words[i - 1] for i, c in enumerate(words) if i > 0)


def remove_special_characters(text):
    cleaned_text = re.sub(r'([^\s\w]|_)+', '', text.strip())
    return remove_accents(cleaned_text)


def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
