from work_file import read_file, read_json
from stage_2.tests import RandomnessTests


def main():
    """
    Основная точка входа программы.

    """
    try:
        servis_paths = read_json("lab_2/service_file.json")
        cpp_seq = RandomnessTests(read_file(servis_paths["path_to_cpp_sequence"]))
        java_seq = RandomnessTests(read_file(servis_paths["path_to_java_sequence"]))
        
        print("  CPP sequence: ")
        cpp_seq.print_sequence()
        print("\n  Java sequence: ")
        java_seq.print_sequence()
        print("\n Test Results for C++ Sequence \n")
        print(f"Frequency (Monobit) Test: {cpp_seq.frequency_test():.4f}")
        print(f"Runs Test: {cpp_seq.runs_test():.4f}")
        print(f"Longest Run of Ones Test: {cpp_seq.longest_sequence_test():.4f}\n")

        print("\n Test Results for Java Sequence \n")
        print(f"Frequency (Monobit) Test: {java_seq.frequency_test():.4f}")
        print(f"Runs Test: {java_seq.runs_test():.4f}")
        print(f"Longest Run of Ones Test: {java_seq.longest_sequence_test():.4f}\n")
    except Exception as e:
        raise Exception(f"decripting error: {e}")


if __name__ == "__main__":
    main()