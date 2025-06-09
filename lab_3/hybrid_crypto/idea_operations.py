import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as symmetric_padding


IDEA_KEY_LENGTH_BYTES = 16 
IDEA_BLOCK_SIZE_BITS = 64
IDEA_BLOCK_SIZE_BYTES = IDEA_BLOCK_SIZE_BITS // 8


def generate_idea_key() -> bytes:
    """
    Генерирует случайный 128-битный (16 байт) ключ для IDEA.
    Возвращает:
        bytes: Сгенерированный ключ.
    """
    key = os.urandom(IDEA_KEY_LENGTH_BYTES)
    print(f"The key for the IDEA algorithm has been generated ({IDEA_KEY_LENGTH_BYTES * 8} bit)")
    return key


def add_padding(data: bytes) -> bytes:
    """
    Добавляет padding ANSIX923 к данным для блока 64 бита.
    """
    padder = symmetric_padding.ANSIX923(IDEA_BLOCK_SIZE_BITS).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def remove_padding(padded_data: bytes) -> bytes:
    """
    Удаляет padding ANSIX923 из данных для блока 64 бита.
    """
    unpadder = symmetric_padding.ANSIX923(IDEA_BLOCK_SIZE_BITS).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data
    

def encrypt_idea_cbc(plaintext: bytes, key: bytes) -> tuple[bytes, bytes] | None:
    """
    Шифрует данные с помощью IDEA в режиме CBC.
    Применяет padding ANSIX923.
    Параметры:
        plaintext (bytes): Открытый текст для шифрования.
        key (bytes): 128-битный ключ IDEA.
    Возвращает:
        tuple[bytes, bytes] | None: Кортеж (iv, ciphertext) или None в случае ошибки.
    """
    if len(key) * 8 != 128:
        print("Error: The IDEA key must be 128 bits (16 bytes) long.")
        return None

    try:
        padded_plaintext = add_padding(plaintext)
        iv = os.urandom(IDEA_BLOCK_SIZE_BYTES)
        cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        print("The data has been successfully encrypted by IDEA (CBC).")
        return iv, ciphertext
    except Exception as e:
        print(f"IDEA encryption error: {e}")
        return None
    
      
def decrypt_idea_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes | None:
    """
    Дешифрует данные с помощью IDEA в режиме CBC.
    Удаляет padding ANSIX923.
    Параметры:
        ciphertext (bytes): Шифротекст для дешифрования.
        key (bytes): 128-битный ключ IDEA.
        iv (bytes): 8-байтный вектор инициализации (IV).
    Возвращает:
        bytes | None: Расшифрованный открытый текст или None в случае ошибки.
    """
    if len(key) * 8 != 128:
        print("Error: The IDEA key must be 128 bits (16 bytes) long.")
        return None

    try:
        # 1. Создание шифра и дешифрование
        cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # 2. Удаление padding
        plaintext = remove_padding(padded_plaintext)
        
        print("The data has been successfully decrypted by IDEA (CBC).")
        return plaintext
    except Exception as e:
        print(f"IDEA decryption error: {e}")
        return None

    
if __name__ == '__main__':
    # --- Конфигурация ---
    SOURCE_TEXT_PATH = 'lab_3/source/text.txt'
    ENCRYPTED_FILE_PATH = 'lab_3/source/encrypted_idea.bin' 
    DECRYPTED_TEXT_PATH = 'lab_3/source/decrypted_text.txt'

    print("===== ТЕСТИРОВАНИЕ ШИФРОВАНИЯ IDEA (CBC) =====")

    # --- ШАГ 1: Генерация ключа IDEA ---
    print("\n--- ШАГ 1: Генерация ключа IDEA ---")
    idea_key = generate_idea_key()

    # --- ШАГ 2: Чтение исходного текста из файла ---
    print(f"\n--- ШАГ 2: Чтение исходного текста из файла ---")
    try:
        with open(SOURCE_TEXT_PATH, 'rb') as f:
            original_plaintext = f.read()
        print(f"Файл '{SOURCE_TEXT_PATH}' успешно прочитан. Размер: {len(original_plaintext)} байт.")
        print(f"Начало текста: {original_plaintext[:80]}...")
    except FileNotFoundError:
        print(f"ОШИБКА: Исходный файл не найден по пути: {SOURCE_TEXT_PATH}")
        print("Пожалуйста, создайте этот файл и поместите в него текст для шифрования.")
        exit(1) 
    # --- ШАГ 3: Шифрование данных ---
    print("\n--- ШАГ 3: Шифрование данных ---")
    encryption_result = encrypt_idea_cbc(original_plaintext, idea_key)
    if encryption_result:
        iv, ciphertext = encryption_result
        print(f"Размер IV (вектора инициализации): {len(iv)} байт")
        print(f"Размер шифротекста: {len(ciphertext)} байт")
        with open(ENCRYPTED_FILE_PATH, 'wb') as f:
            f.write(iv + ciphertext)
        print(f"Зашифрованный файл (IV + шифротекст) сохранен в '{ENCRYPTED_FILE_PATH}'")
    else:
        print("ОШИБКА: Шифрование не удалось. Прерывание работы.")
        exit(1)

    # --- ШАГ 4: Дешифрование данных ---
    print("\n--- ШАГ 4: Дешифрование данных ---")
    decrypted_plaintext = decrypt_idea_cbc(ciphertext, idea_key, iv)

    if decrypted_plaintext is None:
        print("ОШИБКА: Дешифрование не удалось. Прерывание работы.")
        exit(1)
    
    # Сохраняем расшифрованный текст для ручной проверки
    with open(DECRYPTED_TEXT_PATH, 'wb') as f:
        f.write(decrypted_plaintext)
    print(f"Расшифрованный текст сохранен в '{DECRYPTED_TEXT_PATH}' для ручной проверки.")

    # --- ШАГ 5: Проверка результата ---
    print("\n--- ШАГ 5: Проверка результата ---")
    if original_plaintext == decrypted_plaintext:
        print("✅ УСПЕХ! Исходный и расшифрованный тексты полностью совпадают.")
    else:
        print("❌ ПРОВАЛ! Исходный и расшифрованный тексты НЕ СОВПАДАЮТ.")
        print(f"Длина оригинала: {len(original_plaintext)}, Длина результата: {len(decrypted_plaintext)}")
    
    print("\n===== Тестирование завершено. =====")