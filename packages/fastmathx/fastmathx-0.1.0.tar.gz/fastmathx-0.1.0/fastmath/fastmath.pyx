# fastmath/fastmath.pyx
from libc.stdlib cimport malloc, free
from libc.stdint cimport uint32_t, uint64_t, int32_t

cdef extern from "cfastmath.h":
    double divide(double a, double b)
    uint64_t factorial(uint32_t n)
    uint64_t combination(uint32_t n, uint32_t k)
    uint64_t permutation(uint32_t n, uint32_t k)
    int32_t gcd(int32_t a, int32_t b)
    int32_t lcm(int32_t a, int32_t b)
    int32_t abs_int(int32_t value)
    double mean(const double *values, uint32_t count)
    double median(double *values, uint32_t count)
    double population_variance(const double *values, uint32_t count)
    double sample_variance(const double *values, uint32_t count)
    double population_standard_deviation(const double *values, uint32_t count)
    double sample_standard_deviation(const double *values, uint32_t count)
    double min(const double *arr, uint32_t size)
    double max(const double *arr, uint32_t size)
    double sum(const double *arr, uint32_t size)
    double z_score(double value, double mean, double stddev)
    double normal_pdf(double x, double mu, double sigma)
    double normal_cdf(double x, double mu, double sigma)
    void add_array(const double *a, const double *b, double *out, uint32_t n)
    void scalar_multiply(const double *a, double scalar, double *out, uint32_t n)
    double dot(const double *a, const double *b, uint32_t n)


def py_divide(double a, double b): return divide(a, b)
def py_factorial(unsigned int n): return factorial(n)
def py_combination(unsigned int n, unsigned int k): return combination(n, k)
def py_permutation(unsigned int n, unsigned int k): return permutation(n, k)
def py_gcd(int a, int b): return gcd(a, b)
def py_lcm(int a, int b): return lcm(a, b)
def py_abs_int(int val): return abs_int(val)
def py_z_score(double val, double mu, double sigma): return z_score(val, mu, sigma)
def py_normal_pdf(double x, double mu, double sigma): return normal_pdf(x, mu, sigma)
def py_normal_cdf(double x, double mu, double sigma): return normal_cdf(x, mu, sigma)

def py_mean(list arr):
    cdef int n = len(arr)
    cdef double* c_arr = <double*> malloc(n * sizeof(double))
    for i in range(n):
        c_arr[i] = arr[i]
    result = mean(c_arr, n)
    free(c_arr)
    return result

def py_median(list arr):
    cdef int n = len(arr)
    cdef double* c_arr = <double*> malloc(n * sizeof(double))
    for i in range(n):
        c_arr[i] = arr[i]
    result = median(c_arr, n)
    free(c_arr)
    return result

def py_sample_variance(list arr):
    cdef int n = len(arr)
    cdef double* c_arr = <double*> malloc(n * sizeof(double))
    for i in range(n):
        c_arr[i] = arr[i]
    result = sample_variance(c_arr, n)
    free(c_arr)
    return result

def py_dot(list a, list b):
    cdef int n = len(a)
    assert len(b) == n
    cdef double* c_a = <double*> malloc(n * sizeof(double))
    cdef double* c_b = <double*> malloc(n * sizeof(double))
    for i in range(n):
        c_a[i] = a[i]
        c_b[i] = b[i]
    result = dot(c_a, c_b, n)
    free(c_a)
    free(c_b)
    return result
