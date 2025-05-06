import json


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


