import argparse
from os import path


def read_file(path_to_file) -> str:
    """
    Читает содержимое файла и возвращает его в верхнем регистре.

    Args:
        path_to_file (str): Путь к файлу, который нужно прочитать.

    Returns:
        str: Содержимое файла в верхнем регистре.

    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: Если произошла другая ошибка при чтении файла.
    """
    try: 
        with open(path_to_file, "r", encoding="utf-8") as file:
            return file.read().strip().upper()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File was not found: {e}")
    except Exception as e:
        raise Exception(f"error when reading a file: {e}")


def write_file(path_to_file, text) -> None:
    """
    Записывает текст в указанный файл.

    Args:
        path_to_file (str): Путь к файлу, в который нужно записать текст.
        text (str): Текст, который нужно записать в файл.

    Raises:
        Exception: Если произошла ошибка при записи в файл.
    """
    try: 
        with open(path_to_file, "w", encoding="utf-8") as file:
            file.write(text)
    except Exception as e:
        raise Exception(f"error when writing a file: {e}")
    

def arg_parser() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.

    Returns:
        argparse.Namespace: Объект с аргументами командной строки.

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    parser = argparse.ArgumentParser(description='The program for encrypting messages using the Vigener method')
    parser.add_argument("path_to_text", type=str, help="the path to the encrypted text")
    parser.add_argument("path_to_key", type=str, help="the path to the encryption key")
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


def main():
    """
    Основная точка входа программы.

    Читает аргументы командной строки, шифрует текст и сохраняет результат.
    """
    paths = arg_parser()
    text = read_file(paths.path_to_text)
    key = read_file(paths.path_to_key)
    print(key)
    chipertext = encript(text, key)
    write_file(paths.path_to_ciphertext, chipertext)


if __name__ == "__main__":
    main()