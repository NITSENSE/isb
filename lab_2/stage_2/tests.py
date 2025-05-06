import math


class RandomnessTests:
    def __init__(self, bit_sequence: str):
        if not all(bit in '01' for bit in bit_sequence):
            raise TypeError("The sequence is not binary")
        self.bit_sequence = bit_sequence
        self.seq_len = len(bit_sequence)
        
    
    def print_sequence(self):
        formatted_sequence = ''
        for i in range(0, len(self.bit_sequence), 8):
            formatted_sequence += self.bit_sequence[i:i+8]
            formatted_sequence += ' '
            if (i + 8) % 64 == 0:
                formatted_sequence += '\n'
        print(formatted_sequence.strip())


    def print_len(self):
        print(self.seq_len)

    
    def frequency_bitwise_test(self):
        difference = self.bit_sequence.count("1") - self.bit_sequence.count("0")
        s_n = abs(difference) / math.sqrt(self.seq_len)
        p_value = math.erfc(s_n / math.sqrt(2))
        return p_value
    








    
    
