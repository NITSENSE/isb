import os


IDEA_KEY_LENGTH_BYTES = 16 


def generate_idea_key() -> bytes:
    """
    Генерирует случайный 128-битный (16 байт) ключ для IDEA.
    Возвращает:
        bytes: Сгенерированный ключ.
    """
    key = os.urandom(IDEA_KEY_LENGTH_BYTES)
    print(f"The key for the IDEA algorithm has been generated ({IDEA_KEY_LENGTH_BYTES * 8} bit)")
    return key


if __name__ == '__main__':
    idea_key = generate_idea_key()
    print(f"Сгенерированный ключ IDEA: {idea_key.hex} (длина: {len(idea_key)} байт)")