#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "allocate.h"
#include "matrices.h"


void py_2_multialloc_2D(struct Amatrix_float *A)
{
    int i;

    /* Allocate and set array of pointers for multialloc array */
    A->mat = get_spc(sizeof(float *), A->NRows);
    for (i = 0; i < A->NRows ; i ++ ) {
        A->mat[i] = A->mat_pt + i*(A->NCols);
    }
}


void multialloc_2_py_2D(struct Amatrix_float *A)
{
    free((void **)A->mat);
}


int matrix_multiplication(struct Amatrix_float *A, struct Amatrix_float *B , struct Amatrix_float *C)
{
    int i, j, k;

    /* Convert 2D arrays from 1D python format to 2D multialloc format */
    py_2_multialloc_2D(A);
    py_2_multialloc_2D(B);
    py_2_multialloc_2D(C);

    /* Check that matrix shapes are correct */
    if (A->NCols != B->NRows) {
        printf("Number of columns in matrix A(%d) should equal to number of rows in matrix B(%d).\n", A->NCols, B->NRows);
        return(-1);
    }

    /* Compute matrix product */
    for (i = 0; i < A->NRows ; i ++ )
        for (j = 0; j < B->NCols ; j ++ ) {
            C->mat[i][j] = 0;
            for (k = 0; k < A->NCols ; k ++ )
                C->mat[i][j] += A->mat[i][k]*B->mat[k][j];
        }

    multialloc_2_py_2D(A);
    multialloc_2_py_2D(B);
    multialloc_2_py_2D(C);
    return(0);
}