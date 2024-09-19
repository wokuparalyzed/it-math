// main.c

#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "examples.h"

#define min(x, y) (((x) < (y)) ? (x) : (y))
#define max(x, y) (((x) > (y)) ? (x) : (y))

typedef struct grid_t
{
    size_t size;
    double h;
    double **u;
    double **f;
} net_t;

typedef struct ref_grid_t
{
    size_t size;
    double h;
    double **u;
} grid_t;

typedef struct res
{
    size_t number_of_iterations;
    double total_time;
} res;


double **create_double_2d_arr(size_t size)
{
    double **res = calloc(size, sizeof(*res));
    for (int i = 0; i < size; i++)
        res[i] = calloc(size, sizeof(*res[i]));
    return res;
}

void free_double_2d_arr(double **arr, size_t size)
{
    for (int i = 0; i < size; i++)
        free(arr[i]);
    return free(arr);
}

net_t *create_net(
    size_t size,
    u_func_t u_func)
{
    net_t *res = malloc(sizeof(*res));
    res->size = size;
    res->h = 1.0 / (size - 1);
    res->u = create_double_2d_arr(size);
    res->f = create_double_2d_arr(size);
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            if ((i == 0) || (j == 0) || (i == (size - 1)) || (j == (size - 1)))
            {
                res->u[i][j] = u_func.u(i * res->h, j * res->h);
            }
            else
            {
                res->u[i][j] = 0;
            }
            res->f[i][j] = u_func.f(i * res->h, j * res->h);
        }
    }
    return res;
}

void free_net(net_t *net)
{
    free_double_2d_arr(net->u, net->size);
    free_double_2d_arr(net->f, net->size);
    return free(net);
}

double block_update(net_t *net, size_t a, size_t b, size_t block_size)
{
    int i0 = 1 + a * block_size;
    int im = min(i0 + block_size, net->size - 1);
    int j0 = 1 + b * block_size;
    int jm = min(j0 + block_size, net->size - 1);

    double dm = 0;
    for (int i = i0; i < im; i++)
    {
        for (int j = j0; j < jm; j++)
        {
            double temp = net->u[i][j];
            net->u[i][j] = 0.25 * (net->u[i - 1][j] + net->u[i + 1][j] + net->u[i][j - 1] + net->u[i][j + 1] - net->h * net->h * net->f[i][j]);
            double d = fabs(temp - net->u[i][j]);
            dm = max(dm, d);
        }
    }
    return dm;
}

size_t net_update(net_t *net, double eps, int block_size)
{
    size_t number_of_iterations = 0;
    size_t size_without_borders = net->size - 2;
    size_t number_of_blocks = size_without_borders / block_size;
    number_of_blocks += (block_size * number_of_blocks != size_without_borders) ? 1 : 0;

    double dmax = 0;
    double *dm = calloc(number_of_blocks, sizeof(*dm));
    do
    {
        dmax = 0;
        for (int nx = 0; nx < number_of_blocks; nx++)
        {
            dm[nx] = 0;

            int i, j;
            double d;

#pragma omp parallel for shared(net, nx, dm) private(i, j, d)
            for (i = 0; i < nx + 1; i++)
            {
                j = nx - i;
                d = block_update(net, i, j, block_size);
                dm[i] = max(dm[i], d);
            }
        }

        for (int nx = number_of_blocks - 2; nx > -1; nx--)
        {
            int i, j;
            double d;

#pragma omp parallel for shared(net, nx, dm) private(i, j, d)
            for (i = 0; i < nx + 1; i++)
            {
                j = 2 * (number_of_blocks - 1) - nx - i;
                d = block_update(net, i, j, block_size);
                dm[i] = max(dm[i], d);
            }
        }

        for (int i = 0; i < number_of_blocks; i++)
            dmax = max(dm[i], dmax);

        number_of_iterations += 1;
    } while (dmax > eps);
    free(dm);
    return number_of_iterations;
}

res run(u_func_t used_function, double eps, size_t block_size, size_t net_size)
{
    net_t *net = create_net(net_size, used_function);
    double t1, t2, dt;

    t1 = omp_get_wtime();
    size_t number_of_iterations = net_update(net, eps, block_size);
    t2 = omp_get_wtime();
    dt = t2 - t1;

    free_net(net);
    res res = {.number_of_iterations = number_of_iterations, .total_time = dt};
    return res;
}

res execute(size_t thread_count, double eps, size_t block_size, size_t net_size, int function_number)
{
    u_func_t exp_functions[] = {
        add_function(u_1, f_1),
        add_function(u_2, f_2),
        add_function(u_3, f_3),
        add_function(u_4, f_4),
        add_function(u_5, f_5),
    };
    u_func_t used_function = exp_functions[function_number];
    omp_set_num_threads(thread_count);
    return run(used_function, eps, block_size, net_size);
}

int main(int argc, char *argv[])
{

    size_t threads[] = {1,4,8};
    int function_number = 0;
    size_t thread_count;
    for (int i=0; i<5; i++){
        function_number = i;
    double eps = 1e-6;
    size_t block_size = 40;
    size_t net_size = 100;
        for (int j=0; j<3; j++){
            thread_count = threads[j];
    res result = execute(thread_count, eps, block_size, net_size, function_number);
    printf("On fuction: %d with %zu threads. Iterations: %zu, Total time: %f seconds\n",function_number, thread_count, result.number_of_iterations, result.total_time);
    }
    }
    return 0;
}
