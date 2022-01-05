#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char a[0x80];

int main() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    char buf[0x200];
    puts("This is a demo of bypass ROPdefender");
    puts("Make by Acceleration");
    puts("https://github.com/Cobra-de1");
    puts("Payload:");
    read(0, buf, 0x200);
    printf(buf);
    exit(0);
}
