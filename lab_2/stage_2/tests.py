import math


class RandomnessTests:
    def __init__(self, bit_sequence: str):
        if not all(bit in '01' for bit in bit_sequence):
            raise TypeError("The sequence is not binary")
        if len(bit_sequence) == 0:
            raise ValueError("Binary sequense should not be empty")
        self.bit_sequence = bit_sequence
        self.seq_len = len(bit_sequence)
        
    
    def print_sequence(self) -> None:
        formatted_sequence = ''
        for i in range(0, len(self.bit_sequence), 8):
            formatted_sequence += self.bit_sequence[i:i+8]
            formatted_sequence += ' '
            if (i + 8) % 64 == 0:
                formatted_sequence += '\n'
        print(formatted_sequence.strip())


    def print_len(self) -> None:
        print(self.seq_len)

    
    def frequency_test(self) -> float:
        dif = self.bit_sequence.count("1") - self.bit_sequence.count("0")
        s_n = abs(dif) / math.sqrt(self.seq_len)
        p_value = math.erfc(s_n / math.sqrt(2))
        return p_value
    

    def runs_test(self) -> float:
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





    
    
