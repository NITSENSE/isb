import argparse
from os import path
import json



def read_file(path_to_file) -> str:
    """
    Читает содержимое файла возвращает его в виде строки.

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
            return file.read().strip()
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


def read_json(path_to_json) -> dict:
    """
    Функция загружает данные из JSON-файла и возвращает их в виде словаря.
    
    Аргументы:
    path_to_json (str): путь к JSON-файлу, из которого нужно загрузить данные.
    
    Возвращаемое значение:
    dict: словарь, полученный из JSON-файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: Если произошла другая ошибка при чтении файла.
    """
    try: 
        with open(path_to_json, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"JSON File was not found: {e}")
    except Exception as e:
        raise Exception(f"error when reading a JSON file: {e}")


def write_json(path_to_json, dictionary) -> None:
    """
    Функция сохраняет словарь в формате JSON в указанном файле.
    
    Аргументы:
    path_to_json (str): путь к файлу, в который нужно сохранить JSON.
    dictionary (dict): словарь, который нужно сохранить.
    """
    try:
        with open(path_to_json, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)
    except Exception as e:
        raise Exception(f"error when writing a JSON file: {e}")
        

def arg_parser() -> argparse.Namespace:
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


def main():
    """
    Главная функция программы, которая запускает процесс дешифрования текста.
    """
    try:
        paths = arg_parser()
        servis_paths = read_json("service_file.json")
        chipertext = read_file(paths.path_to_ciphertext).upper()
        #char_freg = freguency_analis(chipertext)
        #rus_freg = read_json(servis_paths["path_to_rus_freg"])
        #write_json(servis_paths["path_to_char_freg"], char_freg)
        #key_encryptor = match_alphabets_by_frequency(rus_freg, char_freg)
        #write_json(servis_paths["path_to_freguency_mach"], key_encryptor)
        key_encryptor = read_json(servis_paths["path_to_freguency_mach"])
        deciphertext = decrypt_text(chipertext, key_encryptor)
        write_file(paths.path_to_text, deciphertext)
    except Exception as e:
        raise Exception(f"program error: {e}") 



if __name__ == "__main__":
    main()