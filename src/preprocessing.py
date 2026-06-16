import re

def convert_to_lowercase(text):
    return text.lower()

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def remove_extra_spaces(text):
    return ' '.join(text.split())

def clean_text(text):
    text = convert_to_lowercase(text)
    text = remove_special_characters(text)
    text = remove_extra_spaces(text)
    return text
