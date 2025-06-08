from cryptography.hazmat.primitives.asymmetric import rsa


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


if __name__ == '__main__':
    priv_key, pub_key = generate_rsa_keys()
    print("\nПриватный ключ RSA (объект):")
    print(priv_key)
    print("\nПубличный ключ RSA (объект):")
    print(pub_key)