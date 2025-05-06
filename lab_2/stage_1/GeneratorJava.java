package lab_2.stage_1;

import java.math.BigInteger;
import java.security.SecureRandom;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Класс GeneratorJava предназначен для генерации случайной 128-битной двоичной последовательности
 * и записи её в файл.
 */
public class GeneratorJava {
    /**
     * Основной метод программы. Запускает процесс генерации двоичной последовательности
     * и записи её в файл.
     *
     * @param args аргументы командной строки (не используются)
     */
    public static void main(String[] args) {
        writingSequenceToFile(generateSequence());
    }

    /**
     * Генерирует случайную 128-битную двоичную последовательность.
     * Использует SecureRandom для создания случайного числа и преобразует его в двоичную строку,
     * дополняя нули слева до 128 бит.
     *
     * @return строка, представляющая 128-битную двоичную последовательность
     */
    public static String generateSequence(){
        BigInteger number = new BigInteger(128, new SecureRandom());
        String binaryString = String.format("%128s", number.toString(2)).replace(' ', '0');
        System.out.println(binaryString);
        return binaryString;
    }

    /**
     * Записывает переданную двоичную последовательность в файл "java_sequence.txt".
     * В случае ошибки записи выводит сообщение об ошибке.
     *
     * @param sequence строка с двоичной последовательностью для записи в файл
     */
    public static void writingSequenceToFile(String sequence){
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("java_sequence.txt"))) {
            writer.write(sequence);
            System.out.println("The sequence is written to a file.");
        } catch (IOException e) {
            System.err.println("wtite error: " + e.getMessage());
        }
    }
}