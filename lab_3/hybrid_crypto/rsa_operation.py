from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from work_file import write_file


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


if __name__ == '__main__':
    priv_key_obj, pub_key_obj = generate_rsa_keys()
    serialize_rsa_keys(pub_key_obj, priv_key_obj, 'lab_3/keys/public.pem', 'lab_3/keys/private.pem')
    print("Ключи RSA сгенерированы и сериализованы")