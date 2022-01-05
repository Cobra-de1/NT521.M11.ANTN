#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    char buf[0x50];
    gets(buf);
    return 0;
}
