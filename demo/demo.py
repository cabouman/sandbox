import numpy as np
from cython_sandbox import cython_matrix_multiplication, cython_mat_mult
import time

"""
This is a simple demo of multiplication of two matrices using 
    1. Loops in python
    2. Numpy
    3. A cython wrapper of a C subroutine
    4. Native cython
    
The page http://nealhughes.net/cython1/ also has a nice description about how to get good performance with cython.    
"""


def py_mat_mult(A, B):
    """
    Matrix multiplication using loops in python
    Args:
        A: Left matrix
        B: Right matrix

    Returns:
        C = A * B
    """
    # Get dimensions and check for compatibility
    n_rows = A.shape[0]
    n_cols = B.shape[1]
    n_mults = A.shape[1]
    if n_mults != B.shape[0]:
        raise AttributeError("Input matrices do not have compatible shapes.")

    # Allocate space and then loop to do the multiplication
    C = np.empty((n_rows, n_cols))
    for i in range(n_rows):
        for j in range(n_cols):
            C[i,j] = 0
            for k in range(n_mults):
                C[i,j] += A[i,k] * B[k,j]

    return C


if __name__ == '__main__':
    # Generate random matrices A and B of compatible sizes
    A = np.random.randint(10, size=(1000, 500)).astype(np.float32)
    B = np.random.randint(10, size=(500, 10)).astype(np.float32)

    # List of methods to compare
    methods = [py_mat_mult, cython_mat_mult, cython_matrix_multiplication, np.dot]
    method_names = ["Py loops", "Cython", "C code", "numpy"]
    # Note that cython_matrix_multiplication requires 2D np.ndarrays of floats with C contiguous format

    times = np.zeros((len(methods),))
    error = np.zeros((len(methods),))

    # Get the reference solution
    C_ref = np.dot(A,B)

    width = 10
    prec = 2
    print("\nComparison of matrix multiplication with various methods")
    print(f"Method\t\t Time (ms)\t\tL2 diff with numpy")
    print("----------------------------------------------")

    # Loop through the methods, time each one, and find the error
    for ind, method in enumerate(methods):
        times[ind] = time.time()
        # Compute matrix multiplication
        C = method(A, B)
        times[ind] = 1000 * (time.time() - times[ind])
        error[ind] = np.sqrt(np.sum((C_ref - C) ** 2))
        print(f"{method_names[ind]:{width}}\t{times[ind]:{width}.{prec}}\t{error[ind]:{width}.{prec}}")
