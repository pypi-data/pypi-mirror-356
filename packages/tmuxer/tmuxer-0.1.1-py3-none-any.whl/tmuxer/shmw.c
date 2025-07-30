#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>


int main(int c, char **v) {
    int f = shm_open(v[1], O_CREAT|O_RDWR, 0600);
    uint64_t n = strtoull(v[2], 0, 10);
    ftruncate(f, n);
    char *p = mmap(0, n, PROT_WRITE, MAP_SHARED, f, 0);

    for (uint64_t i = 0;;) {
        ssize_t r = read(0, p + i, 65536);
        if (r == 0) break;
        if (r < 0) {
            perror("read");
            exit(1);
        }
        i += r;
    }
}
