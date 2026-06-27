sed -i 's/int32:opcode = npk_mem_read_int32(state, 0i64);/int32:opcode = npk_mem_read_int32(state, 0i64);\nif (opcode != 0i32) { exit opcode; }/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
