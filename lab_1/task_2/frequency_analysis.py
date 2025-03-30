import argparse
from os import path  


def arg_parser_task_2() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.

    Returns:
        argparse.Namespace: Объект с аргументами командной строки.

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    parser = argparse.ArgumentParser(description='The program for decrypting messages by frequency analysis')
    parser.add_argument("path_to_ciphertext", type=str, help="the path to the encrypted text")
    parser.add_argument("path_to_text", type=str, help="the path to the ciphertext storage location")
    args = parser.parse_args()
    if not path.exists(args.path_to_ciphertext):
        raise FileNotFoundError(f"The text file was not found: {args.path_to_ciphertext}")
    return args


def freguency_analis(text) -> dict:
    """
    Функция проводит частотный анализ текста, подсчитывая частоту появления каждого символа.
    
    Аргументы:
    text (str): текст, для которого проводится частотный анализ.
    
    Возвращаемое значение:
    dict: словарь, где ключи - символы текста, значения - частота их появления.
    """
    char_freg = {}
    lenght_text = len(text)
    for char in text:
        if char in char_freg:
            char_freg[char] += 1
        else:
            char_freg[char] = 1
    for key in char_freg:
        char_freg[key] /= lenght_text
    char_freg = dict(sorted(char_freg.items(), key=lambda item: item[1], reverse=True))
    return char_freg


def match_alphabets_by_frequency(alpha_rus, alpha_cipher) -> dict:
    """
    Функция сопоставляет алфавиты русского языка и шифра по частоте встречаемости символов.
    
    Аргументы:
    alpha_rus (dict): словарь частот символов русского языка.
    alpha_cipher (dict): словарь частот символов шифра.
    
    Возвращаемое значение:
    dict: таблица соответствий между символами шифра и русского алфавита.
    """
    match_char = dict(zip(alpha_cipher.keys(), alpha_rus.keys()))
    return match_char


def decrypt_text(text, key_dict) -> str:
    """
    Функция расшифровывает текст, используя предоставленную таблицу соответствий символов.
    
    Аргументы:
    text (str): зашифрованный текст.
    key_dict (dict): словарь соответствия между шифром и исходными символами.
    
    Возвращаемое значение:
    str: расшифрованный текст.
    """
    for key, value in key_dict.items():
        text = text.replace(key.upper(), value.lower())
    return text.upper()