sed -i 's/int32:opcode = npk_mem_read_int32(state, 0i64);/int32:opcode = npk_mem_read_int32(state, 0i64);\n                if (opcode == OP_MATCH) { exit 99i32; }/g' src/regex_vm.npk
npkc -I src src/test.npk -o test_bin && ./test_bin; echo $?
git restore src/regex_vm.npk
