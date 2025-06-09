from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from work_file import write_file, read_file
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import hashes
from idea_operations import generate_idea_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


RSA_PUBLIC_EXPONENT = 65537
RSA_KEY_SIZE_BITS = 2048


def generate_rsa_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Генерирует пару ключей RSA (приватный и публичный).
    Размер ключа: 2048 бит, публичная экспонента: 65537.
    Возвращает:
        tuple[RSAPrivateKey, RSAPublicKey]: Кортеж с приватным и публичным ключами.
    """
    private_key = rsa.generate_private_key(
        public_exponent = RSA_PUBLIC_EXPONENT,
        key_size = RSA_KEY_SIZE_BITS
    )
    public_key = private_key.public_key()
    print("The pair of keys for the RSA has been generated (2048 bit).")
    return private_key, public_key


def serialize_rsa_keys(public_key: rsa.RSAPublicKey, private_key: rsa.RSAPrivateKey,
                       public_key_path: str, private_key_path: str) -> None:
    """
    Сериализует публичный и приватный ключи RSA и сохраняет их в файлы.
    Параметры:
        public_key (RSAPublicKey): Объект публичного ключа RSA.
        private_key (RSAPrivateKey): Объект приватного ключа RSA.
        public_key_path (str): Путь для сохранения публичного ключа.
        private_key_path (str): Путь для сохранения приватного ключа.
    """
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    write_file(public_key_path, public_pem)
    print(f"The RSA public key is stored in: {public_key_path}")

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    write_file(private_key_path, private_pem)
    print(f"The RSA private key is stored in: {private_key_path}")


def encrypt_symmetric_key_rsa(symmetric_key: bytes, public_key: rsa.RSAPublicKey,
                              encrypted_symmetric_key_path: str) -> None:
    """
    Шифрует симметричный ключ с помощью публичного ключа RSA (OAEP) и сохраняет в файл.
    Параметры:
        symmetric_key (bytes): Симметричный ключ (ключ IDEA).
        public_key (RSAPublicKey): Публичный ключ RSA.
        encrypted_symmetric_key_path (str): Путь для сохранения зашифрованного симметричного ключа.
    """
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    write_file(encrypted_symmetric_key_path, encrypted_symmetric_key)
    print(f"The symmetric key is encrypted with RSA and stored in: {encrypted_symmetric_key_path}")


def load_rsa_private_key(private_key_path: str) -> rsa.RSAPrivateKey | None:
    """
    Загружает приватный ключ RSA из PEM-файла.
    Параметры:
        private_key_path (str): Путь к файлу с приватным ключом.
    Возвращает:
        RSAPrivateKey | None: Объект приватного ключа или None в случае ошибки.
    """
    private_key_pem = read_file(private_key_path)
    if private_key_pem is None:
        raise FileNotFoundError(f"The private key file was not found on the way: {private_key_path}")
    try:
        private_key = load_pem_private_key(
            private_key_pem,
            password=None
        )
        print(f"The RSA private key has been successfully uploaded from: {private_key_path}")
        return private_key
    except ValueError as e:
        raise ValueError(f"Error loading the RSA private key: {e}. The format may be incorrect.")
    except Exception as e: 
        raise Exception(f"Unexpected error when uploading an RSA private key: {e}")


def load_rsa_public_key(public_key_path: str) -> rsa.RSAPublicKey:
    """
    Загружает публичный ключ RSA из PEM-файла.

    Параметры:
        public_key_path (str): Путь к файлу с публичным ключом.

    Возвращает:
        RSAPublicKey: Объект публичного ключа RSA.

    Исключения (Raises):
        FileNotFoundError: Если файл по указанному пути не найден.
        ValueError: Если данные в файле имеют неверный формат.
    """
    public_key_pem = read_file(public_key_path)
    if public_key_pem is None:
        raise FileNotFoundError(f"The public key file was not found on the way: {public_key_path}")
    try:
        private_key = load_pem_public_key(
            public_key_pem
        )
        print(f"The RSA public key has been successfully uploaded from: {public_key_path}")
        return private_key
    except ValueError as e:
        raise ValueError(f"Error loading the RSA public key: {e}. The format may be incorrect.")
    except Exception as e: 
        raise Exception(f"Unexpected error when uploading an RSA public key: {e}")


def decrypt_symmetric_key_rsa(encrypted_symmetric_key_path: str, 
                              private_key: rsa.RSAPrivateKey) -> bytes | None:
    """
    Дешифрует симметричный ключ, зашифрованный RSA, с помощью приватного ключа RSA.
    Параметры:
        encrypted_symmetric_key_path (str): Путь к файлу с зашифрованным симметричным ключом.
        private_key (RSAPrivateKey): Объект приватного ключа RSA.
    Возвращает:
        bytes | None: Расшифрованный симметричный ключ или None в случае ошибки.
    """
    encrypted_symmetric_key = read_file(encrypted_symmetric_key_path)
    if encrypted_symmetric_key is None:
        raise FileNotFoundError(f"""The key file was not found on the way: {
            encrypted_symmetric_key_path
        }""")
    
    try:
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("The symmetric key has been successfully decrypted using RSA")
        return symmetric_key
    except Exception as e:
        raise Exception(f"Symmetric key decryption error: {e}")
    

if __name__ == '__main__':

    PUBLIC_KEY_PATH = "lab_3/keys/public.pem"
    PRIVATE_KEY_PATH = "lab_3/keys/private.pem"
    ENCRYPTED_KEY_PATH = "lab_3/keys/encrypted_sym_key.bin"


    print("--- ШАГ 1: Генерация и сохранение ключей RSA ---")
    priv_key_obj, pub_key_obj = generate_rsa_keys()
    serialize_rsa_keys(pub_key_obj, priv_key_obj, PUBLIC_KEY_PATH, PRIVATE_KEY_PATH)
    print("\n--- ШАГ 2: Генерация и шифрование симметричного ключа ---")
    original_idea_key = generate_idea_key()
    print(f"Оригинальный ключ IDEA:    {original_idea_key.hex()}")
    encrypt_symmetric_key_rsa(original_idea_key, pub_key_obj, ENCRYPTED_KEY_PATH)
    print("\n--- ШАГ 3: Загрузка приватного ключа и расшифровка ---")
    try:
        loaded_private_key = load_rsa_private_key(PRIVATE_KEY_PATH)
        if loaded_private_key:
            decrypted_idea_key = decrypt_symmetric_key_rsa(
                ENCRYPTED_KEY_PATH, 
                loaded_private_key
            )
            print(f"Расшифрованный ключ IDEA: {decrypted_idea_key.hex()}")         
            assert original_idea_key == decrypted_idea_key
            print("\n[УСПЕХ] Ключи совпадают! Полный цикл шифрования-расшифровки прошел корректно.")
    except (FileNotFoundError, ValueError, Exception) as e:
        print(f"\n[ОШИБКА] Произошла ошибка во время выполнения: {e}")

    
