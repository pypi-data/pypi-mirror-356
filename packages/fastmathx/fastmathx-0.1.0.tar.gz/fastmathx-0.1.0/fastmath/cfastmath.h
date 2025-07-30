#pragma once

#include <math.h>
#include <stdint.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#define EPSILON 1e-9
#endif

static inline double add(double a, double b) { return a + b; }
static inline double subtract(double a, double b) { return a - b; }
static inline double multiply(double a, double b) { return a * b; }
static inline double square(double x) { return x * x; }
static inline double cube(double x) { return x * x * x; }
static inline double absolute_value(double x) { return fabs(x); }

double divide(double a, double b);
double power(double base, double exponent);
double square_root(double value);
double absolute(double value);
double logarithm(double value);
double sine(double angle);
double cosine(double angle);
double tangent(double angle);
double arc_sine(double value);
double arc_cosine(double value);
double arc_tangent(double value);
double modulus(double a, double b);
double exponential(double value);
double hyperbolic_sine(double value);
double hyperbolic_cosine(double value);
double hyperbolic_tangent(double value);
double hyperbolic_arc_sine(double value);
double hyperbolic_arc_cosine(double value);
double hyperbolic_arc_tangent(double value);
uint64_t factorial(uint32_t n);
uint64_t combination(uint32_t n, uint32_t k);
uint64_t permutation(uint32_t n, uint32_t k);
int32_t gcd(int32_t a, int32_t b);
int32_t lcm(int32_t a, int32_t b);
int32_t abs_int(int32_t value);
double mean(const double *values, uint32_t count);
int compare_doubles(const void *a, const void *b);
void quicksort(double *array, uint32_t size);
void sort(double *array, uint32_t size);
double median(double *values, uint32_t count);
double population_variance(const double *values, uint32_t count);
double sample_variance(const double *values, uint32_t count);
double population_standard_deviation(const double *values, uint32_t count);
double sample_standard_deviation(const double *values, uint32_t count);
double population_covariance(const double *x, const double *y, uint32_t count);
double sample_covariance(const double *x, const double *y, uint32_t count);
double min(const double *arr, uint32_t size);
double max(const double *arr, uint32_t size);
double sum(const double *arr, uint32_t size);
double z_score(double value, double mean, double stddev);
double normal_pdf(double x, double mu, double sigma);
double normal_cdf(double x, double mu, double sigma);
void add_array(const double *a, const double *b, double *out, uint32_t n);
void scalar_multiply(const double *a, double scalar, double *out, uint32_t n);
double dot(const double *a, const double *b, uint32_t n);