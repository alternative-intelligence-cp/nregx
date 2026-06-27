import re

with open('src/regex_vm.npk', 'r') as f:
    code = f.read()

loop_orig = """            when (raw asize_list(clist_ah) > 0i64) {
                int64:state = raw apop_state(clist_ah);
                int64:state_start_idx = raw apop_start_idx(clist_ah);
                int32:opcode = npk_mem_read_int32(state, 0i64);
                
                if (opcode == OP_MATCH) {
                    matched = 1i32;
                    running = 0i32;
                    final_start_idx = state_start_idx;
                } else if (c != -1i64) {"""

loop_new = """            int64:sz = raw asize_list(clist_ah);
            int64:ti = 0i64;
            when (ti < sz) {
                int64:state = npk_mem_read_int64(clist_ah, 8i64 + ti * 16i64);
                int64:state_start_idx = npk_mem_read_int64(clist_ah, 8i64 + ti * 16i64 + 8i64);
                int32:opcode = npk_mem_read_int32(state, 0i64);
                
                if (opcode == OP_MATCH) {
                    matched = 1i32;
                    running = 0i32;
                    final_start_idx = state_start_idx;
                    ti = sz;
                } else if (c != -1i64) {"""

code = code.replace(loop_orig, loop_new)

# We need to add `ti = ti + 1i64;` and `drop(aclear_list(clist_ah));` at the end of the block.
# The original block ends with:
#                 }
#             }
#             
#             if (matched == 0i32) {

end_orig = """                }
            }
            
            if (matched == 0i32) {"""

end_new = """                }
                if (ti != sz + 1i64) { ti = ti + 1i64; }
            }
            drop(aclear_list(clist_ah));
            
            if (matched == 0i32) {"""

code = code.replace(end_orig, end_new)

with open('src/regex_vm.npk', 'w') as f:
    f.write(code)

