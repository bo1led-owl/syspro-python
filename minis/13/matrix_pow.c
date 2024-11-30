#define PY_SSIZE_T_CLEAN
#include <Python.h>

static void matrix_swap(double** a, double** b) {
    double* tmp = *a;
    *a = *b;
    *b = tmp;
}

static void matrix_mul(size_t n, double* a, double* b, double* buf) {
    memset(buf, 0, n * n * sizeof(double));

    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            for (size_t k = 0; k < n; ++k) {
                buf[i * n + j] += a[i * n + k] * b[k * n + j];
            }
        }
    }
}

static PyObject* matrix_pow(PyObject* self, PyObject* args) {
    PyObject* py_mat;
    size_t power;
    if (!PyArg_ParseTuple(args, "OK", &py_mat, &power)) {
        return NULL;
    }

    size_t mat_len = PyObject_Length(py_mat);

    PyObject* py_res_mat = PyList_New(mat_len);
    if (power == 0) {
        for (size_t i = 0; i < mat_len; ++i) {
            PyObject* row = PyList_New(mat_len);
            PyList_SetItem(py_res_mat, i, row);
            for (size_t j = 0; j < mat_len; ++j) {
                PyList_SetItem(row, j, PyFloat_FromDouble(i == j));
            }
        }
        return py_res_mat;
    } else if (power == 1) {
        for (size_t i = 0; i < mat_len; ++i) {
            PyObject* original_row = PyList_GetItem(py_mat, i);
            PyObject* row = PyList_New(mat_len);
            PyList_SetItem(py_res_mat, i, row);
            for (size_t j = 0; j < mat_len; ++j) {
                double item = PyFloat_AsDouble(PyList_GetItem(original_row, j));
                PyList_SetItem(row, j, PyFloat_FromDouble(item));
            }
        }
        return py_res_mat;
    }

    size_t mat_size = sizeof(double) * mat_len * mat_len;

    double* original_matrix = malloc(mat_size);
    double* result = malloc(mat_size);
    double* matrix_buf = malloc(mat_size);

    for (size_t i = 0; i < mat_len; ++i) {
        PyObject* row = PyList_GetItem(py_mat, i);
        for (size_t j = 0; j < mat_len; ++j) {
            PyObject* item = PyList_GetItem(row, j);
            original_matrix[i * mat_len + j] = PyFloat_AsDouble(item);
        }
    }

    memcpy(result, original_matrix, mat_size);

    for (size_t i = 1; i < power; ++i) {
        matrix_mul(mat_len, result, original_matrix, matrix_buf);
        matrix_swap(&result, &matrix_buf);
    }

    for (size_t i = 0; i < mat_len; ++i) {
        PyObject* row = PyList_New(mat_len);
        PyList_SetItem(py_res_mat, i, row);
        for (size_t j = 0; j < mat_len; ++j) {
            double item = result[i * mat_len + j];
            PyList_SetItem(row, j, PyFloat_FromDouble(item));
        }
    }

    free(original_matrix);
    free(result);
    free(matrix_buf);

    return py_res_mat;
}

static PyMethodDef methods[] = {
    {
        .ml_name = "matrix_pow",
        .ml_meth = matrix_pow,
        .ml_flags = METH_VARARGS,
        .ml_doc = "",
    },
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "matrix_pow", NULL, -1, methods,
};

PyObject* PyInit_matrix_pow(void) { return PyModule_Create(&module); }
