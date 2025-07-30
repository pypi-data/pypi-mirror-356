#include "cfastmath.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
#include <stdbool.h>

bool will_multiply_overflow_uint64(uint64_t a, uint64_t b);

bool will_multiply_overflow_uint64(uint64_t a, uint64_t b) {
    if (b == 0) return false;  // multiplying by 0 is always safe
    return a > UINT64_MAX / b;
}

// Integer absolute value using bitwise ops (no branching)
int32_t abs_int(int32_t value) {
    int32_t mask = value >> 31;      // all 1s if negative, 0 if positive
    return (value + mask) ^ mask;    // flips bits +1 if negative
}

double divide(double a, double b) {
    if (fabs(b) < EPSILON) {  // check for near-zero to avoid division by zero
        fprintf(stderr, "Error: Division by zero.\n");
        exit(EXIT_FAILURE);
    }
    return a / b;
}

double power(double base, double exponent) {
    return pow(base, exponent);
}

double square_root(double value) {
    if (value < 0) {
        fprintf(stderr, "Error: Square root of negative number.\n");
        exit(EXIT_FAILURE);
    }
    return sqrt(value);
}

double absolute(double value) {
    return fabs(value);
}

double logarithm(double value) {
    if (value <= 0) {
        fprintf(stderr, "Error: Logarithm of non-positive number.\n");
        exit(EXIT_FAILURE);
    }
    return log(value);
}

double sine(double angle) {
    return sin(angle);
}

double cosine(double angle) {
    return cos(angle);
}

double tangent(double angle) {
    return tan(angle);
}

double arc_sine(double value) {
    if (value < -1 || value > 1) {
        fprintf(stderr, "Error: Arc sine of out of range value.\n");
        exit(EXIT_FAILURE);
    }
    return asin(value);
}

double arc_cosine(double value) {
    if (value < -1 || value > 1) {
        fprintf(stderr, "Error: Arc cosine of out of range value.\n");
        exit(EXIT_FAILURE);
    }
    return acos(value);
}

double arc_tangent(double value) {
    return atan(value);
}

double modulus(double a, double b) {
    if (fabs(b) < EPSILON) {
        fprintf(stderr, "Error: Modulus by zero.\n");
        exit(EXIT_FAILURE);
    }
    return fmod(a, b);
}

double exponential(double value) {
    return exp(value);
}

double hyperbolic_sine(double value) {
    return sinh(value);
}

double hyperbolic_cosine(double value) {
    return cosh(value);
}

double hyperbolic_tangent(double value) {
    return tanh(value);
}

double hyperbolic_arc_sine(double value) {
    return asinh(value);
}

double hyperbolic_arc_cosine(double value) {
    return acosh(value);
}

double hyperbolic_arc_tangent(double value) {
    return atanh(value);
}

uint64_t factorial(uint32_t n) {
    if (n == 0) return 1;
    uint64_t result = 1;
    for (uint32_t i = 2; i <= n; ++i) {
        if (will_multiply_overflow_uint64(result, i)) {
            fprintf(stderr, "Error: factorial overflow for n = %u.\n", n);
            exit(EXIT_FAILURE);
        }
        result *= i;
    }
    return result;
}

uint64_t combination(uint32_t n, uint32_t k) {
    if (k > n) {
        fprintf(stderr, "Error: Invalid combination parameters.\n");
        exit(EXIT_FAILURE);
    }
    if (k > n - k) k = n - k;

    uint64_t result = 1;
    for (uint32_t i = 1; i <= k; ++i) {
        uint64_t numerator = n - k + i;
        if (will_multiply_overflow_uint64(result, numerator)) {
            fprintf(stderr, "Error: combination overflow for n = %u, k = %u.\n", n, k);
            exit(EXIT_FAILURE);
        }
        result *= numerator;
        result /= i;
    }
    return result;
}

uint64_t permutation(uint32_t n, uint32_t k) {
    if (k > n) {
        fprintf(stderr, "Error: Invalid permutation parameters.\n");
        exit(EXIT_FAILURE);
    }
    uint64_t result = 1;
    for (uint32_t i = 0; i < k; ++i) {
        uint64_t factor = n - i;
        if (will_multiply_overflow_uint64(result, factor)) {
            fprintf(stderr, "Error: permutation overflow for n = %u, k = %u.\n", n, k);
            exit(EXIT_FAILURE);
        }
        result *= factor;
    }
    return result;
}

// Bitwise GCD using Stein's Algorithm (binary GCD)
static uint32_t gcd_unsigned(uint32_t a, uint32_t b) {
    if (a == 0) return b;
    if (b == 0) return a;

    // Find common factors of 2
    uint32_t shift = 0;
    while (((a | b) & 1) == 0) {
        a >>= 1;
        b >>= 1;
        shift++;
    }

    // Divide a by 2 until odd
    while ((a & 1) == 0) {
        a >>= 1;
    }

    do {
        // Remove all factors of 2 in b
        while ((b & 1) == 0) {
            b >>= 1;
        }

        // Now a and b are both odd. Swap if necessary so a <= b
        if (a > b) {
            uint32_t temp = a;
            a = b;
            b = temp;
        }

        b = b - a;  // b is now even
    } while (b != 0);

    // Restore common factors of 2
    return a << shift;
}

int32_t gcd(int32_t a, int32_t b) {
    // Use abs_int for negative input
    uint32_t ua = (uint32_t) abs_int(a);
    uint32_t ub = (uint32_t) abs_int(b);
    return (int32_t) gcd_unsigned(ua, ub);
}

