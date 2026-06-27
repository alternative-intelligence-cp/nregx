cat << 'INNER_EOF' > patch_vm.sh
sed -i 's/int64:text_len, int64:start_idx) {/int64:text_len, int64:start_idx) {\n    int64:retval = -1i64;/g' src/regex_vm.npk
sed -i 's/int32:opcode = npk_mem_read_int32(state, 0i64);/int32:opcode = npk_mem_read_int32(state, 0i64);\n        if (retval == -1i64) { retval = opcode => int64; }/g' src/regex_vm.npk
sed -i 's/pass 0i64;/pass retval;/g' src/regex_vm.npk
sed -i 's/drop add_state(start_state, clist_ah, visit_gen, visited_arr, arena_data, work_ah, 0i64, text_len, 0i64);/int64:add_ret = raw add_state(start_state, clist_ah, visit_gen, visited_arr, arena_data, work_ah, 0i64, text_len, 0i64);\n    pass MatchResult{matched: add_ret => int32, start_idx: 0i32, end_idx: 0i32};/g' src/regex_vm.npk
INNER_EOF
bash patch_vm.sh
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
