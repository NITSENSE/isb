import argparse
from os import path


def arg_parser_task_1() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.

    Returns:
        argparse.Namespace: Объект с аргументами командной строки.

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    parser = argparse.ArgumentParser(description='The program for encrypting messages using the Vigener method')
    parser.add_argument("path_to_text", type=str, help="the path to the encrypted text")
    parser.add_argument("path_to_key", type=str, help="the path to the encryption key (.json)")
    parser.add_argument("path_to_ciphertext", type=str, help="the path to the ciphertext storage location")
    args = parser.parse_args()
    if not path.exists(args.path_to_text):
        raise FileNotFoundError(f"The text file was not found: {args.path_to_text}")
    if not path.exists(args.path_to_key):
        raise FileNotFoundError(f"The encryption key was not found: {args.path_to_key}")
    return args


def char_shift(char, shift) -> str:
    """
    Выполняет сдвиг символа на указанное количество позиций в алфавите.

    Args:
        char (str): Символ, который нужно сдвинуть.
        shift (int): Величина сдвига.

    Returns:
        str: Новый символ после сдвига.
    """
    if 'А' <= char <= 'Я':
        start = ord('А')
        return chr(start + (ord(char) - start + shift) % 32)
    return char


def encript(text, key) -> str:
    """
    Шифрует текст с помощью шифра Виженера.

    Args:
        text (str): Текст для шифрования.
        key (str): Ключ для шифрования.

    Returns:
        chipertext (str): Зашифрованный текст.

    Raises:
        Exception: Если произошла ошибка при шифровании.
    """
    k_index = 0
    k_lenght = len(key) 
    chipertext = ''
    try: 
        for char in text:
            shift = ord(key[k_index]) - ord('А') 
            chipertext += char_shift(char, shift)
            k_index = (k_index + 1) % k_lenght  
    except Exception as e:
        raise Exception(f"encripting error: {e}")
    return chipertext


def decrypt(chipertext, key) -> str:
    """
    Дешифрует текст методом Виженера.

    Args:
        ciphertext (str): Зашифрованный текст.
        key (str): Ключ шифрования.

    Returns:
        str: Расшифрованный текст.

    Raises:
        Exception: Если произошла ошибка при дешифровке.
    """ 
    k_index = 0
    k_lenght = len(key) 
    dechipertext = ''
    try: 
        for char in chipertext:
            shift = ord(key[k_index]) - ord('А') 
            dechipertext += char_shift(char, -shift)
            k_index = (k_index + 1) % k_lenght   
    except Exception as e:
        raise Exception(f"decripting error: {e}")
    return dechipertext