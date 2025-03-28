import argparse


def read_file(path_to_file) -> str:
    try: 
        with open(path_to_file, "r", encoding="utf-8") as file:
            return file.read().strip().upper()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File was not found: {e}")
    except Exception as e:
        raise Exception(f"error when reading a file: {e}")


def write_file(path_to_file, text) -> None:
    try: 
        with open(path_to_file, "w", encoding="utf-8") as file:
            file.write(text)

    except Exception as e:
        raise Exception(f"error when writing a file: {e}")
    

def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='a program for encrypting messages using the Vigener method')
    parser.add_argument("path_to_text", type=str, help="the path to the encrypted text")
    parser.add_argument("path_to_key", type=str, help="the path to the encryption key")
    parser.add_argument("path_to_ciphertext", type=str, help="the path to the ciphertext storage location")
    arg = parser.parse_args()
    return arg


def char_shift(char, shift) -> str:
    """
    Сдвигает символ на заданное количество позиций в алфавите.

    Args:
        char (str): сдвигаемый символ.
        shift (int): интервал сдвига.

    Returns:
        str: символ .
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
    """
    k_index = 0
    k_lenght = len(key) 
    chipertext = ''
    for char in text:
        print(k_index)
        shift = ord(key[k_index]) - ord('А') 
        chipertext += char_shift(char, shift)
        k_index = (k_index + 1) % k_lenght   
    return chipertext


def decrypt(chipertext, key) -> str:
    k_index = 0
    k_lenght = len(key) 
    dechipertext = ''
    for char in chipertext:
        shift = ord(key[k_index]) - ord('А') 
        dechipertext += char_shift(char, -shift)
        k_index = (k_index + 1) % k_lenght   
    return dechipertext


def main():
    paths = arg_parser()
    text = read_file(paths.path_to_text)
    key = read_file(paths.path_to_key)
    print(key)
    chipertext = encript(text, key)
    write_file(paths.path_to_ciphertext, chipertext)
    print(decrypt(chipertext, key))


if __name__ == "__main__":
    main()