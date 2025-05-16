import math
from spicy import special


class RandomnessTests:
    """
    Класс для проведения тестов на случайность битовой последовательности.
    """
    def __init__(self, bit_sequence: str):
        """
        Инициализирует объект тестов на случайность.

        Args:
            bit_sequence (str): Входная битовая последовательность (строка из '0' и '1').

        Raises:
            TypeError: Если последовательность содержит символы, отличные от '0' и '1'.
            ValueError: Если последовательность пуста.
        """
        if not all(bit in '01' for bit in bit_sequence):
            raise TypeError("The sequence is not binary")
        if len(bit_sequence) == 0:
            raise ValueError("Binary sequense should not be empty")
        self.bit_sequence = bit_sequence
        self.seq_len = len(bit_sequence)
        
    
    def _cut_into_blocks(self) -> list[str]:
        """
        Вспомогательный метод для разделения битовой последовательности на блоки по 8 бит.
        Если длина исходной последовательности не кратна 8, последний блок будет содержать 
        оставшиеся биты и будет короче 8 бит.

        Returns:
            list[str]: Список строк, где каждая строка - это блок (обычно из 8 бит).
        """
        blocks = [
            self.bit_sequence[i : i + 8] 
            for i in range(0, len(self.bit_sequence), 8)
        ]
        return blocks

    
    def print_sequence(self) -> None:
        """
        Выводит битовую последовательность, отформатированную блоками.
        Последовательность выводится группами по 8 блоков (каждый блок по 8 бит) в строке.
        """
        block_list = self._cut_into_blocks()
        for i in range(0, len(block_list), 8):
            current_group = block_list[i : i + 8]
            print(' '.join(current_group))


    def print_len(self) -> None:
        """
        Выводит длину битовой последовательности.
        """
        print(self.seq_len)

    
    def frequency_test(self) -> float:
        """
        Частотный тест (Monobit Frequency Test).
        Проверяет соотношение нулей и единиц во всей последовательности.
        Чем ближе количество единиц к количеству нулей, тем выше p-значение.

        Returns:
            float: p-значение теста. Если p-значение < 0.01, последовательность считается неслучайной.
        """
        dif = self.bit_sequence.count("1") - self.bit_sequence.count("0")
        s_n = abs(dif) / math.sqrt(self.seq_len)
        p_value = math.erfc(s_n / math.sqrt(2))
        return p_value
    

    def runs_test(self) -> float:
        """
        Тест на количество серий (Runs Test).
        Проверяет количество непрерывных серий одинаковых битов (например, '111' или '00').
        Слишком мало или слишком много серий указывает на неслучайность.

        Returns:
            float: p-значение теста. Если p-значение < 0.01, последовательность считается неслучайной.
                   Возвращает 0, если предварительное условие на долю единиц не выполняется.
        """
        size = self.seq_len
        z = self.bit_sequence.count("1") / size
        if abs(z - 0.5) >= 2 / math.sqrt(size):
            return 0 
        v_n = sum(
            self.bit_sequence[i] != self.bit_sequence[i + 1]
            for i in range(size - 1)
        )
        return math.erfc(
            abs(v_n - 2 * size * z * (1 - z)) / 
            (2 * math.sqrt(2 * size) * z * (1 - z))
        )
    

    def longest_sequence_test(self) -> float:
        """
        Тест на самую длинную серию единиц в блоке (Longest Run of Ones in a Block Test).
        Этот тест применяется к последовательности длиной 128 бит, которая делится
        на M=16 блоков по N=8 бит каждый. В каждом блоке определяется длина
        самой длинной непрерывной последовательности ('серии') единиц.

        Наблюдаемые частоты (νᵢ) длин таких серий сравниваются с теоретически
        ожидаемыми частотами (Mπᵢ) с использованием статистики хи-квадрат.

        Категории для длины самой длинной серии единиц в 8-битном блоке (K=4 категории):
        - Категория 0 (длина <= 1): π₀ = 0.2148, соответствует ν₀
        - Категория 1 (длина == 2): π₁ = 0.3672, соответствует ν₁
        - Категория 2 (длина == 3): π₂ = 0.2305, соответствует ν₂
        - Категория 3 (длина >= 4): π₃ = 0.1875, соответствует ν₃
        
        Статистика теста: χ² = Σᵢ ( (νᵢ - Mπᵢ)² / (Mπᵢ) ) для i от 0 до K-1.
        Число степеней свободы df = K-1 = 3.

        P-значение рассчитывается как P-value = gammainc(df/2, χ²/2), где `gammainc` — это 
        неполная гамма-функция

        Returns:
            float: p-значение теста. Если p-значение < 0.01, последовательность считается неслучайной.

        Raises:
            ValueError: Если длина входной последовательности не равна 128 битам.
        """
        if self.seq_len != 128:
            raise ValueError("This test runing for sequence with size 128 bits long")
        block_list = self._cut_into_blocks()
        v_i = [0] * 4
        theo_probs = [0.2148, 0.3672, 0.2305, 0.1875]
        for block in block_list:
            max_length = float(0)
            current_length = 0
            for bit in block:
                if bit == "1":
                    current_length += 1
                    max_length = max(max_length, current_length)
                else:
                    current_length = 0

            match max_length:
                case _ if max_length <= 1:
                    v_i[0] += 1
                case 2:
                    v_i[1] += 1
                case 3:
                    v_i[2] += 1
                case _:
                    v_i[3] += 1

        chi_square = sum(
            ((v_i[i] - 16 * theo_probs[i]) ** 2) / 
            (16 * theo_probs[i]) for i in range(len(v_i))
        )
        p_value = special.gammainc((3 / 2), (chi_square / 2))
        return p_value





    
    
