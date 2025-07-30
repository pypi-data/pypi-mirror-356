import sys
import pickle
from stringebraic import helpers

def main():
    if len(sys.argv[1:]) != 4:
        raise Exception("Sorry, please input four files: input_string_list, input_string_coeff_list, pauli_matrix_list, pauli_coeff_list.")
    input_string_list_file = sys.argv[1:][0]
    input_string_coeff_list_file = sys.argv[1:][1]
    pauli_matrix_list_file = sys.argv[1:][2]
    pauli_coeff_list_file = sys.argv[1:][3]


    print(input_string_list_file)
    print(input_string_coeff_list_file)
    print(pauli_matrix_list_file)
    print(pauli_coeff_list_file)


    with open(input_string_list_file, 'rb') as f:
        input_string_list = pickle.load(f)

    with open(input_string_coeff_list_file, 'rb') as f:
        input_string_coeff_list = pickle.load(f)

    with open(pauli_matrix_list_file, 'rb') as f:
        pauli_matrix_list = pickle.load(f)

    with open(pauli_coeff_list_file, 'rb') as f:
        pauli_coeff_list = pickle.load(f)

    print(input_string_list)
    print(input_string_coeff_list)
    print(pauli_matrix_list)
    print(pauli_coeff_list)


    inner_product = helpers.string_inner_product(input_string_list, input_string_coeff_list, pauli_matrix_list, pauli_coeff_list)
    print(inner_product)


if __name__ == '__main__':
    main()



