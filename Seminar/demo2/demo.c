#include <stdio.h>
#include <stdlib.h>

char paragraph[401];

void menu() {
    printf("\n\n1. Input a paragraph\n");
    printf("2. Edit a charracter\n");
    printf("3. Show\n");
    printf("4. Exit\n");
    printf("Chose:\n");
}

int main() {
    printf("Hack ho bo may cai\n");
    printf("Welcome\n");
    printf("This is my stupid code editor!!!\n");
    while (1) {   
        menu();
        int c;
        scanf("%d", &c);
        if (c == 1) {
            printf("Input your paragraph (max 400):\n");
            scanf("%400s", paragraph);
        } else if (c == 2) {
            char buf[20];
            printf("What index you want to change:\n");
            scanf("%19s", buf);
            char d[3];
            printf("Input the charracter:\n");
            scanf("%2s", d);
            getchar();
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
            paragraph[z] = d[0];              
            printf("Change charracter at index %s", buf);         
        } else if (c == 3) {
            printf("%s\n", paragraph);
        } else {
            break;
        }
    }
    printf("Bye\n");
    return 0;
}
