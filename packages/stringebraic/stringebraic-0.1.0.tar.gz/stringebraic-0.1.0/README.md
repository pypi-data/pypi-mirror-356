  <figure>
    <img src="https://github.com/kwyip/stringebraic/blob/main/logo.png?raw=True" alt="logo" height="143" />
  </figure>

[![](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/kwyip/stringebraic/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stringebraic)](https://pypi.org/project/stringebraic/)
[![Static Badge](https://img.shields.io/badge/CalVer-2025.0416-ff5733)](https://pypi.org/project/stringebraic)
[![Static Badge](https://img.shields.io/badge/PyPI-wheels-d8d805)](https://pypi.org/project/stringebraic/#files)
[![](https://pepy.tech/badge/stringebraic/month)](https://pepy.tech/project/stringebraic)

[stringebraic](https://stringebraic.github.io/)
===============================================

Stringebraic is a library of methods for representing a Hamiltonian (i.e., a matrix) as a sum of Pauli *string*s and a quantum state (i.e., a vector) as a sum of *bitstring*s. This perspective allows for a variety of operations using these *string*s, such as matrix-vector multiplication, inner products, and other algebraic manipulations.  
🐦: Why take this approach?  
🐧: Because the computational complexity of these operations typically grows exponentially with the number of qubits—or, equivalently, with the size of the matrix.

In layman&#39;s terms, it automates Pauli algebra by:

1.  removing the concept of matrix and vector size,
2.  performing the matrix multiplication with string-based rules.

#### Input Files:

*   `input_string_list.pkl` – A [pickle](https://docs.python.org/3/library/pickle.html)
        file containing a list of bitstrings that compose the quantum state.</li>
*   `input_string_coeff_list.pkl` – A pickle file containing a list of coefficients that compose the quantum state.
*   `pauli_matrix_list.pkl` – A pickle file containing a list of Pauli strings that compose the Hamiltonian.
*   `pauli_coeff_list.pkl` – A pickle file containing a list of Pauli coefficients that compose the Hamiltonian. 

#### Output:

*   `The inner product value` – A scalar for what the inner product (e.g., expected energy) is.

* * *

Installation
------------

It can be installed with `pip`, ideally by using a [virtual environment](https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment). Open up a terminal and install the package and the dependencies with:  
  

    `pip install stringebraic`

_or_

    `python -m pip install stringebraic`

  
_🐍 This requires Python 3.8 or newer versions_

* * *

### Steps to fast compute the inner product energy using Pauli *string* algebra

1.  **Prepare the input files (i.e., converting the quantum Hamiltonian and quantum state into lists of strings and coefficients, as specified in the above [section](#input-files))**.
2.  **Run the command to generate a inner product (i.e., a scalar)**:  
      
    
           `stringebraic input_string_list.pkl input_string_coeff_list.pkl pauli_matrix_list.pkl pauli_coeff_list.pkl`


* * *

### Test

You may test the installation using the sample input files (`input_string_list.pkl` and
    `input_string_coeff_list.pkl`, `pauli_matrix_list.pkl` and `pauli_coeff_list.pkl`) located in the test folder.

---

♥ Lastly executed on Python `3.10` on 2025-06-05.