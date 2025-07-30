import pandas as pd
import numpy as np

def string_inner_product(input_string_list, input_string_coeff_list, pauli_matrix_list, pauli_coeff_list):
    #print("abcdefgihjk")
    output_string_list = []
    residue_list = []
    for input_string, input_string_coeff in zip(input_string_list, input_string_coeff_list):
        for pauli_matrix, pauli_coeff in zip(pauli_matrix_list, pauli_coeff_list):
            output_string = ''
            residue = pauli_coeff*input_string_coeff
            for i in zip(pauli_matrix[::-1], input_string):    
                if i == ('I', '0'):
                    output_string += '0'
                elif i == ('I', '1'):
                    output_string += '1'
                elif i == ('X', '0'):
                    output_string += '1'
                elif i == ('X', '1'):
                    output_string += '0'
                elif i == ('Y', '0'):
                    output_string += '1'
                    residue *= 1j
                elif i == ('Y', '1'):
                    output_string += '0'
                    residue *= -1j
                elif i == ('Z', '0'):
                    output_string += '0'
                elif i == ('Z', '1'):
                    output_string += '1'
                    residue *= -1

    output_string_list.append(output_string)
    residue_list.append(residue)

    df_psi = pd.DataFrame({'sample_s': input_string_list, 'prob_amp': input_string_coeff_list})
    df_psi_dagger = df_psi.copy()
    df_psi_dagger['prob_amp'] = df_psi_dagger['prob_amp'].apply(np.conjugate)
    df_psi_dagger['prob_amp'] = df_psi_dagger['prob_amp'].apply(np.complex128)
    dict_H_psi={}
    for index in range(len(output_string_list)):
        if output_string_list[index] not in dict_H_psi:
            dict_H_psi[output_string_list[index]]=residue_list[index]
        else:
            dict_H_psi[output_string_list[index]] += residue_list[index]
    df_H_psi = pd.DataFrame(dict_H_psi.items(), columns=['H_sample_s', 'prob_amp'])
    df_inner_product = df_psi_dagger.merge(df_H_psi, left_on=['sample_s'], right_on = ['H_sample_s'], how='inner', suffixes=('_left', '_right'))
    inner_product = (df_inner_product['prob_amp_left'] * df_inner_product['prob_amp_right']).sum().real
            
    return inner_product