#include <stdio.h>
void vm_print_state(long state, int c, int opcode, long out1) {
    printf("EVAL: state=%lx c=%c opcode=%d out1=%lx\n", state, c, opcode, out1);
}
