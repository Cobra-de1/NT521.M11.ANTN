#include <stdio.h>
#include <stdlib.h>

int cost = 500;

void print_flag() {
    char buff[50];
    FILE* fp = fopen("flag.txt", "r");
    fscanf(fp, "%s", buff);
    printf("%s\n", buff);    
    exit(0);
}

void menu() {
    printf("Your cost: %d\n", cost);
    printf("1. Buy stone\n");
    printf("2. Buy flag\n");
    printf("3. Exit\n");
}

int main() {
    int d;
    printf("Welcome\n");    
    while (1) {
        menu();
        scanf("%d", &d);
        if (d == 1) {
            char buf[20];
            printf("How many stone you want to buy?: ");
            scanf("%19s", buf);
            int negative = 0;
            for (int i = 0; i < 19; i++) {
                if (buf[i] == '-') {
                    printf("Entering negative number is NOOB\n");         
                    negative = 1;
                }
            }
            if (negative) {
                continue;
            }
            unsigned z = strtoul(buf, buf + 20, 0);
            cost -= z;
            if (cost < 0) {
                printf("You don't have enough money\n");
                cost += z;
            } else {
                printf("Buy done\n");
            }
        } else if (d == 2) {
            if (cost >= 100000) {
                print_flag();
                break;
            } else {
                printf("You don't have enough money\n");
            }
        } else {
            break;
        }
    }
    printf("Bye");
    return 0;
}
