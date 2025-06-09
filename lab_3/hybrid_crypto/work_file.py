def read_file(path_to_file) -> bytes:
    """
    Читает бинарные данные из файла.

    Args:
        path_to_file (str): Путь к файлу, который нужно прочитать.

    Returns:
        str: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: Если произошла другая ошибка при чтении файла.
    """
    try: 
        with open(path_to_file, "rb") as data:
            return data.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File was not found: {e}")
    except Exception as e:
        raise Exception(f"error when reading a file: {e}")


def write_file(path_to_file, data) -> None:
    """
    Записывает бинарные данные в указанный файл.

    Args:
        path_to_file (str): Путь к файлу, в который нужно записать данные.
        data (bytes): Данные, который нужно записать в файл.

    Raises:
        Exception: Если произошла ошибка при записи в файл.
    """
    try: 
        with open(path_to_file, "wb") as file:
            file.write(data)
    except Exception as e:
        raise Exception(f"error when writing a file: {e}")