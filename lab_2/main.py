from work_file import read_file, read_json
from stage_2.tests import RandomnessTests


def main():
    servis_paths = read_json("C:/Users/NITSENSE KO/Desktop/Учеба/isb/isb/lab_2/service_file.json")
    cpp_seq = RandomnessTests(read_file(servis_paths["path_to_cpp_sequence"]))
    java_seq = RandomnessTests(read_file(servis_paths["path_to_java_sequence"]))
    cpp_seq.print_len()
    cpp_seq.print_sequence()
    print(cpp_seq.frequency_test())
    print(cpp_seq.runs_test(),"\n")

    java_seq.print_len()
    java_seq.print_sequence()
    print(java_seq.frequency_test()) 
    print(java_seq.runs_test(),"\n") 

if __name__ == "__main__":
    main()