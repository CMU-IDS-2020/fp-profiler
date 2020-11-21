#define SCALE 1024

double A[SCALE][SCALE];
double B[SCALE][SCALE];

void access_by_row(int row_num) {
    int idx = 0;
    for (; idx < SCALE; idx++) {
        B[row_num][idx] = A[row_num][idx];
    }
}

void access_by_col(int col_num) {
    int idx = 0;
    for (; idx < SCALE; idx++) {
        B[idx][col_num] = A[idx][col_num];
    }
}

long long recursive_factorial(int n) {
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * recursive_factorial(n - 1);
}

void do_task() {
    int loop = 0;
    long long ans = 0;
    for (; loop < SCALE * 100; loop++) {
        access_by_row(loop % SCALE);
        access_by_col(loop % SCALE);
        ans = recursive_factorial(SCALE);
    }
}

void main() {
    do_task();
}