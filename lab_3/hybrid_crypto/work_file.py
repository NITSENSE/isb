def read_file(file_path: str, is_binary: bool = True) -> bytes | str | None:
    """
    Читает содержимое файла.
    Параметры:
        file_path (str): Путь к файлу.
        is_binary (bool): Если True (по умолчанию), читает в бинарном режиме ('rb').
                          Если False, читает в текстовом режиме ('r') с кодировкой UTF-8.
    Возвращает:
        bytes | str | None: Содержимое файла или None в случае ошибки.
    """
    mode = 'rb' if is_binary else 'r'
    encoding = None if is_binary else 'utf-8'
    try:
        with open(file_path, mode, encoding=encoding) as f:
            content = f.read()
        return content
    except FileNotFoundError:
        # Лучше использовать raise, чтобы вызывающий код мог обработать ошибку
        raise FileNotFoundError(f"Файл не найден по пути: {file_path}")
    except Exception as e:
        # Обработка других возможных ошибок, например, с кодировкой
        raise IOError(f"Не удалось прочитать файл '{file_path}': {e}")


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