int32_t lcm(int32_t a, int32_t b) {
    if (a == 0 || b == 0) return 0;
    // lcm(a,b) = |a * b| / gcd(a,b)
    int64_t product = (int64_t) a * b;
    int32_t gcd_val = gcd(a, b);
    return (int32_t)(llabs(product) / gcd_val);
}

double mean(const double *values, uint32_t count) {
    double total = 0.0;
    for (uint32_t i = 0; i < count; ++i) {
        total += values[i];
    }
    return total / count;
}

int compare_doubles(const void *a, const void *b) {
    double diff = (*(double *)a) - (*(double *)b);
    if (diff < 0) return -1;
    if (diff > 0) return 1;
    return 0;
}

void quicksort(double *array, uint32_t size) {
    qsort(array, size, sizeof(double), compare_doubles);
}

void sort(double *array, uint32_t size) {
    quicksort(array, size);
}

double median(double *values, uint32_t count) {
    sort(values, count);
    if (count % 2 == 1) {
        return values[count >> 1];  // bitwise divide by 2
    } else {
        return (values[(count >> 1) - 1] + values[count >> 1]) / 2.0;
    }
}

double population_variance(const double *values, uint32_t count) {
    double mean_val = mean(values, count);
    double total = 0.0;
    for (uint32_t i = 0; i < count; ++i) {
        double diff = values[i] - mean_val;
        total += diff * diff;
    }
    return total / count;
}

double sample_variance(const double *values, uint32_t count) {
    if (count < 2) {
        fprintf(stderr, "Sample variance requires at least two data points.\n");
        exit(EXIT_FAILURE);
    }
    double mean_val = mean(values, count);
    double total = 0.0;
    for (uint32_t i = 0; i < count; ++i) {
        double diff = values[i] - mean_val;
        total += diff * diff;
    }
    return total / (count - 1);
}

double population_standard_deviation(const double *values, uint32_t count) {
    return sqrt(population_variance(values, count));
}

double sample_standard_deviation(const double *values, uint32_t count) {
    return sqrt(sample_variance(values, count));
}

double population_covariance(const double *x, const double *y, uint32_t count) {
    double mean_x = mean(x, count);
    double mean_y = mean(y, count);
    double total = 0.0;
    for (uint32_t i = 0; i < count; ++i) {
        total += (x[i] - mean_x) * (y[i] - mean_y);
    }
    return total / count;
}

double sample_covariance(const double *x, const double *y, uint32_t count) {
    if (count < 2) {
        fprintf(stderr, "Sample covariance requires at least two data points.\n");
        exit(EXIT_FAILURE);
    }
    double mean_x = mean(x, count);
    double mean_y = mean(y, count);
    double total = 0.0;
    for (uint32_t i = 0; i < count; ++i) {
        total += (x[i] - mean_x) * (y[i] - mean_y);
    }
    return total / (count - 1);
}

double min(const double *arr, uint32_t size) {
    if (size == 0) {
        fprintf(stderr, "Error: min of empty array.\n");
        exit(EXIT_FAILURE);
    }
    double min_val = arr[0];
    for (uint32_t i = 1; i < size; ++i) {
        if (arr[i] < min_val) min_val = arr[i];
    }
    return min_val;
}

double max(const double *arr, uint32_t size) {
    if (size == 0) {
        fprintf(stderr, "Error: max of empty array.\n");
        exit(EXIT_FAILURE);
    }
    double max_val = arr[0];
    for (uint32_t i = 1; i < size; ++i) {
        if (arr[i] > max_val) max_val = arr[i];
    }
    return max_val;
}

double sum(const double *arr, uint32_t size) {
    double total = 0.0;
    for (uint32_t i = 0; i < size; ++i) {
        total += arr[i];
    }
    return total;
}

double z_score(double value, double mean, double stddev) {
    if (fabs(stddev) < EPSILON) {
        fprintf(stderr, "Standard deviation cannot be zero for z-score.\n");
        exit(EXIT_FAILURE);
    }
    return (value - mean) / stddev;
}

double normal_pdf(double x, double mu, double sigma) {
    if (sigma <= 0) {
        fprintf(stderr, "Standard deviation must be positive for normal PDF.\n");
        exit(EXIT_FAILURE);
    }
    double diff = x - mu;
    return (1.0 / (sigma * sqrt(2.0 * M_PI))) * exp(-(diff * diff) / (2.0 * sigma * sigma));
}

double normal_cdf(double x, double mu, double sigma) {
    if (sigma <= 0) {
        fprintf(stderr, "Standard deviation must be positive for normal CDF.\n");
        exit(EXIT_FAILURE);
    }
    return 0.5 * (1.0 + erf((x - mu) / (sigma * sqrt(2.0))));
}

void add_array(const double *a, const double *b, double *out, uint32_t n) {
    for (uint32_t i = 0; i < n; ++i) {
        out[i] = a[i] + b[i];
    }
}

void scalar_multiply(const double *a, double scalar, double *out, uint32_t n) {
    for (uint32_t i = 0; i < n; ++i) {
        out[i] = a[i] * scalar;
    }
}

double dot(const double *a, const double *b, uint32_t n) {
    double result = 0.0;
    for (uint32_t i = 0; i < n; ++i) {
        result += a[i] * b[i];
    }
    return result;
}
