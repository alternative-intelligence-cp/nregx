sed -i 's/int32:match_char = npk_mem_read_int32(state, 4i64);/int32:match_char = npk_mem_read_int32(state, 4i64);\nmatched = (c => int32);\nrunning = 0i32;\nbreak;/g' src/regex_vm.npk
npkc -I src src/test2.npk -o test2_bin && ./test2_bin; echo $?
git restore src/regex_vm.npk
