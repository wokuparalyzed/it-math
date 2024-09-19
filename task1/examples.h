#define EXAMPLES_H

#include <math.h>

typedef double (*fun_xy)(double, double);

typedef struct u_func_t
{
    fun_xy u;
    fun_xy f;
} u_func_t;

double u_1(double x, double y) { return 3000 * pow(x, 3) + 2000 * pow(y, 3); }
double f_1(double x, double y) { return 2000 * x + 10000 * y; }

double u_2(double x, double y) { return 2 * pow(x, 4.0) + pow(x, 3.0) + pow(y, 2.0) + 6; }
double f_2(double x, double y) { return 24 * pow(x, 2.0) + 6 * x + 2; }

double u_3(double x, double y) { return 7 * pow(x, 2.0) - 10 * pow(x, 3.0) + x + y - 1; }
double f_3(double x, double y) { return 14 - 60 * x; }

double u_4(double x, double y) { return exp(x + 2 * y) + pow(x, 2.0); }
double f_4(double x, double y) { return 5 * exp(x + 2 * y) + 2; }

double u_5(double x, double y) { return pow(x, 2.0) + pow(y, 3.0) + 1; }
double f_5(double x, double y) { return 6 * y + 2; }

u_func_t add_function(fun_xy u, fun_xy f)
{
    u_func_t res;
    res.f = f;
    res.u = u;
    return res;
}