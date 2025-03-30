from enum import Enum
from file_work import read_file, write_file, read_json, write_json
from task_1.text_encryptor import arg_parser_task_1, encript, decrypt
from task_2.frequency_analysis import arg_parser_task_2, freguency_analis, match_alphabets_by_frequency, decrypt_text


class Task(Enum):
    """
    Выбор задачи.

    Attributes:
        TASK_1 (int): Задание 1.
        TASK_2 (int): Задание 2.
    """
    TASK_1 = 1
    TASK_2 = 2


class Goal(Enum):
    """
    Выбор порядка выполнения второго задания.

    Attributes:
        FREQUENCY_ANALYSIS (int): Выполнить частотный анализ, 
            получить возможный вариант расшифровки текста.
        LOCATION_SELECTION (int): Проверка гипотиз,
            когда частотный анализ уже был произведен.
    """
    FREQUENCY_ANALYSIS = 1
    LOCATION_SELECTION = 2


def main():
    """
    Основная точка входа программы.
    
    """
    try:
        match Task.TASK_2.value:
            case 1: 
                paths = arg_parser_task_1()
                text = read_file(paths.path_to_text)
                key = read_json(paths.path_to_key)["key"]
                print(key)
                chipertext = encript(text, key)
                write_file(paths.path_to_ciphertext, chipertext)
            case 2:
                paths = arg_parser_task_2()
                servis_paths = read_json("service_file.json")
                chipertext = read_file(paths.path_to_ciphertext).upper()
                match Goal.LOCATION_SELECTION.value:
                    case 1:
                        char_freg = freguency_analis(chipertext)
                        rus_freg = read_json(servis_paths["path_to_rus_freg"])
                        write_json(servis_paths["path_to_char_freg"], char_freg)
                        key_encryptor = match_alphabets_by_frequency(rus_freg, char_freg)
                        write_json(servis_paths["path_to_freguency_mach"], key_encryptor)
                    case 2:
                        key_encryptor = read_json(servis_paths["path_to_freguency_mach"])
                deciphertext = decrypt_text(chipertext, key_encryptor)
                write_file(paths.path_to_text, deciphertext)
    except Exception as e:
        raise Exception(f"program error: {e}")


if __name__ == "__main__":
    main()