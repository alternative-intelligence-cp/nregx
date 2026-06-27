sed -i 's/int32:match_char = npk_mem_read_int32(state, 4i64);/int32:match_char = npk_mem_read_int32(state, 4i64);\nif (c == 97i64) {\nif (match_char == 97i32) { matched = 112i32; running = 0i32; break; }\nif (match_char == 0i32) { matched = 113i32; running = 0i32; break; }\n}/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
