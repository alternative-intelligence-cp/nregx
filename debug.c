#include <stdio.h>
void debug_node(long node, long state) {
    printf("NODE: %p, STATE: %ld\n", (void*)node, state);
    fflush(stdout);
}
