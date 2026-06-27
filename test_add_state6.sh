sed -i 's/int64:text_len, int64:start_idx) {/int64:text_len, int64:start_idx) {\nint64:retval = 0i64;/g' src/regex_vm.npk
sed -i 's/int32:opcode = npk_mem_read_int32(state, 0i64);/int32:opcode = npk_mem_read_int32(state, 0i64);\nif (retval == 0i64) { retval = opcode => int64; }/g' src/regex_vm.npk
sed -i 's/pass 0i64;/pass retval;/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
